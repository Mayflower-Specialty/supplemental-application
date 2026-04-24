# To-Do: Future Improvements

Items identified during design/repeatability/scalability review.

## Immediate

- [ ] **Commit `mock_data.py`** — currently untracked; `--filled` flag is broken for anyone else who clones the repo

## High Priority

- [ ] **Single `VERSION` constant** — `"v6"` is duplicated in two output-path string literals (lines 1673 & 1675); a `VERSION = "v6"` constant at the top prevents drift on every version bump
- [ ] **Guard missing `pdfs/` directory** — add `os.makedirs("pdfs", exist_ok=True)` before `BaseDocTemplate` build to prevent `FileNotFoundError` on a fresh clone
- [ ] **Update README** — references v4 filename; doesn't document `--filled` flag, `mock_data.py`, or `uv run`

## Medium Priority

- [ ] **Break `build_story()` into section functions** — the ~1,100-line monolith makes every edit risky; split into `build_section_i(data)`, `build_section_ii(data)`, … that each return `list[Flowable]`
- [ ] **Add `--output` CLI flag** — output path is fully hardcoded; a `--output` arg enables CI, testing, and staging without touching source
- [ ] **Remove old PDF binaries from git** — v3, v4, v5 are tracked binary blobs with no source-code value; add `pdfs/*.pdf` to `.gitignore` and regenerate on demand

## Low Priority

- [ ] **Deduplicate X-drawing logic** — identical 4-line cross-drawing code exists in both `CheckBox.draw()` and `YesNoBoxes.draw()`; extract a `draw_x(canvas, x, y, size)` helper
- [ ] **Fix `AnswerBox` word-wrap** — the manual word-wrap loop (lines 319–337) silently truncates long words and ignores newlines; render answer text via a `Paragraph` drawn inside box bounds instead
- [ ] **Document data schema** — expected dict keys, value types, and index meanings (e.g. `[1]` → "AI Provider, embedded") are only discoverable by cross-referencing `build_story()` with `mock_data.py`; add a `TypedDict` or top-of-file reference table
- [ ] **Lazy-load fonts** — font registration runs as a module-level side effect at import time; wrap in `_setup_fonts()` called once from `build_story()` to allow clean imports from other scripts
