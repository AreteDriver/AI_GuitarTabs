# Guitar Tab Generator - Windows Desktop Application

Professional desktop application for converting guitar audio to tablature in real-time.

![Platform](https://img.shields.io/badge/platform-Windows-blue)
![Python](https://img.shields.io/badge/python-3.10+-green)
![License](https://img.shields.io/badge/license-MIT-blue)

## Features

### 🎸 Core Features
- **Real-time pitch detection** - See notes as you play
- **Electric guitar optimization** - Specialized mode for clean signals
- **Multiple audio inputs** - Support for audio interfaces, USB mics, built-in mic
- **Professional tablature** - Clean, readable guitar tabs
- **Multiple formats** - ASCII, JSON, or compact output
- **Save & export** - Export tabs to text files

### ⚡ Performance
- **Low latency** - Sub-100ms pitch detection
- **High accuracy** - Optimized autocorrelation algorithm
- **Noise gate** - Filters unwanted background noise
- **Adjustable sensitivity** - Fine-tune for your setup

### 💻 User Interface
- **Clean, modern design** - Professional PyQt6 interface
- **Real-time monitoring** - Live pitch and note display
- **Easy controls** - One-click recording
- **Large display** - Comfortable tablature viewing
- **Quick actions** - Copy, save, clear with one click

## Screenshots

```
┌─────────────────────────────────────────────────────────────┐
│  🎸 Guitar Tab Generator                          [_][□][X] │
├─────────────────────────────────────────────────────────────┤
│ Settings               │  Generated Tablature:              │
│ ☑ Electric Guitar Mode │  e|--0--5--7--5--3--0-------------|│
│ ☑ Enable Noise Gate   │  B|--0--5--7--5--3--0-------------|│
│ Sensitivity: [Medium▼] │  G|--1--5--7--5--4--1-------------|│
│ Audio: [Interface  ▼]  │  D|--2--7--9--7--5--2-------------|│
│                         │  A|--2--7--9--7--5--2-------------|│
│ Pitch Monitor          │  E|--0--5--7--5--3--0-------------|│
│     A4                  │                                    │
│   440.0 Hz             │  Notes detected: 12                │
│  5th (A)               │  Duration: 8.3s                    │
│                         │                                    │
│ [● Start Recording]    │  [Clear] [Copy] [Save As...]       │
└─────────────────────────────────────────────────────────────┘
```

## Installation

### Option 1: Use Pre-built Executable (Easiest)

1. Download `GuitarTabGenerator.exe` from releases
2. Double-click to run
3. That's it!

**No Python installation required!**

### Option 2: Run from Source

**Requirements:**
- Python 3.10 or higher
- Windows 10 or higher

**Install:**
```bash
# Clone or download this repository
cd GuitarTabGenerator_Desktop

# Install dependencies
pip install -r requirements.txt

# Install tabsynth package (from parent directory)
pip install -e ../tabsynth

# Run application
python main.py
```

## Building Executable

To create a standalone .exe file:

```bash
# Method 1: Use build script (recommended)
build.bat

# Method 2: Manual PyInstaller
pyinstaller --name=GuitarTabGenerator --onefile --windowed main.py
```

The executable will be in `dist/GuitarTabGenerator.exe`

**Size:** ~50MB (includes all dependencies)

## Usage Guide

### Basic Workflow

1. **Configure Settings**
   - Enable "Electric Guitar Mode" for electric guitars
   - Enable "Noise Gate" to filter background noise
   - Select your audio input device
   - Choose sensitivity level

2. **Start Recording**
   - Click "Start Recording" button
   - The pitch monitor will show current notes in real-time

3. **Play Your Guitar**
   - Play one note at a time for best results
   - Watch the note display update in real-time
   - Play clearly and distinctly

4. **Stop Recording**
   - Click "Stop Recording" when finished
   - Wait a few seconds for processing

5. **View & Save**
   - Review generated tablature
   - Copy to clipboard or save to file

### Audio Setup

**For Electric Guitar:**
```
Guitar → Audio Interface → Computer → Select interface in app
         (Focusrite, etc)
```

**For Acoustic Guitar:**
```
Guitar → Microphone → Computer → Select microphone in app
         (USB mic or built-in)
```

**Recommended Audio Interfaces:**
- Focusrite Scarlett Solo/2i2
- PreSonus AudioBox
- Behringer U-Phoria UM2
- Any USB audio interface

### Settings Explained

**Electric Guitar Mode**
- Optimized for clean electric guitar signal
- Lower noise threshold
- Tighter pitch tolerance (30 cents)
- Supports 24-fret guitars

**Noise Gate**
- Filters out quiet background noise
- Prevents false detections from room noise
- Adjust sensitivity if notes are missed

**Sensitivity Levels**
- **Low:** Picks up quieter playing (more sensitive)
- **Medium:** Balanced (recommended)
- **High:** Only loud/clear playing (less sensitive)

**Output Formats**
- **ASCII:** Traditional text-based tablature
- **Compact:** Condensed format with timestamps
- **JSON:** Structured data for other tools

## Tips for Best Results

### Playing Technique
- ✅ Play one note at a time
- ✅ Play clearly and distinctly
- ✅ Use consistent picking strength
- ✅ Wait briefly between notes
- ❌ Avoid strumming chords (single notes only)
- ❌ Don't play too fast initially

### Audio Setup
- ✅ Use audio interface for best quality
- ✅ Position microphone 6-12 inches from guitar
- ✅ Minimize background noise
- ✅ Test levels before recording
- ❌ Avoid room with echo/reverb
- ❌ Don't record in noisy environment

### Settings
- Start with **Electric Guitar Mode ON** if using electric
- Start with **Medium sensitivity**
- Adjust noise gate if getting false detections
- Try different audio inputs if quality is poor

## Troubleshooting

### No Audio Input Devices Found
**Solution:** Check that your audio interface is connected and drivers are installed.

### No Pitch Detected
**Solutions:**
1. Increase microphone/input volume
2. Lower sensitivity setting
3. Disable noise gate temporarily
4. Play closer to microphone
5. Check that correct input device is selected

### Incorrect Notes
**Solutions:**
1. Tune your guitar
2. Enable electric guitar mode for clean signal
3. Increase noise gate threshold
4. Play more distinctly
5. Try different audio input

### Application Won't Start
**Solutions:**
1. Install Visual C++ Redistributable
2. Run as administrator
3. Check Python version (3.10+)
4. Reinstall dependencies

### Audio Latency/Lag
**Solutions:**
1. Use ASIO driver if available
2. Reduce buffer size in audio interface settings
3. Close other audio applications
4. Use dedicated audio interface instead of built-in mic

## Technical Details

### Architecture
```
Audio Input → sounddevice → Real-time Pitch Detection
                                    ↓
                          Event Aggregation
                                    ↓
                          TabSynth Engine (DP Optimization)
                                    ↓
                          Tablature Display
```

### Audio Processing
- **Sample Rate:** 44100 Hz
- **Channels:** Mono (1 channel)
- **Buffer Size:** 4096 samples
- **Algorithm:** Autocorrelation pitch detection
- **Frequency Range:** 82-1318 Hz (guitar range)

### Performance
- **Pitch Detection:** <50ms latency
- **Memory Usage:** ~100MB
- **CPU Usage:** <5% (modern CPU)
- **Disk Space:** 50MB (executable)

## Keyboard Shortcuts

- `Ctrl+S` - Save tablature
- `Ctrl+Q` - Exit application
- `Space` - Start/stop recording (when focused)

## Project Structure

```
GuitarTabGenerator_Desktop/
├── main.py                 # Application entry point
├── src/
│   ├── gui/
│   │   └── main_window.py # Main UI window
│   ├── audio/
│   │   ├── recorder.py    # Audio recording
│   │   └── pitch_detector.py # Pitch detection
│   └── core/
│       └── tab_processor.py # Tablature generation
├── assets/
│   └── icon.ico           # Application icon
├── build/
│   └── build_exe.py       # Build script
├── requirements.txt       # Python dependencies
├── build.bat             # Windows build script
└── README.md             # This file
```

## Dependencies

- **PyQt6** (6.6.1) - GUI framework
- **sounddevice** (0.4.6) - Audio I/O
- **numpy** (1.26.2) - Numerical processing
- **tabsynth** - Core tablature engine
- **PyInstaller** (6.3.0) - Executable builder

## System Requirements

**Minimum:**
- Windows 10 or higher
- Intel Core i3 or equivalent
- 4GB RAM
- 100MB free disk space
- Audio input device (mic/interface)

**Recommended:**
- Windows 11
- Intel Core i5 or better
- 8GB RAM
- USB audio interface
- Electric guitar with clean signal

## Comparison: Desktop vs Mobile

| Feature | Desktop App | Mobile App |
|---------|------------|------------|
| **Audio Quality** | ⭐⭐⭐⭐⭐ Professional | ⭐⭐⭐ Good |
| **Screen Size** | ⭐⭐⭐⭐⭐ Large | ⭐⭐ Small |
| **Portability** | ⭐⭐ Desk-bound | ⭐⭐⭐⭐⭐ Anywhere |
| **Setup Time** | ⭐⭐⭐ Quick | ⭐⭐⭐⭐⭐ Instant |
| **Audio Interface** | ⭐⭐⭐⭐⭐ Full support | ⭐⭐ Limited |
| **Processing Speed** | ⭐⭐⭐⭐⭐ Fast | ⭐⭐⭐⭐ Fast |
| **Multi-tasking** | ⭐⭐⭐⭐⭐ Easy | ⭐⭐ Hard |

**Use Desktop When:**
- Recording in home studio
- Using audio interface
- Want large display
- Serious transcription work
- Need to edit/export easily

**Use Mobile When:**
- Playing on couch
- Quick idea capture
- Multiple locations
- No computer available
- Jamming with friends

## Known Limitations

- Single note detection only (no chord detection yet)
- Requires relatively clean audio signal
- May struggle with very quiet or very loud signals
- Bent notes may not be detected accurately
- Works best with standard tuning

## Future Enhancements

- [ ] Chord detection and recognition
- [ ] Support for alternate tunings
- [ ] MIDI export
- [ ] Guitar Pro file export
- [ ] Playback feature
- [ ] Metronome integration
- [ ] Multi-track recording
- [ ] VST plugin support

## License

MIT License - See LICENSE file for details

## Credits

**Developed by:** ARETE  
**Core Engine:** TabSynth (Python package)  
**GUI Framework:** PyQt6  
**Audio Library:** sounddevice

## Support

For issues, questions, or feature requests:
- Open an issue on GitHub
- Check troubleshooting section above
- Review settings recommendations

## Version History

**v1.0.0** (Current)
- Initial release
- Real-time pitch detection
- Electric guitar optimization
- Multiple output formats
- Professional UI

---

**Built for guitarists who want to capture their ideas quickly and professionally.**

🎸 Happy tab generating!
