# Changelog

All notable changes to AI_GuitarTabs will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.6] - 2025-01-06

### Added
- CLI tests (9 new tests)
- CLI module now included in coverage reporting

### Changed
- Simplified render.py header logic (removed redundant check)
- Added pragma:no-cover to unreachable defensive code in optimize.py

### Improved
- Test coverage from 99.38% to 100% (106 tests total)

## [1.0.5] - 2025-01-06

### Fixed
- Applied ruff lint/format fixes

## [1.0.4] - 2025-01-06

### Added
- Comprehensive test suite (97 tests, 99.38% coverage)
- Tests for model validation, fretboard, templates, render, cost, candidates, optimize

## [1.0.3] - 2025-01-05

### Added
- pytest-cov for test coverage reporting
- Expanded chord template library from 5 to 63 templates

## [1.0.2] - 2025-01-05

### Fixed
- PyPI environment configuration in release workflow

## [1.0.1] - 2025-01-05

### Added
- CI badge to README
- CI/CD workflows (lint, test, release)
- CLAUDE.md project instructions
- Dependabot for dependency security updates

## [1.0.0] - 2025-01-04

### Added
- Initial release of tabsynth package
- Core tab synthesis from musical events
- Dynamic programming optimization (Viterbi-style)
- Fretboard representation and Hz↔fret mapping
- Candidate generation for fingering positions
- Cost functions (hand movement, stretch, string changes)
- Output formatters (ASCII, JSON, compact)
- High-level pipeline API
- 5 basic chord templates
- CLI interface for demos

### Documentation
- Comprehensive README with installation and usage
- QUICKSTART.md for quick setup
- Architecture overview
- API reference

[1.0.6]: https://github.com/AreteDriver/AI_GuitarTabs/compare/v1.0.5...v1.0.6
[1.0.5]: https://github.com/AreteDriver/AI_GuitarTabs/compare/v1.0.4...v1.0.5
[1.0.4]: https://github.com/AreteDriver/AI_GuitarTabs/compare/v1.0.3...v1.0.4
[1.0.3]: https://github.com/AreteDriver/AI_GuitarTabs/compare/v1.0.2...v1.0.3
[1.0.2]: https://github.com/AreteDriver/AI_GuitarTabs/compare/v1.0.1...v1.0.2
[1.0.1]: https://github.com/AreteDriver/AI_GuitarTabs/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/AreteDriver/AI_GuitarTabs/releases/tag/v1.0.0
