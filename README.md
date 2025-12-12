# AI_GuitarTabs

This repository contains **tabsynth**, a production-ready Python package for converting pre-detected musical events into playable guitar tablature via dynamic programming optimization.

## About tabsynth

**tabsynth** transforms musical event data (notes and chords) into optimized guitar tablature. It uses:
- Candidate generation for multiple fingering options
- Dynamic programming (Viterbi-style) optimization to minimize hand movement
- Chord template matching for common guitar shapes
- Multiple output formats (ASCII, JSON, compact text)

### Quick Start

```bash
cd tabsynth
pip install -e .
tabsynth demo-notes
```

### Documentation

See the [tabsynth README](tabsynth/README.md) for complete documentation, API reference, and usage examples.

### Package Structure

```
tabsynth/
  ├── src/tabsynth/      # Core package
  ├── tests/             # Test suite (pytest)
  ├── README.md          # Full documentation
  └── pyproject.toml     # Package configuration
```

## Features

- **Event-based input**: Accepts NoteEvent and ChordEvent objects
- **Smart optimization**: Finds optimal fingering sequences
- **Extensible**: Easy to add custom chord templates
- **Well-tested**: Comprehensive test suite
- **Production-ready**: Typed, documented, minimal dependencies

## Example

```python
from tabsynth import NoteEvent, events_to_tablature

events = [
    NoteEvent(pitch_hz=329.63, start=0.0, duration=0.5),  # E4
    NoteEvent(pitch_hz=440.00, start=0.5, duration=0.5),  # A4
]

tablature = events_to_tablature(events, output_format="ascii")
print(tablature)
```

## License

MIT License