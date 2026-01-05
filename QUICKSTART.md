# Quick Start Guide - Windows Desktop App

Get up and running in 5 minutes!

## For Your Friend (End User)

### Download & Run

1. Get the `GuitarTabGenerator.exe` file
2. Double-click it
3. Done!

No installation, no Python, no setup needed.

## For You (Developer)

### Setup Development Environment

```bash
# 1. Clone/copy the project
cd GuitarTabGenerator_Desktop

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install tabsynth (from parent directory)
pip install -e ../tabsynth

# 5. Run the app
python main.py
```

### Build Executable for Distribution

```bash
# Easy way - use build script
build.bat

# Output: dist/GuitarTabGenerator.exe

# Give this .exe to your friend!
```

## First Time Usage

### For Electric Guitar (Recommended)

1. **Open the app**
2. **Check settings:**
   - ✅ Electric Guitar Mode: ON
   - ✅ Noise Gate: ON
   - ⚙️ Sensitivity: Medium
3. **Select audio input:**
   - Choose your audio interface from dropdown
   - Or built-in mic if that's what you have
4. **Click "Start Recording"**
5. **Play a simple scale** (one note at a time)
6. **Click "Stop Recording"**
7. **View your tab!**

### Audio Setup Options

**Option 1: Audio Interface (Best)**
```
Electric Guitar → 1/4" cable → Audio Interface → USB → Computer
                                (Focusrite, etc)
```
- Best audio quality
- Cleanest signal
- Most accurate detection
- Recommended!

**Option 2: Direct Connection**
```
Electric Guitar → USB Guitar Cable → Computer
```
- Works well
- Affordable option
- Good for casual use

**Option 3: Microphone**
```
Acoustic Guitar → USB Microphone → Computer
```
- Works for acoustic
- Budget option
- More background noise

## Tips for Immediate Success

### Your Friend's Setup

Since he plays **electric guitar** and wants to **capture ideas while jamming**:

**Best Setup:**
- Use any audio interface he might have
- Or just hold phone near guitar body (unplugged electric)
- Enable Electric Guitar Mode
- Medium sensitivity

**Workflow:**
1. Has riff idea
2. Opens app (bookmark on desktop)
3. Clicks record
4. Plays riff
5. Clicks stop
6. Saves tab to file
7. Back to jamming!

Total time: 30 seconds

## Troubleshooting

### "No audio devices found"
- Check audio interface is plugged in
- Install interface drivers
- Try restarting app

### "No notes detected"
- Turn up input volume
- Lower sensitivity
- Play louder/closer to mic
- Check correct input selected

### "Wrong notes detected"
- Tune guitar
- Enable Electric Guitar Mode
- Increase noise gate
- Use audio interface instead of built-in mic

## Building for Distribution

### Create the .exe

```bash
# Run build script
build.bat

# Wait 2-3 minutes for PyInstaller

# Output location:
dist\GuitarTabGenerator.exe
```

### Test Before Giving to Friend

```bash
# Test the .exe
dist\GuitarTabGenerator.exe

# Try these tests:
1. Open app - should launch quickly
2. Record 5 seconds of audio
3. Stop and generate tab
4. Save to file
5. Copy to clipboard
6. Close app

# If all work, you're good to go!
```

### Distribution

**Option 1: Direct File**
- Send him the .exe via email/USB/network
- Tell him: "Just double-click it"

**Option 2: Shared Folder**
- Put .exe on shared drive
- He can run it from there

**Option 3: Create Shortcut**
- Create shortcut to .exe on his desktop
- Rename to "Guitar Tab Generator"
- Add nice icon if you want

## What to Tell Your Friend

"Hey, here's that guitar tab app!

Just double-click **GuitarTabGenerator.exe** to run it.

Quick guide:
1. Make sure 'Electric Guitar Mode' is checked
2. Click 'Start Recording'
3. Play your riff (one note at a time works best)
4. Click 'Stop Recording'
5. Your tab appears on the right!

You can save it to a file or copy it.

If it's not picking up notes, try:
- Playing louder
- Selecting your audio interface in the Audio Input dropdown
- Adjusting Sensitivity to Low

Let me know how it works!"

## Advanced: Audio Interface Setup

If your friend has an audio interface:

### Focusrite Scarlett (Popular Choice)

1. **Physical connections:**
   - Guitar → Interface input 1
   - Interface → Computer USB

2. **Interface settings:**
   - Gain knob: Start at 12 o'clock
   - Monitor: Can be on or off
   - Direct Monitor: Off (to avoid latency)

3. **App settings:**
   - Audio Input: Select "Scarlett" from dropdown
   - Sensitivity: Medium
   - Electric Guitar Mode: ON

4. **Adjust gain:**
   - Play guitar
   - Adjust gain knob until signal LED is green (not red)
   - If app says "too quiet", turn up gain
   - If app says "too loud", turn down gain

## File Sizes

- **Source code:** ~50KB
- **With dependencies:** ~300MB (dev environment)
- **Built .exe:** ~50MB (single file)
- **Memory usage:** ~100MB while running
- **Disk space needed:** 100MB total

## System Requirements

**Minimum:**
- Windows 10
- Any modern PC from last 10 years
- 4GB RAM
- Audio input (interface or mic)

**Your friend's setup will definitely work!**

## What If He Doesn't Like Desktop?

No problem! You also built the mobile app.

**Mobile app is better for:**
- Couch playing ✓ (your friend's use case)
- Quick idea capture ✓ (your friend's use case)
- Multiple locations ✓ (your friend's use case)

**Desktop app is better for:**
- Audio interface use
- Large screen work
- Serious transcription
- Long recording sessions

**Give him both!** Let him choose what works better for his workflow.

## Next Steps

1. **Build the .exe:**
   ```bash
   build.bat
   ```

2. **Test it yourself:**
   ```bash
   dist\GuitarTabGenerator.exe
   ```

3. **Give to friend:**
   - Send him the .exe
   - Send him this quick start guide
   - Tell him to message you if issues

4. **Collect feedback:**
   - What works well?
   - What's confusing?
   - What features would help?

## Done!

That's it! Your friend now has a professional desktop app for capturing guitar ideas.

**Total build time:** 5 minutes  
**Total file size:** 50MB  
**User experience:** Double-click and go

🎸 Rock on!
