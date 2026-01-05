# Claude Code Build Doc — AI_GuitarTabs Mobile + API Hardening

## Objective
Build the missing product layer to ship **AI Guitar Tabs** to mobile:
- A cross-platform mobile app (iOS + Android) that:
  1) stores projects locally,
  2) creates/imports musical events (manual + MIDI),
  3) calls the existing `tabsynth` FastAPI backend (`POST /tablature/json`),
  4) renders tablature from the structured JSON,
  5) supports playback cursor + metronome,
  6) exports tab (ASCII/JSON/share).

Also harden the backend for mobile:
- API versioning (`/v1/...`), CORS, optional tuning/capo support, request/response typing, and consistent error handling.

You will scaffold + implement a **complete MVP** with clean architecture and sane defaults. Prefer “working end-to-end” over perfection.

---

## Assumptions (do not ask unless blocked)
- Mobile stack: **React Native (Expo)** + **TypeScript**
- Navigation: **expo-router**
- Local persistence: **expo-sqlite** (simple project storage)
- MIDI import: parse `.mid` to note events (timing + pitch), then convert to Hz and group chords.
- Backend: existing `tabsynth` package (FastAPI app in `tabsynth/src/tabsynth/api.py`) with documented endpoints:
  - `POST /tablature/json` returns list of TabState objects (structured JSON).
  - `POST /tablature` returns text/compact/json.
- User will run backend locally for dev and host later.

---

## Repo Plan
Create a new repo: `AI_GuitarTabs_Mobile` (or `tabsynth-mobile` if you prefer).

Structure:
```
AI_GuitarTabs_Mobile/
  README.md
  apps/
    mobile/
      app/                 # expo-router routes
      src/
        api/
        models/
        storage/
        midi/
        render/
        playback/
        utils/
      package.json
      app.json
      tsconfig.json
  packages/
    shared/                # shared types and utilities
      src/
        types.ts
        midi.ts
        tab.ts
      package.json
      tsconfig.json
  .gitignore
  LICENSE
```

---

## Step A — Create the Mobile Repo (Expo Router)

### A1) Initialize
Commands (run exactly):
1) Create repo folder and initialize git
2) Create Expo app under `apps/mobile` with TypeScript + expo-router
3) Configure workspace (pnpm preferred; npm ok)

Use pnpm if available:
- `pnpm -v` check; if not installed: `npm i -g pnpm`

Commands:
```bash
mkdir -p AI_GuitarTabs_Mobile/apps
cd AI_GuitarTabs_Mobile
git init -b main

# Create expo app
cd apps
npx create-expo-app@latest mobile -t tabs@latest
cd mobile

# Add expo-router (if template didn't already)
npx expo install expo-router react-native-safe-area-context react-native-screens
```

Then restructure for expo-router:
- Ensure `apps/mobile/app/_layout.tsx` exists and uses Stack.
- Ensure `apps/mobile/app/index.tsx` routes to Library screen.

### A2) Dependencies
In `apps/mobile`, install:
```bash
npx expo install expo-sqlite expo-file-system expo-document-picker
npm i zod axios
npm i @react-native-community/slider
```

For MIDI parsing:
- Prefer a JS MIDI parser that works in React Native. Use `@tonejs/midi` if it works; otherwise use `midi-parser-js`.
Try:
```bash
npm i @tonejs/midi
```
If bundling breaks, fall back to:
```bash
npm i midi-parser-js
```

### A3) Shared package
Create `packages/shared` with:
- `types.ts`: Event models + TabState types
- `midi.ts`: MIDI → events conversion (Hz conversion and chord grouping)
- `tab.ts`: rendering helpers (chunking into measures/rows)

Set up workspace:
- Root `package.json` with workspaces `["apps/*","packages/*"]`
- `packages/shared/package.json` with `"name": "@arete/shared"` and `"main": "src/index.ts"`

---

## Step B — Data Models (match backend)

Create models in `packages/shared/src/types.ts`:

### Event Models (request)
- `NoteEvent`: `{ type:"note"; pitch_hz:number; start:number; duration:number }`
- `ChordEvent`: `{ type:"chord"; pitches_hz:number[]; start:number; duration:number }`
- `Event = NoteEvent | ChordEvent`

### Request
- `TablatureRequest`: `{ events: Event[]; output_format?: "ascii"|"json"|"compact"; max_fret?: number; tolerance_cents?: number; tuning?: string[]; capo?: number }`
  - tuning/capo are forward-compatible (backend will be updated).

### Response for `/tablature/json`
- `TabState` based on API.md:
  - index, start, duration, kind, strings, frets, mean_fret, min_fret, max_fret, requires_barre, chord_id

Use zod schemas for runtime validation.

---

## Step C — Backend Hardening Patch (tabsynth)

Target file: `tabsynth/src/tabsynth/api.py`

### C1) Add CORS
Allow local dev from Expo:
- `http://localhost:8081`
- `http://127.0.0.1:8081`
- `exp://*` isn’t literal; for dev allow `*` or configure env.

Use `fastapi.middleware.cors.CORSMiddleware` with env-controlled origins.

### C2) Versioned routes
Keep old endpoints for backwards compatibility, add v1:
- `/v1/health`
- `/v1/tablature`
- `/v1/tablature/json`

Implementation: mount a router with prefix `/v1` and include existing endpoints.

### C3) Optional tuning + capo support (minimal)
- Extend request model to accept `tuning` (array of note names or MIDI numbers) and `capo`.
- Default: standard tuning E2 A2 D3 G3 B3 E4 and capo=0.
- Update `Fretboard` construction to use provided tuning, applying capo offset to base frets if needed.

If full tuning refactor is too large, implement “accept but ignore” safely for MVP:
- Parse and validate tuning/capo.
- Return it in response metadata (so client can keep consistent).
- Then schedule full tuning support as Phase 2.

### C4) Consistent errors
Return JSON errors:
```json
{ "error": { "code": "...", "message": "...", "details": ... } }
```
Use `HTTPException` handlers.

### C5) Update API.md
Add v1 endpoints, CORS note, and tuning/capo fields.

---

## Step D — Mobile App Implementation

### D1) Screens (expo-router routes)
Routes under `apps/mobile/app`:
- `index.tsx` → redirect to `/library`
- `library.tsx` → Project Library
- `project/[id].tsx` → Project Editor (events list + import midi + generate)
- `viewer/[id].tsx` → Tab Viewer (render + playback cursor + export)

### D2) Storage (SQLite)
Create `apps/mobile/src/storage/db.ts`:
- Initialize database with tables:
  - `projects(id TEXT PK, title TEXT, bpm REAL, tuning TEXT, createdAt TEXT, updatedAt TEXT)`
  - `events(id TEXT PK, projectId TEXT, type TEXT, payload TEXT, start REAL, duration REAL)`
  - `tabcache(projectId TEXT PK, payload TEXT, updatedAt TEXT)`

Store payload as JSON string (simple MVP).

Provide CRUD functions:
- `listProjects`, `createProject`, `getProject`, `deleteProject`
- `listEvents(projectId)`, `addEvent`, `updateEvent`, `deleteEvent`
- `getCachedTab(projectId)`, `setCachedTab(projectId, tabStates)`

### D3) API client
`apps/mobile/src/api/client.ts`:
- Base URL from env/config:
  - For Android emulator: `http://10.0.2.2:8000`
  - For iOS sim: `http://localhost:8000`
Provide a UI setting to override base URL (stored in sqlite or AsyncStorage).

Functions:
- `generateTabJson(req: TablatureRequest): Promise<TabState[]>`
- `generateTabAscii(req: TablatureRequest): Promise<string>`

Validate responses with zod.

### D4) Manual event editor (simple but usable)
In `project/[id].tsx`:
- Render an events list sorted by start time.
- Add “Add Note” and “Add Chord” modals with fields:
  - pitch (Hz or note name selectable), start, duration
- Include quick note-name → Hz helper:
  - A4=440, midi conversion function for note names.
- Save to SQLite.

### D5) MIDI import
In `apps/mobile/src/midi/import.ts`:
- Use DocumentPicker to pick `.mid`
- Parse:
  - Extract noteOn/noteOff pairs
  - Compute start/duration in seconds using tempo map
  - Convert MIDI note number → Hz: `440 * 2 ** ((n - 69)/12)`
- Group notes that share similar `start` (within epsilon, e.g. 0.02s) into chords:
  - if 2+ notes overlap at same start → chord event
  - else note event
- Insert into SQLite, replacing or appending (choose replace by default; prompt user).

### D6) Generate tab + cache
On “Generate”:
- Read events from DB, build request with defaults:
  - `max_fret=15`, `tolerance_cents=50`
- Call `/v1/tablature/json` (fall back to `/tablature/json` if v1 not available)
- Cache in `tabcache`
- Navigate to viewer screen

### D7) Tab rendering (MVP)
Implement `apps/mobile/src/render/TabGrid.tsx`:
- Take `TabState[]` and render as a vertical list of “columns” (time slices)
- Display six strings (e B G D A E) as rows
- For each state:
  - Place fret numbers in the appropriate string row
  - Empty strings show `-`
- Provide horizontal scrolling for measures if needed
- Provide “compact mode”: group into 16–32 states per row to fit screen

MVP rendering rules:
- Monospace font
- Fixed cell width
- Simple row chunking (no advanced engraving)

### D8) Playback cursor + metronome (MVP)
In `apps/mobile/src/playback/metronome.ts`:
- Implement a JS timer-based metronome (no audio click in v1 if complicated)
- Cursor moves through states by `start + duration`
- Highlight current state column
- Controls: play/pause, tempo slider, loop toggle

(If you can add an audio click easily using `expo-av`, do it. Otherwise ship cursor-only.)

### D9) Export/share
In viewer:
- Export JSON (tab states) to file using `expo-file-system`
- Export ASCII:
  - Either call backend `/tablature` with `output_format="ascii"`
  - Or generate a basic ASCII from states on-device
- Share via OS share sheet (add later if you want; MVP can just save to Files)

---

## Step E — Quality Gates (must pass)
- `npm run start` launches mobile app
- Create project → add manual note → generate tab → see viewer
- Import MIDI → generate tab → see viewer
- Backend runs locally with CORS (Expo can reach it)
- No crashes on empty state (show “No events yet”)

---

## Step F — Deliverables
You must output:
1) Repo URL after pushing `AI_GuitarTabs_Mobile`
2) A short “How to run” section in README:
   - start backend
   - start mobile app
   - set API base URL for emulator/simulator
3) A backend PR (or branch) with:
   - CORS
   - `/v1` routes
   - request model accepting tuning/capo (at least validated, even if not fully applied)

---

## Implementation Notes (important)
- Prioritize end-to-end MVP over perfect UI.
- Keep rendering simple and stable. The MVP is “readable tab + highlight cursor”, not full notation.
- Use strict typing (TypeScript + zod).
- Handle networking errors and show a single clear error banner.

---

## Start Now
Proceed to implement Steps A–F in order. Do not ask clarifying questions unless blocked by tooling limitations.
