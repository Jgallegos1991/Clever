# Changelog

All notable changes to Clever are documented here. This is the canonical changelog; the previous duplicate under `docs/CHANGELOG.md` is now consolidated here.

## [Unreleased]

- (Add upcoming changes here)

## 2025-09-20

### Added

- Unified `clever-ci.yml` workflow: lint, tests, security (non-blocking), doc pattern scan, file inventory auto-commit.
- Advanced NLP reasoning & mode variation system in `persona.py`.
- Hybrid sentiment + readability + concept density pipeline in `nlp_processor.py`.
- Performance benchmarking harness (`tools/perf_benchmark.py`).
- Centralized flake8 config `.flake8`.

### Fixed

- Database `add_utterance` nested scope regression & lock usage consistency.
- Sentiment polarity attribute access guard in NLP layer.
- Port conflict resolution (stale Flask process) clarified in ops docs.

### Removed

- Redundant legacy GitHub workflows (documentation enforcement, coverage, performance monitor, dependency security duplicates, release notes, stale branch cleanup, inventory updater). Replaced by consolidated `clever-ci.yml`.

### Moved / Consolidated

- Misnamed `changlog.md` contents merged here; `docs/CHANGELOG.md` marked deprecated.

### Notes

- Future enhancements: extend variation to non-Auto modes, richer long-term memory weighting, CI-integrated performance thresholding, offline guard negative tests.

