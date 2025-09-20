# Changelog

All notable changes to Clever are documented here. This is the canonical changelog; the previous duplicate under `docs/CHANGELOG.md` is now consolidated here.

## [Unreleased]

- (Add upcoming changes here)

### Changed

- Documentation coverage raised to 100% (module-level Why/Where/How across all scanned Python files).
- Refined `tools/docstring_enforcer.py` to use relative path exclusion (eliminates false duplicate-path hits and preserves accurate coverage metrics).

### Added (Unreleased)

- Placeholder tests `tests/test_util_placeholders.py` safeguarding return contracts for `summarize_repo.summarize()` and `self_fix.plan_self_fixes()`.

### Security

- Identified one moderate dependency vulnerability via GitHub advisory (Dependabot alert #2) – assessment pending; remediation path to be evaluated in next cycle.

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
