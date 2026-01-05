# AI_GuitarTabs - Project Instructions

## Project Overview
Convert guitar audio/MIDI to optimized tablature using dynamic programming.

**Stack**: Python, FastAPI (optional API layer)
**Core Package**: `tabsynth/` - tab synthesis library

---

## Architecture

### tabsynth Package
- **model.py** - Data models (NoteEvent, ChordEvent, PlayableState)
- **fretboard.py** - Guitar fretboard representation, Hz↔fret mapping
- **candidates.py** - Generate fingering candidates for each event
- **cost.py** - Transition cost functions (hand movement, stretch)
- **optimize.py** - Viterbi-style DP optimization
- **render.py** - Output formatters (ASCII, JSON, compact)
- **pipeline.py** - High-level API combining all steps
- **templates.py** - Common chord shape templates
- **cli.py** - Command-line interface

---

## Development Workflow

```bash
# Setup
cd tabsynth
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Test
pytest -v

# Lint
ruff check .
ruff format .

# CLI usage
tabsynth --help
```

---

## Code Conventions
- Type hints required
- ruff for linting/formatting
- Tests in `tabsynth/tests/`
- Events use Hz for pitch (not MIDI numbers)

---

## Key Algorithms

### Candidate Generation
For each musical event, generate all valid fret positions on all strings within tolerance.

### DP Optimization
Viterbi algorithm minimizing total transition cost:
- Hand position changes
- Finger stretch
- String jumps
- Preference for chord templates

### Output Formats
- **ASCII**: Traditional tab notation
- **JSON**: Structured for programmatic use
- **Compact**: Single-line per string
