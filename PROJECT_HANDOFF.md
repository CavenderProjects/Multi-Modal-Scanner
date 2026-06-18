# Project Handoff — Multi-Modal Vulnerability Scanner
*Generated: June 12, 2026 — last updated June 18, 2026 (Round 27) — Claude reads this automatically when the folder is mounted in Cowork*

---

## Project Overview

### Goals and Purpose

A regulated-environment security assessment platform built for a senior information security professional with 20 years of GRC and security management experience across financial services, healthcare, and real estate. The platform exists in two versions that share the same controls libraries, compliance framework mappings, and report format:

**Version 1 — Claude Code Skill** (`pen-tester/`): AI-augmented assessment workflows running inside Claude Code. Install once, runs wherever Claude Code runs. Produces interactive HTML reports.

**Version 2 — Standalone App** (`pen-tester/standalone/`): Full PyQt6 desktop application. Runs independently with no Claude API dependency. Persistent SQLite scan history, in-app triage interface, prior report carryover. Designed for restricted environments. Note: the OS & Software scanner queries the NVD API for CVE lookups — full air-gap requires either skipping OS assessment or providing a local NVD mirror.

Both versions assess seven target types: Website, AI Agent, API, Source Code, STIG Compliance, OS & Software (Standalone only), and Connected Systems.

### Success Criteria

- All assessment workflows run end-to-end without errors
- Standalone app launches, scans a target, reaches review tier, generates report
- Reports correctly render framework dropdown, language-filtered review steps, FAIL/PASS highlighting, and control requirements
- Git repos are clean, correctly scoped, and pushable via manage.ps1
- Controls count is audited and accurate across all files

---

## Current State

### Completed (this session)

**HTML Report Templates — all four templates updated:**
- `pen-tester/assets/report-template.html`
- `pen-tester/assets/api-report-template.html`
- `pen-tester/assets/code-review-report-template.html`
- `pen-tester/assets/interconnected-report-template.html`

Changes applied to all four:
- `FW_MAP` JavaScript block (12 frameworks × most control families) — maps security controls to framework-specific IDs and labels. **CPX-\* (complexity) and OSAUDIT families have NO entries in any framework table** — those controls always show "⊘ Not relevant" regardless of the selected framework. PATCH/EOL/SVCCONFIG/SVCEXPOSE are covered in NIST SP 800-53, ISO 27001, PCI-DSS, and CMMC but NOT in OWASP Top 10, SOC 2, HIPAA, SEC/FINRA.
- `fmtEvidence()` — bolds `[FAIL]` and `[PASS]` tokens in evidence text
- `detectLanguage()` + `DETECTED_LANG` + `filterReviewSteps()` — auto-detects assessment language (Python, JS, etc.) and shows only matching review steps
- `getFw()` + `getFwInfo()` — retrieves framework short ID and full label for a control
- Framework dropdown (`fwDrop`) — renames control IDs and marks irrelevant controls "Not relevant to this framework"
- "What to confirm" section — shows only the selected framework ID + control label; blank when Default selected
- Expand/collapse buttons — stay highlighted (`.btn-active` CSS class) when clicked
- Notes button — moved to left side; textarea spans full card width
- Control requirements — collapsed `<details>` block at top right of each card

**`pen-tester/standalone/controls.py`** — Framework reference fields added to `_known` set so they no longer leak into `review_procedure`. Committed and pushed to Multi-Modal-Scanner_Standalone.

**`pen-tester/standalone/reporter.py`** — Formatting fixes. Committed and pushed.

**`manage.ps1`** — New file at project root. Provides `status` and `push -Repo scanner|standalone|both -m "msg"` commands for managing dual-repo workflow. Committed to Multi-Modal-Scanner.

**`pen-tester/assets/code-review-report-template.html` — Language autodetection regex fixed (Round 27).** `detectLanguages()` had a stray `'\\'` prefix in the regex constructor: `'\\' + ext.replace('.','[.]')` produced the string `\[.]py` which in the regex engine means literal-`[` + any-char + `]` + `py` — never matched `.py` in evidence text. Fix: removed the prefix so `ext.replace('.','[.]')` alone produces `[.]py`, where `[.]` is a character class matching only a literal dot. All four language extensions (`.py`, `.java`, `.go`, `.php`) now match correctly. Push to scanner repo: `.\manage.ps1 push -Repo scanner -m "fix language autodetection regex in code-review template"`. **The same `detectLanguage()` function in the other three templates (`report-template.html`, `api-report-template.html`, `interconnected-report-template.html`) uses the same broken regex — those templates don't use multi-language filtering today, but should be patched for consistency. Not yet done.**

**`pen-tester/standalone/code_scanner.py` — COMPLIANT result emission fixed (Round 25).** The scanner previously only emitted NON_COMPLIANT results. When no vulnerability pattern matched, controls were silently absent, causing engine.py's fallback to produce NEEDS_REVIEW instead of COMPLIANT. Fix: added `_CPX_UNIVERSAL` (CPX-STRUCT-004, CPX-STRUCT-001, CPX-METRIC-001, CPX-STRUCT-003) and `_CPX_BY_LANG` constants to define which controls are checked per language, plus a `_build_compliant_results(detected_langs, noncompliant_ids)` helper that emits COMPLIANT for every checked control_id that had no NON_COMPLIANT finding. Called at the end of both `scan_directory()` (directory scan) and the single-file path in `scan_target()`. engine.py's `result_by_ctrl` dedup ensures NON_COMPLIANT always wins if any file had a violation. Pushed as commit `16e31f9`.

**`CLAUDE.md`** — Created at project root. Contains session-start reminder (run manage.ps1 status), repo structure, and pending commit reminder. Auto-loaded by Cowork at session start.

**`HOW_TO_START_NEW_SESSION.txt`** — Updated to remove outdated references (pen-test-triage-update, mandatory handoff file uploads, fixed bug count), added manage.ps1 step.

**Bug fixes confirmed:**
- Bug 4 (pyyaml missing from requirements.txt) — FIXED, `pyyaml>=6.0` is present
- Bug 6 (controls count 64 vs 67) — FIXED, `controls-library.md` now says 67, `SKILL.md` now says 67
- Bug 1 (framework fields leaking into review_procedure) — FIXED via controls.py `_known` set

**Git / repo cleanup:**
- `pen-test-triage-update` submodule remote URL updated from `pen-test-triage.git` → `Multi-Modal-Scanner.git`
- Merge conflict resolved (kept remote versions, which had all recent template changes)
- Multi-Modal-Scanner pushed at `fbb4148`
- Multi-Modal-Scanner_Standalone pushed at `16e31f9` (Round 25: code_scanner COMPLIANT fix); Round 26 pushes complete (vulnbank_backend test targets + engine.py no-inference fix + code-review template updates)

**Redundancy audit completed.** Files confirmed safe to delete have NOT been deleted yet — user needs to run the PowerShell commands listed in Next Steps → Immediate item 1.

### In Progress / Partially Done

**Bug 2 (Evidence fallback in engine.py):** FULLY FIXED for `review_required` controls. When no scanner covers a control and no family relatives exist, the fallback now shows: (1) a target profile (scanners run, controls tested, pass/fail counts), (2) "No scanner covers {ctrl_id} — this control requires manual assessment", (3) a structured checklist from `ctrl.test_procedure` (split on `.`, up to 6 steps with `[ ]` checkboxes), falling back to `ctrl.statement` if no test_procedure exists, (4) "Assess manually and select: Accept finding / Compliant / N/A / False positive", (5) confidence set to 0.2. The `automatic_confirmation` tier fallback (line ~219) still shows a shorter message (`"No scanner covers {ctrl_id} directly.\n\nControl: ...\nRequirement: ...\nThis control requires manual verification."`) — but automatic_confirmation controls are expected to have scanner coverage by design, so this path is rarely hit.

**Folder rename / structure cleanup:** The root folder is still named "Revised pen tester" but the repo is `Multi-Modal-Scanner`. Plan to rename has been discussed but not executed (renaming requires reselecting the folder in Cowork).

**Other projects review:** Identified `pen-tester-standalone` and `Pen tester with advice` folders under `C:\Users\slagb\OneDrive\Documents\Claude\Projects\` as potentially redundant with the current project. Could not access them (mount limited to "Revised pen tester"). Needs review in a session with the parent `Projects` folder mounted.

### Blocked

**Bug 3 (STIG parser path):** Supplement described this as going up two dirs incorrectly. Verified in current code: `os.path.dirname(os.path.dirname(os.path.abspath(__file__)))` from `pen-tester/standalone/main.py` correctly resolves to `pen-tester/` → `pen-tester/tools/`. The path appears correct. May have been fixed in a prior session. Verify by actually running the STIG import dialog.

**Bug 5 (STIG report template):** `stig-report-template.html` exists (294 lines, 25 STIG-related references). Has not been verified to produce a correct STIG-format report end-to-end. Needs a test run with a real STIG XCCDF file.

---

## Key Decisions

### Architecture decisions

**Two separate repos, shared filesystem.** Multi-Modal-Scanner tracks `assets/`, `references/`, `SKILL.md`, `manage.ps1`, `CLAUDE.md`. Multi-Modal-Scanner_Standalone tracks all `.py` files at `pen-tester/standalone/`. The outer repo's `.gitignore` excludes `pen-tester/standalone/`. Use `manage.ps1` to push either or both.

**Standalone stays nested at `pen-tester/standalone/`.** Moving it to a sibling folder would break `controls.py`, `reporter.py`, and `main.py` which all use `os.path.dirname(standalone_dir)` to locate sibling `references/` and `assets/` directories. A `config.py` with `PENTESTER_ROOT` env var override was discussed but not implemented.

**Tiered assessment model with three tier names — final, never change:**
- `automatic confirmation` — scanner determines pass/fail definitively; no human review needed
- `review required` — scanner found something that needs human interpretation, OR no scanner covers this control at all (fallback: shows a structured checklist from `test_procedure` + confidence 0.2)
- `manual confirmation` — requires organizational knowledge that no scanner can provide (policy, configuration, access control decisions)

**Control family is AGENT, not SKILL.** Renamed. All references to SKILL as a control family are wrong; SKILL is the Claude Code artifact type.

**Framework mapping is primarily JS, but adding a new framework requires changes in three places.** The FW_MAP block in each template handles control renaming and "not relevant" marking client-side. But a complete new-framework addition also requires: adding mapping rows to each `.md` control library (Markdown), and adding the lowercase key to `controls.py` `_known` (Python). See Extensibility in Critical Nuance for the full checklist.

**Evidence language detection is runtime, not pre-generated.** `detectLanguage()` reads the evidence text to infer programming language, then `filterReviewSteps()` shows only the matching review procedure steps. No pre-filtering at scan time.

### Decisions rejected

**Single repo for both versions** — rejected because the standalone `.py` files and the skill's `assets/references/` files have different commit cadences and different audiences on GitHub.

**Moving standalone to a top-level sibling folder** — rejected because it would break three hardcoded relative path lookups without a config abstraction layer.

**Separate "cross-system" as a distinct product** — rejected; `cross-system-report-template.html` and `cross-system-controls.md` were just old names for the interconnected workflow. The files were confirmed redundant with their `interconnected-*` replacements.

**Plugin architecture for scanners** — discussed, not implemented. The current architecture uses direct imports in `engine.py`. Plugin discovery via a `plugins/` directory was considered but deferred.

---

## What Didn't Work

**Bash sandbox for git operations.** The sandbox mount creates `.git/index.lock` files that block git commands. Every `git add/commit/push` must be run in the user's PowerShell, not via the bash tool. Do not attempt git operations via `mcp__workspace__bash`.

**`manage.ps1` execution.** ~~PowerShell script execution was disabled (`ExecutionPolicy` restriction)~~ — **FIXED (Round 25).** `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` has been run; `manage.ps1` now works normally. Raw git equivalents below are kept for reference only:

```powershell
# manage.ps1 status
cd "C:\Users\slagb\OneDrive\Documents\Claude\Projects\Revised pen tester"
git status --short; git log --oneline -3
cd pen-tester\standalone
git status --short; git log --oneline -3
cd ..\..\..

# manage.ps1 push -Repo scanner -m "msg"
cd "C:\Users\slagb\OneDrive\Documents\Claude\Projects\Revised pen tester"
git add -A; git commit -m "msg"; git push

# manage.ps1 push -Repo standalone -m "msg"
cd "C:\Users\slagb\OneDrive\Documents\Claude\Projects\Revised pen tester\pen-tester\standalone"
git add -A; git commit -m "msg"; git push
cd ..\..\..

# manage.ps1 push -Repo both -m "msg"  (run scanner block, then standalone block)
```

**`git pull --allow-unrelated-histories` on pen-test-triage-update.** The remote had been force-pushed with Multi-Modal-Scanner's history, creating unrelated histories. The pull produced conflicts on every shared file. Resolution: `git checkout --theirs` for all conflicted files, then `git push --force`.

**`git checkout --theirs` run from wrong directory.** Was accidentally run from the parent repo root instead of inside the submodule. "Updated 0 paths" is the tell — always `cd` into the submodule first.

**CLAUDE.md not appearing in git status after `git add`.** The file existed on disk (`Test-Path` returned True) but `git ls-files CLAUDE.md` showed it was already tracked and committed — it had been committed in a prior session. Not a bug; no action needed.

---

## Constraints & Requirements

### Technical constraints

- Python 3.14 (user's exact version: `C:\Users\slagb\AppData\Local\Python\pythoncore-3.14-64\python.exe`)
- PyQt6 6.11.0 / PyQt6-Qt6 6.11.1
- No Claude API dependency in standalone app — ever
- `pen-tester/standalone/` must remain a sibling of `pen-tester/references/` and `pen-tester/assets/` for relative path lookups to work
- Windows paths (backslashes) in all user-facing commands
- `node_modules/` is in `.gitignore` and should never be committed

### Rules and preferences established

- **Accuracy over speed.** Confirm everything is correct before stating it. If uncertain, say so.
- **Terse communication.** No preambles, no "let me..." or "I'll now...". Direct action or direct answer.
- **No over-explaining security concepts.** User has 20 years of GRC and security management experience.
- **Don't ask clarifying questions when intent is clear.** When they say "fix all bugs", fix them — don't ask which ones.
- **Model guidance:** Use Opus for bugs and architectural decisions. Use Sonnet for adding features, regenerating reports, updating docs.
- **Tier names are immutable.** Never shorten "automatic confirmation", "review required", "manual confirmation".
- **Control family is AGENT.** Never call it SKILL in any code or documentation.
- **manage.ps1 status** before any work session. Push via `manage.ps1 push -Repo [scanner|standalone|both] -m "message"`.

### File ownership (which repo tracks what)

```
Multi-Modal-Scanner (root):
  pen-tester/assets/*.html        — report templates
  pen-tester/references/*.md      — control libraries
  pen-tester/SKILL.md             — Claude Code skill definition
  manage.ps1, CLAUDE.md, README.md

Multi-Modal-Scanner_Standalone (at pen-tester/standalone/):
  *.py                            — all Python source files
  requirements.txt, README.md

Shared concern (changes may need both repos):
  standalone/controls.py          — parser logic affects template output
  references/*.md                 — read at runtime by Standalone; tracked in Scanner only
```

---

## Open Questions

1. **pen-tester-standalone folder** (`C:\Users\slagb\OneDrive\Documents\Claude\Projects\pen-tester-standalone`) — Is this an old copy of the standalone app or something different? Needs review when parent Projects folder is mounted.

2. **Pen tester with advice folder** — Same question. May be an earlier version of the project.

3. **Root folder rename** — Should "Revised pen tester" be renamed to "Multi-Modal-Scanner" to match the GitHub repo? Doing so requires reselecting the folder in Cowork. Low priority but creates naming inconsistency.

4. **Bug 3 verification** — STIG parser path appears correct in code but hasn't been tested end-to-end with a real STIG XML file. Confirm by running the STIG import dialog.

5. **Bug 5 verification** — `stig-report-template.html` exists with STIG references but hasn't been verified to produce a correct CAT I/II/III checklist report.

6. ~~**Controls count audit**~~ — RESOLVED.

8. **STIG profile selection is not wired up** — `StigImportDialog` in `main.py` shows a profile dropdown (populated from `parsed['profiles']`), but `_import_stig()` never reads the selected profile index. Always calls `to_markdown(parsed, include_profiles=True)` on the full rule set. All rules are imported regardless of selection. Fix: read `dialog.profile_combo.currentIndex()`, map index → profile, pass `profile_id` to a filter step in `to_markdown()` or filter `parsed` before calling it.

9. **`apply_review_decision()`, `apply_manual_decision()`, and `apply_all_prior_manual()` are all never called from the GUI** — defined on `AssessmentEngine` but `main.py` invokes none of them. `apply_review_decision()` and `apply_manual_decision()` are the individual triage decision methods; `apply_all_prior_manual()` bulk-applies prior DB decisions. Since `apply_review_decision()` and `apply_manual_decision()` are never called, `DecisionsDB.save()` and `FalsePositivesDB.add()` are also never called — leaving both the `decisions` and `false_positives` tables always empty. The entire DB persistence layer for triage is built but non-functional. See Open Question 11.

10. **`prior_evidence_changed` is set but never consumed** — `engine.py` sets `ar.prior_evidence_changed = True/False` during the auto-tier scan when `use_prior=True`, but `main.py` and `reporter.py` never read this field. The intended "evidence changed since last scan" warning badge in the GUI was never implemented. Additionally, `use_prior` is never passed as `True` from `main.py` (always defaults to `False`), so the evidence hash comparison never runs at all in normal GUI flow. `###` header audit confirmed: 67 controls in `controls-library.md` (73 total headers minus 6 appendices), 53 in `api-controls-library.md`, 51 in `code-review-controls.md`, 27 in `interconnected-controls.md`, 12 in `os-software-controls.md`. All match `CONTROL_LIBRARIES` hardcoded counts.

11. **`apply_review_decision()` and `apply_manual_decision()` are never called from the GUI — the in-app triage UI was never built.** Triage happens in the browser via the HTML report. `DecisionsDB.save()` is only inside these two methods (engine.py lines 411, 440), so the `decisions` table is never written. DB-based decision carryforward (`DecisionsDB.get_prior()`) always returns None because the table is always empty. The carryforward mechanism is built but non-functional end-to-end. Only FP carryforward (via report HTML or `FalsePositivesDB`) actually works. To make DB decision carryforward functional, an in-app triage screen would need to be implemented that calls these methods.

7. ~~**Evidence fallback (Bug 2)**~~ — RESOLVED. The review_required tier fallback now shows a target profile + structured checklist from `test_procedure` + confidence 0.2. See Current State → In Progress for the remaining auto tier minor case.

12. **AGENT-007 and AGENT-010 scan results are silently discarded** — `agent_scanner.py` generates findings for both controls (dangerous instructions, no-confirmation patterns) but both are `MANUAL_IDS`, so the manual-tier loop ignores `result_by_ctrl` entirely. The scanner effort is wasted. Resolution options: (a) remove AGENT-007 and AGENT-010 from `MANUAL_IDS` and move them to `review_required` so scanner evidence surfaces in the report, or (b) remove their scan logic from `agent_scanner.py`. Option (a) is preferable since the scanner detects genuinely dangerous configurations. Unresolved — needs a decision before fixing.

---

## Next Steps

### Immediate

1. ~~Run the delete commands to clean up redundant files~~ — **DONE (Round 25).** Files moved to `C:\to-delete-in-30\` via Move-Item; redundant files also removed from git history in commit `6e5a2f0`.

2. ~~Enable PowerShell script execution~~ — **DONE.** `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` confirmed executed. `manage.ps1` runs without restriction.

3. Test STIG import end-to-end (verifies Bug 3 and Bug 5). Expected: dialog opens, parse preview shows title/rules/CAT distribution, import writes `.md` to `pen-tester/references/`.

4. Test the standalone app end-to-end against each target type. Expected result counts (from HANDOFF_SUPPLEMENT section 13): code scanner ~44 findings, API scanner ~12 findings, agent scanner ~9 findings. Test inputs are in `pen-tester/standalone/test_targets/` (local only, gitignored): `code_sample/app.py`, `api_sample/openapi.yaml`, `agent_sample/SKILL.md`. **Also verify code scanner now shows Compliant results (Round 25 fix).**

   Multi-language directory test (Round 26/27): enter `test_targets\code_sample\vulnbank_backend` — scans Python, Java, Go, and PHP together. Expect 30+ NON_COMPLIANT findings plus COMPLIANT results for every clean control. Files: `app.py`, `UserService.java`, `transfer.go`, `payment.php`. **Language autodetection regex was fixed (Round 27) — verify all four languages now appear in "What to confirm".**

5. Review `pen-tester-standalone` and `Pen tester with advice` folders (mount parent Projects folder in Cowork first).

### Longer term

- Bug 2 review_required tier is fixed. Minor gap: `automatic_confirmation` fallback (line ~219) shows a shorter message — low priority since auto-tier controls are expected to have scanner coverage.
- PyInstaller packaging (Phase 10 of original 10-phase plan — only phase not yet complete). Confirm exact rebuild process for `pen-tester.skill` zip artifact (likely: zip the `pen-tester/` directory and rename to `.skill`) and document it here before packaging.
- ~~Code cleanup batch (standalone repo)~~ — **DONE (Round 27).** Removed `ScanResult.elapsed_seconds` from `scanners.py` (dataclass field + all 60 constructor kwargs); removed `HAS_BS4`/`BeautifulSoup` import block from `scanners.py` and `beautifulsoup4` from `requirements.txt`; removed dead `detect_languages()` from `detector.py`; fixed `os-software-controls.md` header to "6 families"; added `fix_text=fields.get('fix text', fields.get('fix', ''))` to the non-STIG `Control()` constructor in `controls.py`. Push: `.\manage.ps1 push -Repo both -m "Round 27: code cleanup batch"`.
- Patch the same language detection regex bug (remove stray `'\\'` prefix) in `detectLanguage()` in the other three templates: `report-template.html`, `api-report-template.html`, `interconnected-report-template.html`. Those templates don't currently use multi-language filtering, but the function is present and broken in all three.
- Resolve AGENT-007/010 inconsistency (Open Question 12): either move both to `review_required` tier or remove their scan logic from `agent_scanner.py`.
- ~~Add Windows 11 to `_OS_EOL` dict~~ — **DONE (Round 25).** All six Win11 versions added using Enterprise/Education dates (same convention as Win10 entries). Win11 version detection mirrors Win10's `display_version` pattern. `win11-22h2` and `win11-23h2` are already past EOL as of June 2026 and will produce NON_COMPLIANT.
- ~~Capture exact pyyaml version~~ — **PyYAML 6.0.3** confirmed installed. `requirements.txt` entry `pyyaml>=6.0` covers it; no change needed.
- Consider externalizing `VULN_PATTERNS` in `code_scanner.py` to a JSON/YAML file for runtime updates without rebuilding
- Consider `config.py` with `PENTESTER_ROOT` env var to allow moving standalone to a sibling directory cleanly
- Rename root folder "Revised pen tester" → "Multi-Modal-Scanner" if desired

---

## Critical Nuance

**The sandbox can't run git.** Every git command in this project must be run in the user's PowerShell. The bash sandbox creates `.git/index.lock` files that block git operations. This is not intermittent — it is consistent. Do not try to work around it.

**pen-test-triage-update was a submodule pointing at the wrong repo.** It was a git submodule inside Multi-Modal-Scanner that pointed to `pen-test-triage.git`, which was force-pushed at some point with Multi-Modal-Scanner's history. The result was two git repos (root and submodule) pointing at the same remote. The submodule's remote has been updated to `Multi-Modal-Scanner.git` and a merge conflict resolved. The directory is queued for deletion (see Next Steps → Immediate item 1) — it duplicates everything in the root repo and serves no purpose. As of handoff it still exists on disk; the user has not yet run the delete commands.

**All four report templates are now in sync.** `report-template.html`, `api-report-template.html`, `code-review-report-template.html`, and `interconnected-report-template.html` all have the same JS utility functions, framework dropdown, language filter, expand/collapse highlight, and notes layout. If a change is made to one template's JS or CSS, it must be applied to all four.

**The "cross-system" naming is retired.** `cross-system-report-template.html` and `cross-system-controls.md` were old names for the interconnected workflow. They existed only in the `pen-test-triage-update/` submodule (queued for deletion, still on disk as of handoff). The current names are `interconnected-report-template.html` and `interconnected-controls.md`. Do not create new files with "cross-system" in the name.

**controls.py `_known` set controls what appears in review_procedure.** Any field key in a control library `.md` file that is NOT in the `_known` set gets appended to `review_procedure` with `.title()` formatting. This was the root cause of framework abbreviations (owasp, nist-800, etc.) appearing as procedure steps. The fix is committed. If new fields are added to the `.md` control libraries, they must also be added to `_known` in `controls.py`.

**`detectLanguage()` reads the evidence text, not the target.** Language detection for "What to confirm" filtering happens client-side in the report template by scanning the evidence string. It is not set at scan time. This means if the evidence text doesn't contain clear language identifiers, all review steps will show.

**`detectLanguages()` / `detectLanguage()` implementation details (verified from source):** Scans `(c.evidence || '') + ' ' + (c.finding || '')` for ALL controls — not just the current card. Counts file extension matches using `[.]ext(?=[:,(\s]|$)` lookahead to avoid mid-word false positives. The character class `[.]` matches only a literal dot (NOT `\.` — no backslash). **Round 27 fix**: the original had a stray `'\\'` prefix producing `\[.]ext` which never matched `.ext` in paths. `code-review-report-template.html` is fixed; the other three templates still have the broken version but don't yet use multi-language filtering. `.kt` maps to `'Java'`. `detectLanguages()` (code-review template) returns a sorted array of all detected languages; `detectLanguage()` (other three templates) returns only the top language or `null`. The `_LANG_KEYS` list that `filterReviewSteps()` uses as section headers is `['Python','Js/Ts','Rust','Java','C/C++','C#','Go','Php']` — these exact strings must appear as line prefixes in the review procedure text. Lines before the first language-keyed section are shown for all languages ("general steps"). If filtering produces an empty string, falls back to the full text.

**`getFwInfo()` has a prefix-match fallback.** After trying an exact `c.family` match in `FW_MAP`, it falls back to checking whether `c.family.startsWith(k)` or `c.id.startsWith(k + '-')` for any key `k` in the framework table. This means CPX-STRUCT would match a 'CPX' key if one were added — but no current framework table has 'CPX', so CPX controls are always "not relevant" in all frameworks.

**Report filter bar — status "active" matches three statuses, not two.** The dropdown option is labeled "Non-compliant + Needs review" but the JS filter `fStatus === 'active'` includes `['NON_COMPLIANT', 'NEEDS_REVIEW', 'NOT_TESTED']`. The NEEDS_REVIEW stat pill likewise expands to `['NEEDS_REVIEW', 'NOT_TESTED']` when matched. Manual-tier controls always arrive as NOT_TESTED — the pill and "active" filter ensures they're visible under the default "needs attention" view.

**Cards auto-expand on render.** `render()` auto-opens `.ctrl.nc`, `.ctrl.nr`, and `.ctrl.manual` cards after building the list. COMPLIANT and NOT_APPLICABLE cards start collapsed. Text search in the filter bar searches `c.id + c.name + c.evidence + c.family` (case-insensitive substring).

**The user is the product owner and architect.** They make design decisions. Do not present options when they have already decided something. Do not override tier names, control family names, or GUI specs. Implement exactly what is specified.

**`stig-report-template.html` was NOT updated this session.** The four templates that received FW_MAP, fmtEvidence, detectLanguage, framework dropdown, etc. are: `report-template.html`, `api-report-template.html`, `code-review-report-template.html`, `interconnected-report-template.html`. The STIG template (`pen-tester/assets/stig-report-template.html`, 294 lines) was intentionally left out — it has a different structure (CAT I/II/III format) and wasn't part of this session's scope.

**FW_MAP lives in all four templates independently.** There is no shared JS file. If a new compliance framework needs to be added, or an existing mapping corrected, the change must be manually applied to all four templates. This is the most likely source of drift.

**`_fw`/`_fwInfo` variable ordering in templates is critical.** These must be computed before `reviewProcHtml` is built, otherwise the framework note can't appear in "What to confirm". In prior code, this was wrong — they were computed after. If editing any template's JS block, preserve the order: compute `_fw` and `_fwInfo` → build `_fwNote` → build `reviewProcHtml` using `${_fwNote}`.

**`_known` set in `controls.py` — what it contains and what matters.** Any field key in a `.md` control library that is NOT in `_known` gets appended to `review_procedure` with `.title()` formatting. The full `_known` set (around line 219 of `controls.py`) contains two categories:

*Standard structural fields* (always present, pre-session): `name`, `control name`, `languages`, `cia`, `sources`, `cwe`, `statement`, `control statement`, `severity`, `severity if non-compliant`, `mapped severity`, `family`, `test`, `test approach`, `check`, `tier`, `source`, `reachability`, `framework`, `fix`, `fix text`, `check content`, `description`, `rationale`, `references`, `rule id`, `group id`, `version`, `weight`, `legacy ids`, `discussion`, `vul discuss`, `ia controls`, `responsibility`, `priority`, `security override guidance`, `potential impact`, `third party tools`, `mitigation control`, `severity override guidance`, `title`, `id`, `mitigations`, `applicable platforms`, `notes`, `common consequences`, `observed examples`

*Framework reference fields added this session*:
```python
'owasp', 'owasp-api', 'nist-800', 'iso-27001', 'cmmc', 'dod-srg', 'fedramp',
'hipaa', 'pci-dss', 'soc2', 'sec-finra', 'eu-dora', 'eu-ai',
'owasp-llm', 'nist-ai', 'iso-42001', 'saif', 'csa-ai',
'secondary', 'secondary cia', 'secondary cia (if applicable)',
```
When new fields are added to control library `.md` files, add the lowercase key to `_known` in `controls.py`. If they already appear in the standard structural fields list above, no change is needed.

**Tier assignment is computed by `classify_control()` in `controls.py`, not set in the `.md` library.** When a control is parsed, its tier is determined by three hardcoded sets near the top of `controls.py`: `AUTO_IDS` (specific control IDs → automatic_confirmation), `AUTO_FAMILIES` (family names → automatic_confirmation), and `MANUAL_IDS` (specific IDs → manual_confirmation). Everything else defaults to `review_required`. Priority: `AUTO_IDS` / `AUTO_FAMILIES` are checked first; `MANUAL_IDS` is only reached if neither auto condition matches. `DATA-001` and `DATA-003` appear in both `AUTO_IDS` and `MANUAL_IDS` — they resolve to `automatic_confirmation` because AUTO wins. To change a control's tier, add/remove its ID from one of these sets in `controls.py` — a `Tier:` field in the `.md` file is recognized (it's in `_known`) but is NOT what drives the actual tier assignment.

**Tier names in code use underscores; display uses spaces.** In `controls.py` and `engine.py`, tiers are the strings `"automatic_confirmation"`, `"review_required"`, `"manual_confirmation"`. In the UI and reports, they display as "automatic confirmation", "review required", "manual confirmation" (spaces). The "tier names are immutable" rule applies to the display form. Both forms must stay in sync.

**`CONTROL_LIBRARIES` dict in `controls.py` hardcodes the control count for every library.** Each entry includes a `"count"` value (e.g. `"count": 67` for `website_agent`). If controls are added or removed from any `.md` library, the corresponding count in this dict must also be updated in `controls.py`. Not updating it won't crash the app but will produce incorrect counts in any UI that displays library statistics. This applies to all five library entries in the dict (`website_agent`, `api`, `code_review`, `interconnected`, `os_software`), not just `website_agent`. STIG controls are not in `CONTROL_LIBRARIES` — they use a separate `parse_stig_controls(md_path)` function.

**`requirements.txt` has only four dependencies:** `PyQt6>=6.6.0`, `requests>=2.31.0`, `beautifulsoup4>=4.12.0`, `pyyaml>=6.0`. Relevant for Phase 10 (PyInstaller packaging) — the dependency footprint is small. Note: `beautifulsoup4` is a dead dependency (the `HAS_BS4` import block in `scanners.py` is never used) and is slated for removal in the code cleanup batch — see Next Steps → Longer term.

**Two separate carryforward mechanisms — DB-based and report-based — are independent.**

- **DB carryforward** (`use_prior` flag + `decisions` table): `load_controls()` ALWAYS calls `DecisionsDB.get_prior(system_id, control_id)` for every control and loads the result into `ar.prior_decision`. **However, the `decisions` table is NEVER WRITTEN in normal GUI flow** — `DecisionsDB.save()` is called only inside `apply_review_decision()` and `apply_manual_decision()` (engine.py lines 411, 440), which are never called from `main.py`. The decisions table is always empty. `DecisionsDB.get_prior()` always returns None. `ar.prior_decision` is always None. The entire DB-based decision carryforward mechanism is built but non-functional. The `use_prior` flag at engine.py line 320 gates evidence-hash comparison, but this is also moot since `use_prior` is never passed as True from `main.py` and the decisions table is empty. `prior_evidence_changed` is set in engine.py but never read by `main.py` or `reporter.py` — the warning badge UI is not implemented.
- **Report carryforward** (`prior_report_data`): user explicitly loads a previous HTML report via the "Load previous report" button in the GUI. `_load_previous_report()` calls `extract_prior_data_from_report()`, validates the HTML contains `sat-controls-data` (rejects non-tool reports), and stores the result as `self.prior_report_data = {control_id: {'is_fp': bool, 'justification': str, 'note': str}}`. This dict is passed to `AssessmentEngine(prior_report_data=...)`.

**`apply_review_decision()`, `apply_manual_decision()`, and `apply_all_prior_manual()` are NOT called by `main.py`.** All three methods on `AssessmentEngine` are non-operational — the GUI never invokes them. The `decisions` table (`DecisionsDB`) and `false_positives` table (`FalsePositivesDB`) are always empty because `DecisionsDB.save()` and `FalsePositivesDB.add()` (both only called inside the unused apply_* methods) are never invoked. `ar.prior_decision` is always None. The only effective carryforward is report-based: FP status and notes from a user-loaded prior HTML report are applied by `run_automatic_tier()` via `prior_report_data`. DB carryforward is entirely non-functional in the current GUI.

**`FalsePositivesDB` uses soft deletion — but the table is never written from the current GUI.** FP records are never hard-deleted — deactivated by setting `is_active=0`. Methods: `add()` (upsert — if FP already exists, re-activates it), `get_active(system_id)` (returns only `is_active=1` records), `check_evidence_changed()` (compares stored evidence hash vs new evidence), `remove(system_id, control_id)` (sets `is_active=0`). Note: the method is `remove()`, not `deactivate()`. **`FalsePositivesDB.add()` is only called inside `apply_review_decision()`, which is never called from `main.py`** — so the `false_positives` table is always empty in practice. `FalsePositivesDB.get_active()` is called during `load_controls()` but always returns `[]`. The soft-delete design is correct for an eventual in-app triage UI but is currently non-operational.

**Several DB read methods exist but are never called from `main.py`:** `ScansDB.get_history(system_id, limit=20)`, `SystemsDB.get_all()`, `SystemsDB.find_by_target(target)`, `DecisionsDB.get_all_for_system(system_id)`. These are designed for a history/audit view that doesn't exist in the current GUI. `CONTROL_LIBRARIES` (from controls.py) is imported in `main.py` line 34 but never accessed — dead import, likely a leftover from an earlier GUI iteration.

**`FindingsDB` is partially written during scan but never read back in the GUI.** `_run_next_target()` in `main.py` calls `engine.start_scan()` at line 905 before starting `ScanWorker` — `scan_id` is always non-None during a scan, so `FindingsDB.save()` is never blocked by a null scan_id guard. `FindingsDB.save()` is called in three places in `engine.py`: (1) at line ~226 in `run_automatic_tier()` for auto-tier controls, (2) inside `apply_review_decision()`, (3) inside `apply_manual_decision()`. Since `apply_review_decision()` and `apply_manual_decision()` are never called from `main.py`, only auto-tier control results are actually written to the `findings` table. Important: NOT all auto-tier controls are saved. When an auto-tier control is promoted to `review_required` (scanner returns `NEEDS_REVIEW`), `continue` at engine.py line ~177 skips the rest of the loop body including `FindingsDB.save()` — promoted controls are NOT saved. Auto-tier controls with no scanner match DO get saved (status=`NEEDS_REVIEW`, short fallback message). Review-tier and manual-tier results are never persisted. `FindingsDB.get_for_scan()` exists but is never called from `main.py` or `reporter.py` — the findings table is an incomplete audit log not surfaced in the UI. Reports are generated from `engine.all_results` (in-memory), not from the DB. **`findings` has no UNIQUE constraint on `(scan_id, control_id)`** — if `apply_review_decision()` or `apply_manual_decision()` are eventually wired up, they call `FindingsDB.save()` for controls already saved in the auto loop, producing duplicate rows. `get_for_scan()` would then return two rows for such controls.

**Prior report import uses `extract_prior_data_from_report()` in `reporter.py`, not `extract_fps_from_report()`.** `extract_fps_from_report()` exists but is deprecated — its docstring says "Prefer `extract_prior_data_from_report` for new callers." `extract_prior_data_from_report(html_path) -> dict` reads the `sat-controls-data` JSON tag and returns broader prior state (decisions, notes, FPs). Returns `{}` on any error (file not found, malformed JSON, non-tool report). `extract_fps_from_report(html_path) -> set` is a thin wrapper that calls `extract_prior_data_from_report` and returns only the FP set. Always use `extract_prior_data_from_report` in new code.

**`extract_prior_data_from_report()` returns a sparse dict** — only controls where `mitigation == 'YES'` (FP) OR a non-empty `note` are included. Controls that are neither FP nor annotated are absent from the returned dict. A control absent from the dict means "no prior FP/note data" — it does NOT mean "was compliant" or "was non-compliant".

**`_parse_controls_from_html()` supports two formats** (backward compatibility):
1. New format: `<script type="application/json" id="sat-controls-data">` tag — current format used by all **non-STIG** generated reports
2. Legacy format: `const CONTROLS = ` inline JS variable — older report format, still readable

This means users with reports generated by an earlier version of the tool can still load them via "Load previous report". If neither tag is found, returns `None` and `extract_prior_data_from_report()` returns `{}`.

**STIG reports are NOT parseable by `_parse_controls_from_html()` — prior carryforward is broken for STIG.** `_generate_stig_html_report()` injects data as `<script>var STIG_META = {...}; var CONTROLS = {...};</script>` (inline JS with `var`, not `const` and not a `sat-controls-data` tag). Neither parser format matches `var CONTROLS`. Consequence: if a user loads a previously saved STIG report via "Load previous report", `extract_prior_data_from_report()` returns `{}` — no FPs or notes are carried forward. All triage from the prior STIG assessment is silently discarded. **No fix is planned yet.** The fix requires changing `_generate_stig_html_report()` to inject data as `<script type="application/json" id="sat-controls-data">` instead of `var CONTROLS`, matching the non-STIG report format so `_parse_controls_from_html()` can read it back.

**`reporter.py` generates four output formats.** `generate_html_report()`, `generate_markdown_report()`, `generate_csv_report()`, `generate_json_report()` — all take `(engine, output_path)`. HTML is the primary format. All formats are exposed in the GUI via the report format dropdown. STIG HTML goes through a separate `_generate_stig_html_report()` (called internally by `generate_html_report()` when any control in `engine.all_results` has `library == 'stig'` — NOT checked against `engine.target_type`). STIG uses a different template (CAT I/II/III format) and maps internal statuses to STIG standard terms: `COMPLIANT` → "Not a Finding", `NON_COMPLIANT` → "Open", `NOT_APPLICABLE` → "Not Applicable", `FALSE_POSITIVE` → "Not a Finding", `NOT_TESTED`/`NEEDS_REVIEW` → "Not Reviewed".

**`reporter.py` template routing** — `get_template_path(target_type, selected_sets)` selects the HTML template based on `selected_sets`:
- `"interconnected"` in `selected_sets` → `interconnected-report-template.html`
- `"code_review"` in `selected_sets` → `code-review-report-template.html`
- `"api"` in `selected_sets` → `api-report-template.html`
- anything else (website, agent, os) → `report-template.html`
STIG bypasses `get_template_path()` entirely and uses `get_stig_template_path()` → `stig-report-template.html`.

**`stig_parser.py` exports two functions.** Located at `pen-tester/tools/stig_parser.py`, dynamically imported in `main.py` via `sys.path.insert(0, tools_dir)`:
- `parse_stig(xml_path, profile_id=None)` — parses XCCDF 1.1 XML; returns `{'benchmark': {...}, 'profiles': [...], 'rules': [...], 'stats': {...}}`
- `to_markdown(parsed, include_profiles=False)` — converts parsed data to `.md` format

**`parse_stig()` return structure** (verified from source):
- `benchmark`: dict with keys `id`, `title`, `description`, `version`, `release_info`, `date`, `publisher`, `source`
- `profiles`: list of `{'id': str, 'title': str, 'selected_rules': [rule_id_refs]}` — each STIG profile with its selected rule idref list
- `rules`: list of rule dicts (one per XCCDF Group); each rule has `vuln_id`, `rule_id`, `version`, `title`, `statement`, `stig_severity` ('high'/'medium'/'low'), `mapped_severity` ('CRITICAL'/'HIGH'/'MEDIUM'), `cat` ('CAT I'/'II'/'III'), `cia`, `srg_refs`, `satisfies`, `ccis`, `fixtext`, `check_content`, `dpms_target`, `dpms_id`, `srg_title`
- `stats`: `{'total_rules': N, 'cat_i': N, 'cat_ii': N, 'cat_iii': N}`

**STIG severity mapping (XCCDF → internal → STIG report display) has a round-trip bug.** `stig_parser.py` maps XCCDF severity to internal severity: `high (CAT I) → CRITICAL`, `medium (CAT II) → HIGH`, `low (CAT III) → MEDIUM`. Then `reporter.py`'s `_sev_to_cat()` maps back for the STIG HTML report: `CRITICAL/HIGH → CAT I`, `MEDIUM → CAT II`, `LOW → CAT III`. Round-trip result:
- CAT I → CRITICAL → `_sev_to_cat` → CAT I ✓
- CAT II → HIGH → `_sev_to_cat` → CAT I ✗ (displayed as CAT I in the STIG report)
- CAT III → MEDIUM → `_sev_to_cat` → CAT II ✗ (displayed as CAT II in the STIG report)

CAT II findings will appear as CAT I in the HTML report; CAT III findings will appear as CAT II. This is a known side effect of the deliberate severity-bumping in the parser (`SEVERITY_MAP`). The summary header stat counts in the generated `.md` file preserve the correct CAT distribution, but the HTML report's per-finding CAT labels are elevated.

**For STIG controls, `control.control_id` = the STIG version string** (e.g., `CYLN-OP-000010`), NOT the Vuln ID. `to_markdown()` uses `### {vuln_id}` (e.g., `### V-267789`) as the Markdown section header — this passes the `^V-\d{5,6}` regex in `_parse_control_section()`. The version string (e.g., `CYLN-OP-000010`) is written as `- **Control ID**: {version}` inside the section body. `parse_stig_controls()` reads `fields.get('control id', fields.get('version', ''))` to set `ctrl_id` — so the version string becomes `control_id` in the `Control` object, while the Vuln ID (`V-267789`) only appears in the header. The Vuln ID is stored separately as `control.vuln_id`. When looking up a STIG control in any DB or report, use the version string, not the Vuln ID.

**STIG CIA classification is keyword-inferred, not authoritative.** `_infer_cia()` does keyword matching on the concatenated rule title + VulnDiscussion text (lowercased). Keywords: C — `encrypt`, `tls`, `ssl`, `certificate`, `credential`, `password`, `authentication`, `confidential`, `pii`, `sensitive data`, `disclosure`, `privacy`, `banner`, `identity provider`, `siem`, `audit`, `log`; I — `integrity`, `tamper`, `modify`, `certificate`, `tls`, `digital signature`, `hash`, `checksum`, `update`, `patch`, `version`, `configuration`; A — `availability`, `timeout`, `session`, `denial`, `database`, `port`, `protocol`, `service`, `disable`, `function`. Multiple CIA letters can trigger. Default when no keywords match: `'C, I'`. CIA is approximate for STIG controls — many keywords overlap (e.g., `certificate` and `tls` both trigger C and I simultaneously).

**`to_markdown()` CCI list is capped at 5 per rule.** `rule['ccis'][:5]` — if a rule has more than 5 CCI identifiers, the excess is shown as `(+N more)` in the generated `.md` file (e.g., `CCI-001234, CCI-001235 (+3 more)`). When `parse_stig_controls()` reads `**CCIs**:` back, it splits on `', '` → the last element of `control.ccis` will contain the `(+N more)` suffix (e.g., `['CCI-001234', 'CCI-001235 (+3 more)']`). This is a cosmetic artifact — the CCI data is displayable but not cleanly list-parseable when the rule has more than 5 CCIs.

**`stig_parser.py` handles XCCDF 1.1 only** (namespace `http://checklists.nist.gov/xccdf/1.1`). STIGs using XCCDF 1.2 or a different namespace will parse silently with empty results or raise XML errors.

**`_infer_cia()` keyword sets (verified from source):** Called for each rule with `(statement, title)` — NOT check_content or fixtext. Scans combined lowercase string for membership:
- Confidentiality (`C`): `encrypt`, `tls`, `ssl`, `certificate`, `credential`, `password`, `authentication`, `confidential`, `pii`, `sensitive data`, `disclosure`, `privacy`, `banner`, `identity provider`, `siem`, `audit`, `log`
- Integrity (`I`): `integrity`, `tamper`, `modify`, `certificate`, `tls`, `digital signature`, `hash`, `checksum`, `update`, `patch`, `version`, `configuration`
- Availability (`A`): `availability`, `timeout`, `session`, `denial`, `database`, `port`, `protocol`, `service`, `disable`, `function`
- **Default if no keywords match: `'C, I'`** (not empty). Note: `certificate` and `tls` appear in BOTH C and I lists, so TLS-related rules always get both. `configuration` in the I list means many rules pick up Integrity even if not specifically about data integrity.

**`stig_parser.py` has a CLI** — usable as `python stig_parser.py <stig.xml> [--output out.md] [--profile <profile_id>] [--format md|json]`. The `--profile` flag DOES apply profile filtering (the GUI import ignores profile selection, but a developer can generate a filtered `.md` file via CLI and use it manually).

**`StigImportDialog` profile selection is cosmetic — it has no effect on which rules are imported.** The dialog (`class StigImportDialog` in `main.py`) shows a profile dropdown with "All rules (N)" plus each STIG profile. However, `_import_stig()` never reads which profile the user selected — it always calls `to_markdown(parsed, include_profiles=True)` on the full parsed data, which writes all rules. The profile selection was implemented in the UI but the filter logic was never wired up. All rules always land in the generated `.md` file regardless of selection. This is an open incomplete feature (not a crash bug, but unexpected UX).

**`stig_paths` passed to `AssessmentEngine` contains paths to generated `.md` files, not XCCDF paths.** Full STIG import flow:
1. User clicks "Import STIG" button → `_import_stig()` opens `StigImportDialog`
2. User selects XCCDF XML file → `StigImportDialog._browse()` calls `parse_stig(xml_path)` immediately (parses while dialog is open)
3. User clicks "Import STIG" button in dialog → `dialog.exec()` returns; `dialog.stig_data['parsed']` holds the already-parsed result
4. `_import_stig()` calls `to_markdown(parsed, include_profiles=True)` — writes all rules to `pen-tester/references/stig-{safe_id}-controls.md`, where `safe_id = benchmark_id.replace(' ', '_').lower()`
5. `StigsDB.save()` records the import in the DB
6. Target list item is added with `data = {'target': xml_path, 'type': 'stig', 'stig_md_path': md_path}` — note `target` is the XCCDF XML path, NOT the MD path; `stig_md_path` is the generated MD path
7. At assessment time: `target = d['target']` (XCCDF path, stored in DB as system target), `stig_paths = [d.get('stig_md_path', '')]` (the `.md` path), passed to `load_all_controls()` → `parse_stig_controls(md_path)`

The `tools_dir` used by `_import_stig()` and `StigImportDialog._browse()`: `os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/tools"` = `pen-tester/tools/`. The `refs_dir`: same two-levels-up + "/references" = `pen-tester/references/`. The existing `stig-cylanceon-prem-controls.md` in `references/` was generated this way from a prior import. **Note: imported STIG `.md` files land in `pen-tester/references/`, which is tracked by Multi-Modal-Scanner — they will be staged on the next `git add -A` from root.**

**`AssessmentEngine.__init__` full signature** (engine.py lines 64–93):
```python
AssessmentEngine(
    target: str,
    target_type: str,
    system_id: int,
    selected_sets: list,
    stig_paths: list = None,
    framework_filter: str = None,
    use_prior: bool = False,
    prior_report_data: dict = None,   # from extract_prior_data_from_report()
    prior_fp_ids: set = None,         # fallback if no prior_report_data
)
```
After construction, call `engine.load_controls()` to load and tier all controls into three lists: `engine.auto_results` (automatic_confirmation), `engine.review_items` (review_required), `engine.manual_items` (manual_confirmation). `engine.all_results` contains all controls combined — this is what `reporter.py` reads. `load_controls()` also pre-loads `prior_decision` from `DecisionsDB` for every control and populates `self.false_positives` from `FalsePositivesDB`. Returns `get_tier_counts(self.controls)` (a dict of tier → count). `engine.scan_id` is `None` until `engine.start_scan()` is called, which creates the `scans` DB row.

**`engine.complete(report_path)`** — called after `_write_reports()` in `main.py`. Counts `findings` (status == `NON_COMPLIANT` only) and `compliant` (status == `COMPLIANT` only), then calls `ScansDB.complete(scan_id, controls_tested, findings_count, compliant_count, report_path)` and `SystemsDB.update_last_scanned(system_id)`. Only runs if `self.scan_id` is set. Important: `findings_count` and `compliant_count` do NOT account for all controls — FALSE_POSITIVE + NOT_APPLICABLE + NOT_TESTED controls fall into neither bucket. The two counts will not sum to `controls_tested`.

**`engine.get_summary()` and `engine.get_findings()`** — two additional methods on `AssessmentEngine` not part of the scan lifecycle but called by `reporter.py` and `_show_results()` in `main.py`:
- `get_summary() -> dict` — returns counts for total, compliant, non_compliant, not_applicable, false_positive, not_tested, critical/high/medium/low, auto_total, review_total, manual_total, auto_findings, review_decided, manual_decided. Used for report header stats and GUI results screen. Important nuances: `critical/high/medium/low` count only NON_COMPLIANT results by severity — INFORMATIONAL findings are NOT counted in any severity key (no `informational` key in the dict); `not_tested` counts only status == `NOT_TESTED`, not `NEEDS_REVIEW`; `false_positive` counts `r.is_false_positive` regardless of status (FPs can be COMPLIANT or NON_COMPLIANT in the raw status field). **`review_decided` and `manual_decided` are always 0 in the current GUI** — they count `r.user_decision` which is only set by `apply_review_decision()` / `apply_manual_decision()`, neither of which is ever called from `main.py`.
- `get_findings() -> list` — returns NON_COMPLIANT results (excluding FPs) sorted by severity: CRITICAL(0), HIGH(1), MEDIUM(2), LOW(3), INFORMATIONAL(4). Used internally; unknown severities sort last. `auto_findings` in the summary dict counts NON_COMPLIANT in `auto_results` — NEEDS_REVIEW-promoted auto controls remain in `auto_results` with status=NEEDS_REVIEW, so they are NOT counted in `auto_findings`.

**`auto_total + review_total + manual_total` can exceed `total`.** Promoted controls (auto-tier scanner returned NEEDS_REVIEW) are appended to `self.review_items` during the auto-tier loop (line 176) but are NEVER removed from `self.auto_results`. So they are counted in both `auto_total` (`len(self.auto_results)`) AND `review_total` (`len(self.review_items)`). `total` (from `all_results`) does NOT double-count them. In a scan with N promotions, `auto_total + review_total + manual_total == total + N`.

**`framework_filter`** is a string like `"pci-dss"` or `"hipaa"` that records which compliance framework was active during the scan. `None` means no filter (all frameworks). **`main.py` never passes `framework_filter` to `AssessmentEngine`** — it is always `None` in the current GUI. `engine.framework_filter` is always `None`; `{{FRAMEWORK}}` in the report is always "All frameworks"; `scans.framework_filter` is always None. Framework selection in reports is handled entirely client-side via the `fwDrop` dropdown in the browser. The `framework_filter` parameter is future infrastructure for a server-side filter.

**`target_type == 'unknown'` falls back to `'website'`** in `_start_assessment()` (main.py line 845): `target_type = d['type'] if d['type'] != 'unknown' else 'website'`. If `detect_target()` returns 'unknown', the GUI treats the target as a website — runs website HTTP scanners against `controls-library.md`, uses `report-template.html`. The scan does not fail or error. If `target_type` is somehow not in `_TYPE_SETS` (shouldn't happen after the unknown→website conversion), `_TYPE_SETS.get(target_type, ['website_agent'])` defaults to `['website_agent']` controls.

**`_TYPE_SETS` in `main.py`** is the canonical target_type → `selected_sets` mapping:
```python
_TYPE_SETS = {
    'website':        ['website_agent'],
    'agent':          ['website_agent'],
    'api':            ['api'],
    'code':           ['code_review'],
    'stig':           [],            # uses stig_paths instead
    'os':             ['os_software'],
    'interconnected': ['interconnected'],
}
```
`selected_sets` drives both `load_all_controls()` in controls.py and `get_template_path()` in reporter.py. STIG is the only type with an empty set — controls come from `stig_paths` (paths to imported STIG `.md` files).

**STIG controls hardcode `tier='review_required'` — they never go through `classify_control()`.** `parse_stig_controls()` (controls.py line 309) sets `tier='review_required'` unconditionally for every STIG control. `classify_control()` is never called for STIG controls. Consequence: for a STIG scan, `engine.auto_results = []` and `engine.manual_items = []` — all STIG controls land in `engine.review_items`. `auto_total = 0`, `review_total = N` (all controls), `manual_total = 0`. Even if a STIG control's version string happened to match an ID in `AUTO_IDS` or `MANUAL_IDS`, it would still be `review_required`.

**STIG scans unintentionally run WEBSITE_SCANNERS.** `target_type='stig'` is passed to `AssessmentEngine`. In `run_automatic_tier()`, the dispatch chain (`if target_type == 'code' ... elif target_type == 'api' ... elif target_type == 'os' ... elif target_type == 'agent' ... else ...`) has no 'stig' branch, so it falls to the `else` clause and calls `run_all_scanners(self.target, 'stig', ...)`. `get_scanners_for_type()` in scanners.py returns `WEBSITE_SCANNERS` for any type not explicitly handled — including 'stig'. These website scanners attempt to scan the XCCDF XML file path as a URL, fail with connection errors, and produce ERROR or empty results. Since `auto_results = []` for a STIG scan, the auto-tier loop processes nothing. The `family_evidence` dict is built from the failed scan results (empty or ERROR), so all STIG review-tier controls get the no-match no-family checklist path: confidence=0.2, structured checklist, status=NOT_TESTED. The scanner errors are harmless in practice — STIG controls are review_required regardless and would all end up NOT_TESTED with checklists even if no scanners ran at all.

**Multi-target scans auto-include `interconnected` controls.** When the user enters more than one target in the GUI (`main.py` line ~856), `'interconnected'` is automatically appended to `selected_sets` (unless it's STIG or already present). This means a multi-target scan runs both the primary library AND the 27 interconnected controls — Connected Systems assessment is triggered automatically, not as a separate explicit choice. A single-target scan never includes interconnected controls.

**`ScanWorker` is a `QThread`.** Scans run in a background thread (`ScanWorker(QThread)` in `main.py`) and emit `pyqtSignal` progress updates. The GUI stays responsive during scanning. If debugging a hang or crash during scanning, it's in the thread, not the main GUI thread. **`_abort_scan()` does NOT terminate the thread** — it only disconnects the `progress` and `finished` signals, sets `scan_worker = None`, and calls `_reset_to_home()`. The underlying `QThread` may continue running in the background. The thread cannot be safely force-terminated in PyQt6 without risking memory corruption. If a scan is aborted and a new scan started, both threads may run concurrently (the old one completes silently since signals are disconnected).

**`ScanWorker.progress` signal is `pyqtSignal(str, str, str, list)` — 4 arguments.** Connected at `scan_worker.progress.connect(self._on_progress)`. Handler signature: `_on_progress(self, name, desc, status, results)`. `status` is either `'running'` (scanner started — appends to scanner feed, updates status label) or `'done'` (scanner finished — increments progress bar and, for each NON_COMPLIANT result in `results`, appends `[SEV] control_id — evidence[:80]` to the findings feed). The `desc` arg appears in the `'running'` line as "name: desc…". The `results` arg is always a list of `ScanResult` objects; when `status == 'running'`, `results` is an empty list (signal is emitted before results are known).

**`prior_report_data` vs `prior_fp_ids` in engine init.** If `prior_report_data` (a dict from `extract_prior_data_from_report()`) is provided, the engine derives FP IDs as `{cid for cid, v in prior_report_data.items() if v.get('is_fp')}`. If only `prior_fp_ids` (a plain set of control IDs) is passed, that's used directly. The two-parameter design lets callers pass either a rich prior-report dict or a simpler set, depending on what's available. **Important**: `self.prior_report_data` is always a dict after `__init__` — a `None` argument becomes `{}`. It is never `None` on the engine object, even if `None` was passed to the constructor (lines 77–82 of engine.py). `user_notes` from a prior report (the `note` key in `prior_report_data`) is also carried forward: `ar.user_notes = prior['note']` (line 381) — this means triage notes from a previous report are pre-populated in the new scan's result objects.

**`control.frameworks` field is always an empty list.** `controls.py` never populates `Control.frameworks` — the parser puts all framework field values into `_known` (to prevent leakage into `review_procedure`) but does not assign them to `ctrl.frameworks`. `reporter.py` writes `r.control.frameworks` to the report JSON but it is always `[]`. Framework display in reports is handled entirely by `FW_MAP` in the templates (client-side). Do not try to read control framework data from `ctrl.frameworks` — read it from the FW_MAP lookup or from the raw `.md` library fields.

**STIG XCCDF import feeds into the same `controls.py` parser.** `stig_parser.py` converts XCCDF rule records into the same field format that `controls.py` expects. The STIG-specific field names in `_known` (`rule id`, `group id`, `check content`, `fix text`, `vul discuss`, `ia controls`, `weight`, `legacy ids`, etc.) exist specifically to accommodate STIG data without leaking into `review_procedure`. This means the entire STIG assessment workflow — from XCCDF import to HTML report — runs through the same code paths as the other assessment types; no separate STIG-specific parser path exists in `controls.py` itself.

**`pen-tester/SKILL.md` vs the SKILL.md that `agent_scanner.py` reads — these are different things.** `pen-tester/SKILL.md` (tracked in Multi-Modal-Scanner) is the Claude Code skill definition file for this scanner project. When a user runs an AI Agent assessment and provides a SKILL.md as the target, `agent_scanner.py` reads THAT file as the agent config being assessed for security vulnerabilities. `agent_scanner.py` also accepts GPT configs, LangChain defs, and MCP manifests as agent targets. There is no circular dependency — the scanner's own SKILL.md is never read by the scanner itself during an assessment.

**Standalone app reads `assets/` and `references/` at runtime from the local filesystem.** `reporter.py` finds templates by resolving `os.path.join(standalone_dir, '..', 'assets')`. `controls.py` finds libraries via `os.path.join(standalone_dir, '..', 'references')`. This means: (1) the standalone must stay nested inside `pen-tester/`, (2) pushing template changes to GitHub does NOT automatically update the standalone's output — the local files are what matter at runtime.

**`assessments.db` is gitignored and local only.** The SQLite database at `pen-tester/standalone/assessments.db` stores all scan history, false positives, decisions, and evidence hashes. Never commit it. `pen-tester/standalone/reports/` (generated reports) is also gitignored.

**Python Scripts directory is not on PATH.** `C:\Users\slagb\AppData\Local\Python\pythoncore-3.14-64\Scripts` is not in the user's PATH. Running `pip` from a standard PowerShell prompt may fail. Use the full path or `cd` to the standalone directory and use `python -m pip` instead.

**`_parse_control_section()` silently skips non-control sections** — two conditions cause a `###` section to be silently dropped: (1) the header doesn't match the control ID regex (`^[A-Z]{2,10}(?:-[A-Z]{2,10})?-\d{3,4}` or `^V-\d{5,6}`), OR (2) the header starts with one of the `skip_prefixes`: `('NOTE', 'TODO', 'LEGEND', 'TOTAL', 'TABLE')`. A section is also dropped if it has no `name`, `control name`, `statement`, or `control statement` field after parsing. When debugging a missing control in the assessment (present in `.md` but not appearing in results), check all three conditions.

**`Control` object fields** — what `controls.py` builds and scanners/engine.py consume via `ar.control.X`:

| Field | Type | Default | Notes |
|---|---|---|---|
| `control_id` | str | — | required; FAMILY-NNN format |
| `name` | str | — | required; human-readable control name |
| `family` | str | — | required; e.g. AUTH, CRYPTO, AGENT |
| `library` | str | — | required; `website_agent` / `api` / `code_review` / `interconnected` / `stig` |
| `cia` | str | `""` | primary CIA triad impact |
| `severity` | str | `"MEDIUM"` | `CRITICAL` / `HIGH` / `MEDIUM` / `LOW` / `INFORMATIONAL` |
| `statement` | str | `""` | control statement |
| `test_procedure` | str | `""` | what to test (from Test: field in .md) |
| `review_procedure` | str | `""` | test + all non-`_known` sub-fields concatenated |
| `fix_text` | str | `""` | remediation text |
| `tier` | str | `"review_required"` | computed by `classify_control()` — not read from .md |
| `frameworks` | list | `[]` | list of framework reference strings |
| `cwe` | str | `""` | CWE reference |
| `languages` | str | `"ALL"` | code-review only; drives `filterReviewSteps()` |
| `sources` | str | `""` | source references |
| `vuln_id` | str | `""` | STIG-specific |
| `rule_id` | str | `""` | STIG-specific |
| `srg_ref` | str | `""` | STIG-specific |
| `ccis` | list | `[]` | STIG-specific CCIs |
| `check_content` | str | `""` | STIG-specific check content |

**`detect_target()` in `detector.py` returns a dict, not a string.** The function signature is `detect_target(user_input: str) -> dict`. The returned dict has keys: `type`, `label`, `icon`, `control_sets` (list), `description`. Valid `type` values: `website`, `api`, `code`, `agent`, `stig`, `os`, `unknown`. The `control_sets` value maps to the library key in `CONTROL_LIBRARIES` — both `"website"` and `"agent"` target types return `control_sets: ["website_agent"]` and share the same control library. This is why both assessment types use the same 67-control set.

Detection priority (checked in order): (1) OS scan keywords (`localhost`, `127.0.0.1`, `::1`, `this machine`, `local machine`, `this host`) → `os`; (2) URL matching `^https?://` → `website`; (3) STIG text pattern (`xccdf`, `stig*.xml` regex) → `stig`; (4) Agent text pattern (`SKILL.md`, `.gpt`, `copilot`, `langchain`, `crewai`, `autogen`, `mcp`, `bedrock`, `vertex`) → `agent`; (5) existing file path by extension (code extensions → `code`, `.yaml/.yml/.json` → `api`, `.xml` with xccdf/Benchmark content → `stig`, `.md` with SKILL in name → `agent`); (6) extension alone on non-existent path; (7) text contains `swagger/openapi/api-spec/postman` → `api`; (8) fallback → `unknown`. `detect_languages(paths)` is defined in `detector.py` at line 122 but is **never called** anywhere in the codebase — it is dead code and should be removed.

**`detect_target()` detection priority** (verified against `detector.py`):
1. `text.lower() in OS_SCAN_KEYWORDS` → `"os"`. Exact membership test against `{'localhost', '127.0.0.1', '::1', 'this machine', 'local machine', 'this host'}`. No prefix/suffix — must be exactly one of these strings.
2. `WEBSITE_PATTERN.match(text)` → `"website"`. Matches `http://` or `https://` prefix (case-insensitive).
3. `STIG_PATTERNS.search(text)` → `"stig"`. Matches "xccdf" or "stig*.xml" ANYWHERE in string. Runs BEFORE agent check.
4. `AGENT_PATTERNS.search(text)` → `"agent"`. Matches `SKILL.md`, `.gpt`, `copilot`, `langchain`, `crewai`, `autogen`, `mcp`, `bedrock`, `vertex` ANYWHERE in string. Warning: "mcp" in any path component triggers agent detection (e.g., a file at `C:/projects/mcp-server/config.json` would be wrongly detected as agent).
5. `os.path.exists(text)` → file/directory exists: check extension → `code` (if code ext), `api` (if .yaml/.yml/.json), `stig` (if .xml AND file reads as XCCDF), `agent` (if .md AND "SKILL" in basename). `.json` files matching API extension spec are detected as API even if not an OpenAPI spec.
6. Extension-only fallback (file not required to exist): `.py/.js/etc.` → `"code"`, `.yaml/.yml/.json` → `"api"`.
7. Keyword fallback: 'swagger', 'openapi', 'api-spec', 'postman' in text → `"api"`.
8. Default: `"unknown"` → `main.py` converts to `"website"` in `_start_assessment()`.

`extract_hostname(target)` uses `re.match(r'https?://([^/:]+)', target)` — works for URLs only; returns the full target string unchanged for non-URL targets (file paths, local machine, etc.).

**`SystemsDB.get_or_create()` keying** — the full target string (e.g. `https://example.com/api/v1`) is the `UNIQUE` key in `systems.target`. `extract_hostname()` extracts just the hostname (e.g. `example.com`) and uses it as `display_name`. Two different URLs on the same host are two separate system records. For non-URL targets (code paths, STIG files, local machine), the full target string serves as both key and display name. The `system_id` returned is what ties all scans and decisions for that target together.

**`db.py` connection setup** (`get_connection()`, lines 21–26): `sqlite3.connect()` → `conn.row_factory = sqlite3.Row` (rows accessible as dicts) → `PRAGMA journal_mode=WAL` → `PRAGMA foreign_keys=ON`. All DB calls go through this function so every connection gets WAL mode and FK enforcement. WAL mode allows concurrent reads while a write is in progress — relevant if debugging "database locked" errors.

**`assessments.db` has six tables** — exact schema in `db.py` lines 32–114:
- `systems` — one row per unique target string; `UNIQUE(target)`; fields: `id`, `target`, `target_type`, `display_name`, `first_scanned`, `last_scanned`, `scan_count`
- `scans` — one row per scan run; FK to `systems.id`; fields: `id`, `system_id`, `started_at`, `completed_at`, `controls_tested`, `findings_count`, `compliant_count`, `control_sets` (JSON), `framework_filter`, `report_path`
- `decisions` — per-control triage decisions; `UNIQUE(system_id, control_id)`; fields: `id`, `system_id`, `control_id`, `scan_id`, `tier`, `decision`, `evidence_hash`, `notes`, `decided_at`, `decided_by`
- `false_positives` — FP suppression records; `UNIQUE(system_id, control_id)`; fields: `id`, `system_id`, `control_id`, `justification`, `evidence_hash`, `created_at`, `last_validated`, `is_active`
- `imported_stigs` — STIG import records; `UNIQUE(stig_id)`; fields: `id`, `stig_id`, `title`, `version`, `release_info`, `rule_count`, `file_path`, `imported_at`, `controls_md_path`
- `findings` — per-control scan results; FK to `scans.id`; mirrors `AssessmentResult` fields: `scan_id`, `control_id`, `tier`, `status`, `severity`, `evidence`, `confidence`, `cvss_score`, `cvss_vector`, `reachability`, `remediation`, `is_false_positive`

The `decisions` table is designed to be the carryforward source — `DecisionsDB.get_prior(system_id, control_id)` returns the prior decision for a target+control pair, which `engine.py` loads into `ar.prior_decision` during `load_controls()`. The decisions table stores **one record per target+control pair** (UNIQUE constraint); `DecisionsDB.save()` uses INSERT with ON CONFLICT REPLACE. **However, `DecisionsDB.save()` is never called from the current GUI** — only inside `apply_review_decision()` and `apply_manual_decision()`, which are never invoked from `main.py`. The `decisions` table is always empty; `get_prior()` always returns None; `ar.prior_decision` is always None. Similarly, `FalsePositivesDB.add()` is only called inside `apply_review_decision()` — also never called from `main.py`. The `false_positives` table is also always empty. `FalsePositivesDB.get_active(system_id)` IS called from `load_controls()`, but returns `[]` because the table is empty. The FP-check code in `run_automatic_tier()` (checking `self.false_positives`) always skips. **The only carryforward mechanism that actually works is report-based** (`prior_report_data` loaded from a prior HTML report file). DB decision/FP carryforward is non-functional end-to-end. The `false_positives` table upsert semantics (`add()` re-activates deactivated records; `remove()` sets `is_active=0`) are correct but never exercised from the GUI.

`evidence_hash(evidence_text)` in `db.py` computes `sha256(text).hexdigest()[:16]` — a 16-character hex prefix. This is what's stored in `decisions.evidence_hash` and `false_positives.evidence_hash`, and compared on reassessment to detect evidence changes (FP re-evaluation trigger).

**`pen-tester/references/os-software-controls.md` exists** — this is the OS & Software assessment control library, used only by the Standalone app. It was not mentioned in the four control libraries listed in README.md's structure section but it is present on disk.

**`pen-tester/tools/stig_parser.py` is the STIG XML parser utility.** It is tracked in Multi-Modal-Scanner under `pen-tester/tools/` and dynamically imported at runtime by the Standalone via `sys.path.insert` in `main.py`. It is not in the standalone's own directory.

**Development phases: 9 of 10 complete.** The original 10-phase plan: (1) project setup, (2) controls engine, (3) scanner framework, (4) website scanners, (5) code scanners, (6) API scanners, (7) agent scanners, (8) SQLite persistence, (9) PyQt6 GUI, (10) reporting & packaging. Phases 1–9 are complete. Phase 10's reporting component (HTML report generation, in-app triage, save/load) is done. Only the packaging component (PyInstaller bundling into a distributable `.exe`) remains.

**Evidence confidence scoring thresholds (supplement section 2):**
- \>70% confidence → "Likely non-compliant" (red label)
- 50–70% → "Uncertain — review evidence" (amber label)
- <50% → "Insufficient data" (gray label)

**`package.json`, `package-lock.json` at root are safe to delete.** They were created when the `docx` npm package was used to generate `Project_Handoff_Document.docx`. They have no relationship to the scanner project and are not project dependencies.

**The app actually runs — confirmed by user.** The user successfully launched `python main.py` on their Windows machine, navigated through the scan to the review screen, and observed the bugs live (phantom OWASP control, empty evidence). The app is not theoretical. Basic launch → scan → review flow is working. The "phantom OWASP control" was Bug 1 — framework field keys like `owasp` and `nist-800` were not in `_known`, so they appeared as spurious review procedure steps. Bug 1 is now fixed.

**`manual_confirmation` evidence is engine-generated, not scanner-generated.** No scanner is ever invoked for manual_confirmation controls. `run_automatic_tier()` builds structured evidence for each manual item directly: control name + requirement + numbered test procedure steps (from `ctrl.test_procedure`, split on `.`) + "No automated scanner covers this control. Complete the steps above then record your determination." This mirrors the review_required fallback but is always applied (there's no "did a scanner cover this?" check for manual controls). The resulting evidence text is what the user sees in the triage interface as the checklist to work through.

**Triage currently happens in the browser, not in the PyQt6 GUI.** `main.py` never calls `apply_review_decision()` or `apply_manual_decision()`. After a scan, the HTML report is opened in the browser. The user triages controls (marking FP, accepting findings, adding notes) directly in the browser UI. `apply_review_decision()` and `apply_manual_decision()` are built infrastructure for a planned future in-app triage screen that doesn't exist yet.

**Complete triage save/load flow:**
1. **In-browser state**: Decisions are stored in a JS `decisions{}` dict in memory. Notes in a `notes{}` dict. The `ls` wrapper (safe `localStorage` wrapper that silently no-ops if blocked by browser security/private mode) also persists decisions and notes to localStorage, namespaced by `REPORT_ID` (`lsKey = 'sat_' + REPORT_ID + '_' + controlId`).
2. **State seeding on load**: On report open, `decisions{}` is seeded from: (a) CONTROLS JSON — controls with `mitigation === 'YES'` are pre-marked as FALSE_POSITIVE, and (b) localStorage overrides for this REPORT_ID. **localStorage wins over CONTROLS JSON** — so live edits from a prior browser session are preserved even when loading the same HTML file again.
3. **"Save updated report" button** (id=`saveReport`): Bakes current `decisions` and `notes` back into a copy of CONTROLS JSON, temporarily replaces `sat-controls-data` textContent, serializes `document.documentElement.outerHTML`, then triggers a browser download. **Triage is NOT auto-saved** — the user must click this button for decisions to persist in a downloadable file.
4. **Downloaded file naming**: `{original_report_name}_{YYYY-MM-DD_HH-MM}_saved.html`. The downloaded file is a complete self-contained HTML with all decisions baked into `sat-controls-data`.
5. **Loading the saved report**: User loads the downloaded file via "Load previous report" in the PyQt6 GUI. `extract_prior_data_from_report()` reads `sat-controls-data`, returns FP/note state as `prior_report_data`, which is passed to `AssessmentEngine` on the next scan.

**`REPORT_ID`** is `str(uuid.uuid4())[:8]` generated fresh in `reporter.py` on each call to `generate_html_report()` (line 226). Each scan produces a new REPORT_ID — this namespaces localStorage so different reports don't share triage state in the same browser.

**NEEDS_REVIEW controls don't appear in any summary subcount.** After `run_automatic_tier()` completes but before triage, the status distribution is:
- Auto-tier controls: COMPLIANT, NON_COMPLIANT, NEEDS_REVIEW, or FALSE_POSITIVE (if from prior report). Auto-tier controls with no scanner match always get NEEDS_REVIEW (family-based evidence if available, otherwise generic fallback message).
- Review-tier controls: **NOT_TESTED** is the status for all original `review_required` controls — both with and without scanner coverage. The review loop (`run_automatic_tier()` lines 244–327) **NEVER sets `ar.status`** in any branch: direct match, family-based evidence, or no-evidence checklist. `ar.status` stays at the dataclass default (`NOT_TESTED`). The only non-NOT_TESTED exceptions are: NEEDS_REVIEW for controls **promoted** from auto-tier (status was set at engine.py line 174 before the `continue` that moved them into `review_items`, so they arrive pre-set); FALSE_POSITIVE (from prior report carryforward). There is no review-tier path that produces COMPLIANT or NON_COMPLIANT before human triage.
- Manual-tier controls: NOT_TESTED (dataclass default; never changed since apply_manual_decision is never called)

**Key clarification on review-tier scanner evidence:** A `review_required` control with a direct scanner match (e.g., INPUT-005 matched by `InputValidationScanner` returning NON_COMPLIANT) appears in the report as **NOT_TESTED with scanner evidence text populated**. The engine correctly copies the evidence but intentionally withholds the status judgment — human triage is required before status resolves. "Scanner directly matched" does NOT produce COMPLIANT or NON_COMPLIANT for review-tier controls.

`get_summary()` counts: `compliant` (status==COMPLIANT), `non_compliant` (NON_COMPLIANT), `not_tested` (status==NOT_TESTED), `not_applicable` (NOT_APPLICABLE), `false_positive` (is_false_positive). **NEEDS_REVIEW and ERROR statuses are NOT counted in any subcount.** NOT_TESTED IS counted in the `not_tested` subcount. The sum of subcounts falls short of `total` only by the number of NEEDS_REVIEW (and ERROR) controls — controls that are NOT_TESTED do count. The report header `{{TOTAL_CONTROLS}}` and `{{NON_COMPLIANT_COUNT}}` reflect this — controls with NEEDS_REVIEW status aren't shown in the header stats but NOT_TESTED controls are (via implication: total minus compliant minus non_compliant minus etc.).

**`_generate_standalone_html(engine, findings_data, summary)` is a fallback** for non-STIG reports when the template file is missing from `pen-tester/assets/`. Different from `_generate_stig_fallback_html()`. Both fallbacks produce minimal HTML tables with no JavaScript interactivity.

**User triage decision strings** — exact values the triage UI is designed to pass to `apply_review_decision()` and `apply_manual_decision()` (for reference when building in-app triage; these methods are not currently called from the GUI). A new session implementing in-app triage must use these exact lowercase strings:

| Tier | Decision string | Resulting `status` |
|---|---|---|
| `review_required` | `'false_positive'` | `FALSE_POSITIVE` + `is_false_positive = True` + saved to `FalsePositivesDB` |
| `review_required` | `'accept'` | `NON_COMPLIANT` (user confirms finding is real) |
| `review_required` | `'compliant'` | `COMPLIANT` |
| `review_required` | `'na'` | `NOT_APPLICABLE` |
| `manual_confirmation` | `'fail'` | `NON_COMPLIANT` |
| `manual_confirmation` | `'pass'` | `COMPLIANT` |
| `manual_confirmation` | `'na'` | `NOT_APPLICABLE` |

`automatic_confirmation` controls have no triage decision — their status is set by the scanner result and is final. `apply_all_prior_manual()` is defined to auto-apply prior `decisions` DB entries to manual tier items — but it is NOT called by `main.py`, and even if it were, the `decisions` table is always empty because `DecisionsDB.save()` is never called from the GUI. All three apply_* methods (`apply_review_decision`, `apply_manual_decision`, `apply_all_prior_manual`) are non-operational infrastructure for a future in-app triage screen (see Open Questions 9, 11). `ar.prior_decision` is always None.

**Reports save to `pen-tester/standalone/reports/`** (created automatically; gitignored). Filename format: `{type_prefix}_{safe_target}_{timestamp}.{ext}` — e.g. `website_example.com_2026-06-12 02.30pm.html`. The `type_prefix` comes from a dict in `_write_reports()`: `website`, `api`, `code-review`, `agent`, `stig`, `assessment` (fallback). CSV is **always** generated regardless of the user's format selection — `generate_csv_report()` runs unconditionally after the primary format. Reports open in the user's default browser via `webbrowser.open('file:///' + path)`.

**Multi-target combined report mode** — when the user selects "Combined report" and there are multiple targets, `main.py` merges all four result lists from each subsequent engine into the primary engine: `primary.all_results.extend(eng.all_results)`, `primary.auto_results.extend(eng.auto_results)`, `primary.review_items.extend(eng.review_items)`, `primary.manual_items.extend(eng.manual_items)`. `primary.target` is set to all targets joined with `", "`. This is a **flat merge with no deduplication** — if two targets both have results for, say, AUTH-001, both appear as separate entries in the combined report. The combined report is one report for multiple targets, not a deduplicated union. In separate-report mode, each target produces its own report file.

**Combined mode stat card double-counting in `_show_results()`.** After the combined merge, `_show_results()` still iterates ALL `self.completed_engines` and sums counts across each engine's `.all_results`. But the primary engine's `all_results` was already extended to include every secondary engine's items — so secondary engines' results are counted twice (once from primary's extended list, once from their own list). This means all stat card numbers (total, critical, high, compliant, suppressed) are inflated in combined mode: specifically, for N engines total, items from engines 2..N are double-counted. The report content itself is correct (produced from the merged primary engine); only the Results screen stat cards are affected by this double-count. In separate-report mode, each engine is counted once so no double-counting occurs. **Acceptable limitation; low priority since combined mode is rarely used.** The fix is straightforward: in `_show_results()`, use `self.completed_engines[0].get_summary()` (the merged primary) instead of summing across all `completed_engines`.

**Multi-target scans are sequential, not parallel.** `_start_assessment()` builds a `pending_configs` queue; `_run_next_target()` pops and scans one target at a time. Each target's `ScanWorker` must complete before the next starts (`_on_target_done()` → `_run_next_target()`). All targets report to `completed_engines` before `_all_done()` writes reports.

**`prior_report_data` is applied to ALL targets in a multi-target scan.** The same prior report dict (loaded once via "Load previous report") is passed to every `AssessmentEngine` instance (line ~902: `prior_report_data=self.prior_report_data`). If the prior report was for Target A and the scan includes Target A + Target B, Target B also gets the FP carryforward from Target A's prior report — even if the FPs don't apply. This is a known behavior, not a bug.

**What the user will likely do in the next session:** (1) run `python main.py` and verify Code Review scan shows Compliant results (Round 25 fix), (2) test multi-language directory scan with `test_targets\code_sample\vulnbank_backend` (Round 26 addition — Python/Java/Go/PHP), (3) test STIG import end-to-end, (4) test other scan types (API, Agent, OS), (5) then move to code cleanup batch or PyInstaller packaging.

**The Claude Code skill supports 6 assessment types; the Standalone supports 7.** `pen-tester/SKILL.md` defines: Website, AI Agent, Source Code, API, STIG, and Connected Systems (Interconnected). OS & Software assessment is **Standalone-only** — it requires local machine access that Claude Code cannot provide. Do not try to add OS assessment to the skill.

**`pen-tester.skill`** (21 KB, zip archive at project root) — the packaged Claude Code skill. Installable in Claude Code. May be behind current `pen-tester/SKILL.md` since it was last packaged in April 2026. Not a source file — it's a build artifact. If SKILL.md has changed since April, this needs to be rebuilt.

**`pen-tester-controls-catalogue.xlsx`** (40 KB, April 2026) — a spreadsheet catalogue of controls. Likely a reference/planning artifact from early development. Not used by the scanner at runtime. Status unknown — may be outdated relative to current `.md` libraries.

**`interactive-remediation-report.html`** — a sample interactive report for "VulnBank + Data Researcher Skill". Demo/reference artifact from an earlier session. Not a source file.

**`pen-tester-self-assessment.html/.md`** (April 13, 2026) — the pen-tester skill assessed against itself. Historical artifact. References 60 controls across 11 families (pre-AGENT rename, pre-67 count). Do not treat these as current state.

**`pen-tester-vs-vanilla-comparison.html`** — comparison of pen-tester vs vanilla AI assessment. Historical artifact from April 2026.

**`security-assessment-report.html/.md`** at root — gitignored generated outputs from an April 2026 scan. Not source files. Safe to delete.

**`.~lock.pen-tester-controls-catalogue.xlsx#`** at root — stale LibreOffice lock file. Safe to delete.

**`test-targets/` at project root** contains `sample-skill/SKILL.md` and `sample-website/index.html` — test inputs for the Claude Code skill. Tracked in Multi-Modal-Scanner. Separate from `pen-tester/standalone/test_targets/` which is gitignored and local only.

**`pen-tester/standalone/gui/`** contains only `__init__.py`. The entire GUI is implemented in `main.py` directly (PyQt6 classes defined inline). There is no separate GUI module structure despite the directory existing.

**The planned 6-screen GUI is only 3 screens implemented.** `HANDOFF_SUPPLEMENT.md` section 1 documents a 6-screen GUI design (Main window, STIG import, Progress, Review required, Manual confirmation, Results). Only 3 of these 6 screens are implemented in the current `main.py`:
- Screen 0: Home (target input, prior report load, STIG import, format options)
- Screen 1: Progress (scanner feed, live findings feed showing `[SEV] control_id — evidence[:80]` for each NON_COMPLIANT result, progress bar: ≤90% during scanning via `min(int(count / max(10, count+2) * 90), 90)` formula, jumps to 95% when each target completes (`_on_target_done()`), 100% when all targets done and reports generated (`_all_done()`))
- Screen 2: Results (banner with targets/controls/findings counts; 5 stat cards: Controls tested, Critical, High, Compliant, Suppressed; report file links with Open buttons). Note: no stat card for Medium, Low, NEEDS_REVIEW, or NOT_APPLICABLE.

Screens 4 (Review required — split panel with action buttons: Accept finding/Compliant/N/A/False positive) and 5 (Manual confirmation — per-item radio button checklist) are the in-app triage screens that were never built. These are the screens that would call `apply_review_decision()` and `apply_manual_decision()`. The supplement's Screen 1 mockup also included toolbar buttons (History, Systems, Settings, Help), a control-sets multi-select QListWidget, a framework dropdown in the GUI, and a prior scan banner — none of these appear in the current implementation. Control sets are auto-determined from target type; framework selection is client-side in reports; history/systems/settings are dead DB read methods.

**Tier distribution across all ~195 controls** (from design-time analysis in HANDOFF_SUPPLEMENT.md section 2, approximate):
- Automatic confirmation: ~125 controls (entire families + specific IDs with reliable scanner coverage)
- Review required: ~80 controls (scanner produces evidence, but human interpretation needed)
- Manual confirmation: ~22 controls (organizational knowledge required — policy, architecture, vendor docs)

**`pen-tester/standalone/make_test_reports.py`** — developer utility to generate 6 static test HTML reports using hardcoded sample data. Does NOT use the engine/scanner stack. Run from `pen-tester/standalone/`. Outputs to `pen-tester/test-reports/`: `test-report-website.html`, `test-report-api.html`, `test-report-code-review.html`, `test-report-interconnected.html`, `test-report-os.html`, `test-report-fps.html` (website with AUTH-001 pre-marked as FALSE_POSITIVE). OS type uses `report-template.html` (same as website — no separate OS HTML template). STIG is NOT covered by this utility. The JSON control objects in the hardcoded data match the same schema as `generate_html_report()` produces, so test reports behave identically to real scan outputs in the browser.

**`pen-tester/test-reports/`** contains pre-generated test report HTML files for each assessment type. Tracked in Multi-Modal-Scanner. These are reference outputs, not generated by running the standalone app.

**HANDOFF_SUPPLEMENT.md section 7 is stale and will mislead.** It still says to upload handoff files, references `pen-test-triage-update/` (being deleted), and says "6 bugs" to fix. Do not follow section 7. Use `HOW_TO_START_NEW_SESSION.txt` and `CLAUDE.md` instead — both have been updated this session.

**HANDOFF_SUPPLEMENT.md section 9 checksums are stale.** They reference `cross-system-controls.md` (renamed to `interconnected-controls.md`) and reflect June 2, 2026 line counts — before this session's changes to the report templates and controls.py. Do not use them for integrity verification without re-running the checksums.

**Control library counts — one source of truth:**

| Library file | Assessment types | Controls | Families |
|---|---|---|---|
| `controls-library.md` | Website, AI Agent | 67 | 13 |
| `api-controls-library.md` | API | 53 | 17 |
| `code-review-controls.md` | Code Review | 51 | 12 |
| `interconnected-controls.md` | Connected Systems | 27 | 9 (CHAIN, TRUST, RESCORE, DATAFLOW, SESSION, CRYPTO, CONFIG, INCIDENT, SUPPLY) |
| `os-software-controls.md` | OS & Software | 12 | — |
| STIG | STIG Compliance | dynamic (imported from XCCDF) | — |

Control counts are confirmed by `###` header audit (all counts match `CONTROL_LIBRARIES`): `controls-library.md` has 73 `###` headers total — 6 are non-control reference appendices (OWASP LLM 2025, NIST AI RMF 1.0, Google SAIF, ISO/IEC 42001, CSA AI, Platform Reference) = **67 actual controls**. `api-controls-library.md` has 54 headers — 1 appendix (OWASP API Top 10 Quick Reference) = **53 controls**. `code-review-controls.md` has 54 headers — 3 section headers (Control Domains, Framework References, Language Applicability) = **51 controls**. `interconnected-controls.md` and `os-software-controls.md` header counts match directly (27 and 12). Open Question 6 is now resolved.

**Connected Systems works differently in the Skill vs the Standalone — these are not the same workflow.**

In the **Claude Code skill version**: requires two completed prior assessment HTML reports as inputs. AI analysis correlates findings across both reports to detect multi-step attack chains spanning connected systems, with CVSS re-scoring and reachability promotion. Does not scan a new target.

In the **Standalone app**: there is no separate "Connected Systems" target type and no requirement for prior assessments. Instead, when the user enters more than one target, `main.py` automatically appends `'interconnected'` to `selected_sets`. This adds the 27 interconnected controls to the scan alongside the primary library. The interconnected controls run as additional `review_required` / `manual_confirmation` items — they don't correlate DB records or re-score CVSS. The `reachability` field on `ScanResult` (default `"DIRECT"`) is stored but the standalone has no logic that re-scores CVSS based on it. Connected Systems in the standalone is effectively "extra controls assessed during a multi-target scan."

**All 12 OS controls — IDs, families, tier assignments, and scanner coverage (verified against `os-software-controls.md` and `controls.py`):**

| Control ID | Name | Family | Tier | Scanner covers? |
|---|---|---|---|---|
| PATCH-001 | OS security updates current | PATCH | auto | ✓ via `os_scanner.py` |
| PATCH-002 | Vulnerability patch SLA compliance | PATCH | manual | ✗ — always manual |
| PATCH-003 | Installed software CVE exposure | PATCH | auto | ✓ via NVD lookup |
| EOL-001 | OS end-of-life status | EOL | auto | ✓ via `_OS_EOL` dict |
| EOL-002 | Installed software end-of-life status | EOL | review | ✗ — no scanner |
| SOFTINV-001 | Software inventory documented | SOFTINV | manual | ✗ — always manual |
| SOFTINV-002 | Unauthorized software absent | SOFTINV | review | ✗ — no scanner |
| SVCCONFIG-001 | Services run as least-privilege | SVCCONFIG | review | ✗ — no scanner |
| SVCCONFIG-002 | Unnecessary/insecure services disabled | SVCCONFIG | auto | ✓ via `ServicesScanner` class |
| SVCEXPOSE-001 | Listening network services minimized | SVCEXPOSE | auto | ✓ via `ServicesScanner` class |
| SVCEXPOSE-002 | Remote management services secured | SVCEXPOSE | review | ✗ — no scanner |
| OSAUDIT-001 | OS audit logging enabled | OSAUDIT | review | ✗ — no scanner |

5 of 12 auto, 2 manual, 5 review_required (no scanner). **`os-software-controls.md` header bug (unfixed):** the file header still says "12 controls across 5 families" but there are actually 6 families (PATCH, EOL, SOFTINV, SVCCONFIG, SVCEXPOSE, OSAUDIT — the OSAUDIT family is present in the summary table but missed in the header count). Needs a one-line correction.

**`os_scanner.py` internal structure — 3 scanner classes, not functions.** `scan_os_target()` instantiates and runs exactly three classes in order: `OSVersionScanner` (produces PATCH-001 and EOL-001), `SoftwareCVEScanner` (produces PATCH-003), and `ServicesScanner` (produces SVCCONFIG-002 and SVCEXPOSE-001). There are no `_check_services()` or `_check_ports()` standalone functions — this logic lives inside `ServicesScanner.scan()`. Each scanner is wrapped in a try/except so one scanner crash doesn't abort the others. Scanner `.name` attributes (written to `ScanResult.scanner` and passed to `progress_callback`): `OSVersionScanner.name = "os-version"`, `SoftwareCVEScanner.name = "software-cve"`, `ServicesScanner.name = "services"`. The `target` parameter to `scan_os_target()` is used as a label only — the scan always runs against the local machine regardless of what string is passed.

**`SoftwareCVEScanner` only checks `PRIORITY_KEYWORDS` software against NVD — not all installed packages.** The scanner enumerates all installed software (Windows: PowerShell registry query of HKLM `Uninstall` keys; Linux: `dpkg-query` first, `rpm` fallback), then filters to packages whose name matches any keyword from `PRIORITY_KEYWORDS` (38 keywords covering browsers, runtimes, crypto/SSH, web servers, databases, productivity, comms, devops tools, security tools, and common utilities). Only matching packages are queried against NVD. Non-priority software (e.g., a custom in-house application) is never queried. The NVD keyword is `name[:50]` — the software name truncated to 50 chars, with version omitted from the query string. CVSS threshold for a finding: ≥ 7.0; the finding is tagged CRITICAL if max score ≥ 9.0. Up to 5 CVEs are shown in evidence (`_cve_summary()` max_items=5), descriptions truncated to 120 chars.

**`EOL-001` has three outcome paths, not just pass/fail.** When OS is found in `_OS_EOL` and past its date → NON_COMPLIANT. When found and within support but < 6 months remaining → **NEEDS_REVIEW** (triggers auto→review promotion). When found and ≥ 6 months remaining → COMPLIANT. When NOT found in `_OS_EOL` → NEEDS_REVIEW. Critical gap: **Windows 11 is not in the `_OS_EOL` dict** — any Windows 11 host will always produce NEEDS_REVIEW for EOL-001. Windows 10 version-specific check uses `display_version` from the Windows registry (e.g., `win10-22h2` has EOL date 2025-10-14 — a Windows 10 22H2 host scanned after that date will show NON_COMPLIANT). The Windows 10 `win10-22h2` entry in `_OS_EOL` is past end-of-life as of late 2025.

**`_EXPECTED_PORTS`** (ports that do NOT trigger SVCEXPOSE-001 NON_COMPLIANT/NEEDS_REVIEW): `{22, 80, 443, 3389, 8080, 8443, 8888, 53, 135, 139, 445, 5985, 5986}`. Any listening port outside this set triggers SVCEXPOSE-001 NEEDS_REVIEW (not outright NON_COMPLIANT — requires manual confirmation of business justification). The scanner uses `netstat -ano` on Windows and `ss -tlnp` (falling back to `netstat -tlnp`) on Linux.

**`_RISKY_SERVICES_WIN` includes WinRM, but its ports are in `_EXPECTED_PORTS`.** WinRM (`WinRM` service name) is in the risky services list for SVCCONFIG-002 — if the WinRM service is running, SVCCONFIG-002 fires NON_COMPLIANT. However, ports 5985 and 5986 (WinRM's ports) are in `_EXPECTED_PORTS`, so SVCEXPOSE-001 will NOT flag them as unexpected. Both controls can apply to the same WinRM configuration, but via different mechanisms.

**Full `_RISKY_SERVICES_WIN` service list** (verified from source — these are the 8 Windows service names that trigger SVCCONFIG-002 NON_COMPLIANT):
`TlntSvr` (Telnet server), `FTPSVC` (IIS FTP), `tftpd32` (TFTP), `SNMP` (v1/v2 community strings), `RemoteRegistry` (allows remote registry edits), `Spooler` (Print Spooler — CVE-2021-34527 PrintNightmare), `RasMan` (Remote Access Service), `WinRM` (Windows Remote Management).

**Full `_RISKY_SERVICES_LINUX` service list** (verified from source — these are the Linux daemon names checked via `systemctl` or `service` enumeration):
`telnetd` (Telnet daemon), `vsftpd` (FTP), `proftpd` (ProFTPD), `tftpd` (TFTP), `rshd` (RSH — cleartext), `rexecd` (Rexec — cleartext), `snmpd` (SNMP — check v1/v2), `xinetd` (inetd super-server). Service detection on Linux uses `systemctl list-units --type=service --state=running --plain --no-legend`. If `systemctl` fails (non-systemd systems, or any exception), returns an empty list — no fallback. This means risky service detection is silently skipped on non-systemd Linux.

**`_OS_EOL` dict OS coverage summary** (verified from source): Windows 7/8/8.1; Windows 10 (version-dependent via display_version: 1909, 20H2, 21H1, 21H2, 22H2); Windows 11 (version-dependent via display_version: 21H2, 22H2, 23H2, 24H2, 25H2, 26H1 — added Round 25, Enterprise/Education dates); Windows Server 2008/2012/2016/2019/2022; Ubuntu 16.04–24.04; Debian 9–12; CentOS 6/7/8; RHEL 7/8; macOS 10.15/11/12. **Not in dict**: Windows Server 2025, macOS 13 (Ventura)/14 (Sonoma)/15 (Sequoia) — produce NEEDS_REVIEW. As of June 2026, `win11-22h2` (EOL 2025-10-14), `win11-23h2` (EOL 2026-11-10 — within 6 months, so NEEDS_REVIEW), `win10-22h2` (EOL 2025-10-14), and `ubuntu 20.04` (EOL 2025-04-30) will trigger findings on hosts running those versions.

**`PATCH-001` Windows update check has a 45-second timeout.** `_get_pending_windows_updates()` runs a PowerShell COM object query (`New-Object -ComObject Microsoft.Update.Session`) with `timeout=45`. If the query fails or returns `'ERROR'`, PATCH-001 returns NEEDS_REVIEW (not NON_COMPLIANT). This is the longest-running step in an OS scan and may require elevation to get accurate results.

**OS scanner ScanResult confidence and reachability values (verified against source):**

PATCH-001 exact outcomes:
- NEEDS_REVIEW (query fails/error): severity='HIGH', confidence=0.3, no reachability
- COMPLIANT (pending=0): severity='CRITICAL', confidence=0.9, no reachability — severity='CRITICAL' on COMPLIANT is counterintuitive but reflects the severity of the control, not the finding
- NON_COMPLIANT (pending>0): severity='CRITICAL', confidence=0.95, cvss_score=7.8, cvss_vector='CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H', reachability='INDIRECT'

EOL-001 exact outcomes:
- NON_COMPLIANT (past EOL date): severity='CRITICAL', confidence=0.95, cvss_score=9.8, cvss_vector='CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H', reachability='DIRECT'
- NEEDS_REVIEW or COMPLIANT (within support): confidence=0.9, no reachability; severity='HIGH' if <12 months remaining, 'INFORMATIONAL' otherwise; status='NEEDS_REVIEW' if <6 months remaining, 'COMPLIANT' otherwise
- NEEDS_REVIEW (OS not in `_OS_EOL` dict): severity='MEDIUM', confidence=0.3

PATCH-003 exact outcomes:
- NON_COMPLIANT (CVEs found): severity='CRITICAL' if max_score >= 9.0, else 'HIGH'; confidence=0.75; reachability='INDIRECT'
- COMPLIANT (no CVEs ≥ 7.0, or no priority packages identified): severity='HIGH', confidence=0.6, no reachability
- No NEEDS_REVIEW path exists for PATCH-003 — unlike PATCH-001, NVD query failures silently produce empty CVE results, so a failed NVD query produces COMPLIANT with lower confidence rather than NEEDS_REVIEW

SVCCONFIG-002 exact outcomes:
- NON_COMPLIANT (risky services found): severity='HIGH', confidence=0.9, reachability='DIRECT'
- COMPLIANT (running services present, none risky): severity='HIGH', confidence=0.85, no reachability
- NEEDS_REVIEW (can't enumerate services): severity='HIGH', confidence=0.2

SVCEXPOSE-001 exact outcomes:
- NEEDS_REVIEW (unexpected ports present, i.e., ports outside `_EXPECTED_PORTS`): severity='MEDIUM', confidence=0.8, no reachability — unexpected ports produce NEEDS_REVIEW not NON_COMPLIANT; business justification required before flagging as violation
- COMPLIANT (all listening ports within `_EXPECTED_PORTS`): severity='MEDIUM', confidence=0.8, no reachability
- NEEDS_REVIEW (can't enumerate ports): severity='MEDIUM', confidence=0.1

**OS & Software scanner makes live HTTP requests to the NVD API.** `os_scanner.py` enumerates the local machine (OS version via `platform` module + `winreg` on Windows for detailed build info, installed software, running services, listening ports), then queries `https://services.nvd.nist.gov/rest/json/cves/2.0` to check installed software against the National Vulnerability Database for CVE exposure. Uses `urllib.request` (Python stdlib, NOT the `requests` library) — no extra dependency. NVD queries: `resultsPerPage=10` (max 10 CVEs per keyword), `_highest_cvss()` finds the max score across all returned CVEs. No API key is passed (always unauthenticated — the `api_key` parameter in `_nvd_query()` exists but is never supplied by callers). Rate limit: `_NVD_RATE_DELAY = 0.7` seconds between requests (~1.4 req/sec — conservative, well under the NVD limit of 5/sec). NVD query errors are silently caught and return `[]` — NVD unavailability produces no user-visible error, just empty CVE results. CVSS scores extracted in priority order: CVSSv3.1 > CVSSv3.0 > CVSSv2 (`_highest_cvss()` function). NVD queries use in-memory caching per scan run (`_NVD_CACHE` dict) — the same keyword won't hit the API twice in one scan. An internet connection is required for CVE lookups; local enumeration (OS version, software list, services, ports) runs offline. EOL date checking uses a hardcoded `_OS_EOL` dict in `os_scanner.py` — no network call. This is different from website (`scanners.py`) and API (`api_scanner.py`) scanners, which hit the **target** over the network. OS scanner hits NVD, not the target. Code review, STIG, and agent scanners are fully offline.

**False positive carryforward and evidence hashing — both non-functional from current GUI.** `db.py` keys decisions by target+control. On re-scan, the code checks `FalsePositivesDB.get_active()` for FP records — but since `FalsePositivesDB.add()` is never called from the GUI, the table is always empty; this check always returns `[]` and no FPs are auto-applied from the DB. Similarly, `DecisionsDB.get_prior()` is called but the table is always empty. The only carryforward that functions is report-based: loading a prior HTML report via "Load previous report" and having `prior_report_data` applied by `run_automatic_tier()`. `db.py` stores evidence hashes in both tables (for eventual use by `check_evidence_changed()`), but since no FP/decision records are ever written, hash comparison never fires in practice. The evidence-change warning badge UI is also not implemented (see Open Question 10).

**`Project_Handoff_Document.docx`** at root — the original Word-format handoff document from before June 12, 2026. Safe to delete. `PROJECT_HANDOFF.md` supersedes it entirely.

**`HANDOFF_SUPPLEMENT.md`** — keep for now. Sections 8 and 16 are inlined into this document; sections 7 and 9 are stale. Sections 1–6, 10–15 contain GUI specs, confidence thresholds, scanner architecture detail, and verified test procedures that may still be useful. Do not delete until confirmed redundant.

**Python module map — what each `.py` file does:**

| File | Entry point(s) | Purpose |
|------|----------------|---------|
| `main.py` | run directly | PyQt6 GUI — all UI classes defined inline here; `gui/` dir contains only `__init__.py` |
| `engine.py` | `AssessmentEngine` class | Orchestration — loads controls library, calls scanners, applies tier logic, builds `AssessmentResult` list |
| `detector.py` | `detect_target(user_input)` | Target type detection — reads input string and returns dict with type/label/icon/control_sets/description. Priority order: os → website → stig → agent → file-path → extension-fallback → keyword → unknown |
| `scanners.py` | `run_all_scanners(target, target_type)` | **Website scanner** — despite the generic name, handles website HTTP scanning only |
| `agent_scanner.py` | `scan_agent_config(filepath)` → imported as `scan_agent` | **AI Agent scanner** — static config analysis (parses SKILL.md, GPT configs, LangChain defs, MCP manifests); tests AGENT-001 through AGENT-011 controls; no live HTTP requests |
| `api_scanner.py` | `scan_spec(filepath)` → imported as `scan_api` | **API scanner — static analysis of OpenAPI/Swagger spec files** (YAML or JSON); does NOT make live HTTP requests; target must be a file path to the spec |
| `code_scanner.py` | `scan_target(target)` → imported as `scan_code`; routes to `scan_file()` or `scan_directory()` | Source code scanner — VULN_PATTERNS dict + LANG_EXTENSIONS map for language detection. Emits both NON_COMPLIANT (on pattern match) and COMPLIANT (for every checked control with no violation) via `_build_compliant_results()`. |
| `os_scanner.py` | `scan_os_target(target)` → imported as `scan_os` | OS & Software scanner — enumerates local machine OS version, installed software, running services; queries NVD API for CVEs |
| `controls.py` | `load_all_controls(selected_sets, stig_paths)` | Parses `.md` control libraries into Python objects; `_known` set gates what becomes `review_procedure` |
| `reporter.py` | `generate_html_report(engine, path)` and variants | Generates HTML reports from `AssessmentResult` list; finds templates via relative path to `../assets/` |
| `db.py` | DB class methods (static) | SQLite persistence — stores target systems, scan history, per-control decisions, false positives, evidence hashes; keys decisions by target+control for carryforward |
| `make_test_reports.py` | run directly | Dev utility to generate test HTML reports for every assessment type; not part of the app |

**Report output goes to `pen-tester/standalone/reports/` — NOT `pen-tester/test-reports/`.** `_all_done()` in `main.py` writes reports to `os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")` = `pen-tester/standalone/reports/`. This directory is gitignored (local only). `pen-tester/test-reports/` is a separate directory with pre-generated static test reports tracked in Multi-Modal-Scanner.

**`_abort_scan()` disconnects signals but does NOT terminate the scan thread.** If the user clicks "Cancel" during a scan, `_abort_scan()` disconnects `scan_worker.progress` and `scan_worker.finished` signals and navigates back to the home screen. The `ScanWorker` QThread continues running in the background — it just can't update the UI or trigger report generation anymore. This is safe for short-running scans. For OS scans (which hit NVD API and can take longer), the thread may run for a significant time after abort. **Accepted behavior for now.** The proper fix is a cooperative stop flag: add `self._stop_requested = False` to `ScanWorker.__init__()`, set it to `True` in `_abort_scan()` before disconnecting signals, and check it at appropriate points inside `ScanWorker.run()` (e.g., between scanner calls) to exit early. Not currently queued.

**`prior_report_data` persists across scan sessions within the same app launch.** `_reset_to_home()` clears `completed_engines`, `pending_configs`, and `_scanner_count`, then navigates to screen 0 — but it does NOT clear `self.prior_report_data`, and it does NOT clear `self.target_list` (the list of configured scan targets). If a user loads a prior report, scans, resets, and scans again without loading a new prior report, the old `prior_report_data` is still applied to the new scan. The same targets already added to `target_list` remain after reset — the user can start a new scan of the same targets immediately without re-entering them. To clear prior_report_data, the user must restart the app or load a new prior report (which replaces the dict).

**App initialization** (`main()` function, lines 1132–1138): `app.setStyle("Fusion")` (flat cross-platform look), `app.setFont(QFont("Segoe UI", 10))`. `MainWindow.setMinimumSize(860, 600)`. `StigImportDialog.setMinimumWidth(520)`. The Fusion style avoids platform-specific widget rendering differences between Windows 10/11.

**Two batch launchers in `pen-tester/standalone/`:**
- `launch.bat` — runs `python main.py` (uses whatever `python` is in PATH)
- `run_app.bat` — runs `"C:\Users\slagb\AppData\Local\Python\pythoncore-3.14-64\python.exe" main.py` (hardcoded to user's Python 3.14 install; use this if `python` is not on PATH)

`scanners.py` (`run_all_scanners`, `ScanResult`) is a **required** import in `engine.py` — if it fails, engine.py fails to load entirely. The four optional scanners (`code_scanner`, `api_scanner`, `agent_scanner`, `os_scanner`) are wrapped in try/except: if any fails to import, it is set to `None` and skipped in `run_automatic_tier()` (guarded by `if scan_code:`, `if scan_api:`, etc.). Missing optional dependency → scanner skipped → controls fall through to no-scanner fallback (review_required checklist + confidence 0.2).

**API assessment differs between skill and standalone.** In the **Claude Code skill** (`pen-tester/SKILL.md`), API assessment accepts OpenAPI/Swagger specs, live API endpoint URLs, and Postman collections — Claude reads and interprets them with AI. In the **Standalone**, `api_scanner.py` only accepts a file path to an OpenAPI/Swagger YAML/JSON spec. Live API URLs and Postman collections are not supported in the standalone. `detect_target()` routes `.yaml`/`.yml`/`.json` files with API-like content to `target_type = "api"`.

**`api_scanner.py` requires a file path, not a URL.** The API assessment target must be a path to an OpenAPI/Swagger spec file (`.yaml`, `.yml`, or `.json`). `scan_spec()` parses the spec statically — it detects BOLA patterns, missing auth requirements, mass assignment risks, debug endpoints, non-HTTPS server URLs, rate limiting gaps, and GraphQL risks by reading the spec structure. It makes no live HTTP requests. The `detector.py` routes `.yaml`/`.json` file inputs with API-like content to `target_type = "api"`. If a user enters a live API URL instead of a spec file, `scan_spec()` will fail to parse it.

**`api_scanner.py` control coverage — exact output from `scan_spec()` (verified against source):**

| Control ID | Status produced | Trigger condition |
|---|---|---|
| BOLA-001 | NON_COMPLIANT or COMPLIANT | Always — NON_COMPLIANT if integer path params found, else COMPLIANT |
| AUTH-001 | NON_COMPLIANT or COMPLIANT | Always — NON_COMPLIANT if any endpoint lacks security, else COMPLIANT |
| BOPLA-001 | NON_COMPLIANT only | Only if schema has writable sensitive fields (role, isadmin, balance, etc.) |
| RATE-001 | NEEDS_REVIEW | Always — rate limiting can't be verified from spec alone |
| FUNC-001 | NON_COMPLIANT only | Only if `/admin` endpoints found with no security |
| SSRF-001 | NON_COMPLIANT only | Only if URL/URI/callback/redirect params found |
| CONFIG-001 | NON_COMPLIANT only | Only if `/debug`, `/internal`, `/trace`, `/metrics`, `/actuator` paths found |
| CONFIG-002 | NEEDS_REVIEW | Always — API surface summary (endpoint count, methods, schemas, etc.) |
| CONFIG-003 | NON_COMPLIANT only | Only if `http://` server URLs found (non-HTTPS) |
| DATA-001 | NON_COMPLIANT only | Only if sensitive field names (password, ssn, credit_card, api_key, etc.) in schemas |
| WEBHOOK-001 | NEEDS_REVIEW only | Only if webhook/hook paths found |
| GRAPHQL-001 | NEEDS_REVIEW only | Only if graphql/graphiql paths found |
| INVENTORY-001 | NEEDS_REVIEW | Always — "are there undocumented endpoints?" is unanswerable from spec alone |

Important: AUTH-002 and AUTH-003 appear in `AUTO_IDS` for the API library but `api_scanner.py` produces **no result** for them. They get family-based evidence from AUTH-001 (confidence 0.5) — the report shows "No scanner maps directly to AUTH-002, but related AUTH controls were tested: [AUTH-001 result]" with status COMPLIANT (if AUTH-001 was COMPLIANT) or NEEDS_REVIEW. They stay in `auto_results` (not promoted to review_required). INVENTORY-001 is NOT in `AUTO_IDS` or `MANUAL_IDS` — it defaults to `review_required` tier; since its status is always NEEDS_REVIEW, it stays in `review_items`. The scanner produces 13 control results at most — the other ~40 API controls get no scanner result.

**`_scan_raw_spec()` — YAML-less fallback.** When `HAS_YAML = False` (pyyaml not installed) and the spec is YAML (not JSON), `parse_spec()` falls back to basic line-key extraction and sets `'_raw': content` in the spec dict. `scan_spec()` detects `'_raw' in spec and not spec.get('paths')` and calls `_scan_raw_spec()`. The fallback does keyword matching on lowercased raw text and produces results for only 6 control IDs: BOLA-001, AUTH-001, CONFIG-003, SSRF-001, CONFIG-001, DATA-001 — all at lower confidence (~0.6–0.7). No NEEDS_REVIEW results in fallback mode. The other ~47 API controls get no result when YAML parsing fails.

**`api_scanner.py` only fully supports OpenAPI 3.x, not Swagger 2.x.** `extract_schemas()` looks for `spec.get('components', {}).get('schemas', {})` — the OpenAPI 3.x location. Swagger 2.x specs use `spec.get('definitions', {})` instead. A Swagger 2.x `.yaml` file will parse successfully (if pyyaml is installed) but produce `schemas = {}` — meaning BOPLA-001 (mass assignment) and DATA-001 (sensitive fields) checks will find nothing and produce no results. BOLA-001 and AUTH-001 checks still work because they read `spec['paths']`, which exists in both versions. If a user provides a Swagger 2.x spec and gets no BOPLA-001 or DATA-001 findings, this is the reason.

**`api_scanner.py` has a PyYAML guard.** The module opens with `try: import yaml; HAS_YAML = True except ImportError: HAS_YAML = False`. If PyYAML is not installed and the spec file is YAML (not JSON), `parse_spec()` falls back to a very basic line-by-line key extraction that produces an incomplete `spec` dict. All subsequent scanner checks that look for structured spec data (endpoints, paths, security schemes) will return empty lists and produce minimal/inaccurate results. `pyyaml>=6.0` is in `requirements.txt` (Bug 4 was fixed), so this shouldn't be an issue in the standard setup — but is the root cause if API scanning returns empty results.

**`agent_scanner.py` is entirely keyword-based** — no LLM calls, no semantic analysis. It looks for words from `HIGH_RISK_TOOLS`, `MEDIUM_RISK_TOOLS`, `DEFENSIVE_KEYWORDS`, `DANGEROUS_INSTRUCTIONS`, and `CONFIRMATION_KEYWORDS` sets in the lowercased file text. Some AGENT controls are conditional — only a ScanResult is produced when the trigger condition fires (e.g., AGENT-003 only if database/file tools present; AGENT-004 only if `high_risk AND declared_purpose`). AGENT-001, AGENT-002, and AGENT-005 always produce a ScanResult. **All AGENT controls except AGENT-007/010 are `review_required` tier** — AGENT family is not in `AUTO_FAMILIES` and individual AGENT IDs are not in `AUTO_IDS`. This means: (1) even always-producing controls like AGENT-001/002/005 go through the review-tier loop (not auto-tier), which sets evidence/confidence but NEVER sets ar.status → all AGENT controls show `NOT_TESTED` regardless of scanner coverage; (2) conditional AGENT controls that don't fire (no trigger condition met) go through the review-tier no-match path (family evidence or structured checklist), also staying `NOT_TESTED`.

**`StigsDB.get_all()` is never called from `main.py`** — joins `ScansDB.get_history()`, `SystemsDB.get_all()`, and `SystemsDB.find_by_target()` as dead read methods from an unimplemented history/audit UI. `StigsDB.save()` IS called in `_import_stig()` and uses `ON CONFLICT(stig_id) DO UPDATE` — re-importing the same STIG (same benchmark ID) overwrites the existing DB record and regenerates the `.md` file.

**Report format options** (GUI dropdown, default "HTML dashboard + Markdown"):
- "HTML dashboard + Markdown" → HTML + Markdown + CSV (CSV always generated)
- "HTML dashboard only" → HTML + CSV
- "Markdown only" → Markdown + CSV
- "JSON" → JSON + CSV

CSV is generated unconditionally for every scan regardless of selection. Multi-target mode options: "Separate reports" (default) or "Combined report".

**Report filename pattern** (`_write_reports()` in `main.py`): `{type_prefix}_{safe_target}_{timestamp}.{ext}`. The `type_prefix` maps: `website` → `website`, `api` → `api`, `code` → `code-review`, `agent` → `agent`, `stig` → `stig`, all others (including `os` and `interconnected`) → `assessment`. `safe_target` is the hostname (for URLs) or basename (for file/path inputs), stripped and truncated to 40 chars. Timestamp format is `%Y-%m-%d %I.%M%p` lowercased (e.g. `2026-06-13 02.30pm`). Example: `website_example.com_2026-06-13 02.30pm.html`.

**Markdown report omits INFORMATIONAL from severity breakdown.** `generate_markdown_report()` in `reporter.py` only lists CRITICAL/HIGH/MEDIUM/LOW in its severity summary table (lines 350–354). INFORMATIONAL findings will appear in the Findings section if they are NON_COMPLIANT, but are not counted in the severity table header. HTML and JSON reports include INFORMATIONAL in their data.

**JSON report silently omits NOT_TESTED and NEEDS_REVIEW controls.** `generate_json_report()` (lines 444–471) routes each AssessmentResult to exactly one of three arrays: `"findings"` (NON_COMPLIANT), `"compliant"` (COMPLIANT), or `"false_positives"` (is_false_positive). Controls with status NOT_TESTED, NEEDS_REVIEW, or NOT_APPLICABLE appear in neither array — they are absent from the JSON output entirely. For any incomplete assessment (which includes all STIG assessments, since manual items remain NOT_TESTED), the JSON export produces a partial view. The HTML report does include all controls regardless of status (via `engine.all_results` loop at line 168).

**Template selection by target type** (`get_template_path()` in `reporter.py`): `interconnected` → `interconnected-report-template.html`; `code`/`code_review` → `code-review-report-template.html`; `api` → `api-report-template.html`; `os`/`os_software` → `report-template.html`; `agent` → `report-template.html` (falls through to default). The `agent` target type does NOT have its own template — it shares `report-template.html` with website and OS scans. However, `_report_title()` does return a distinct string for agents: `target_type == 'agent'` → `"Agent Security Assessment"` (while OS → `"OS & Software Security Assessment"`, API → `"API Security Assessment"`, code → `"Code Review Security Assessment"`). Template selection uses `selected_sets` if available, falling back to `target_type`.

**STIG data is injected differently from normal HTML reports.** `_generate_stig_html_report()` does NOT use `{{PLACEHOLDER}}` substitution. Instead, it builds a `<script>` block containing two JavaScript variables — `STIG_META` (target, date, tester, counts) and `CONTROLS` (full stig_data array) — and injects it via `template.replace('</head>', data_script + '\n</head>')`. The STIG template is expected to read these JS globals at runtime. This means `{{REPORT_TITLE}}` etc. are NOT substituted in the STIG report — the template must use the JS vars directly.

**STIG CAT level mapping** (`_sev_to_cat()` in `reporter.py`): CRITICAL/HIGH → CAT I, MEDIUM → CAT II, LOW → CAT III, INFORMATIONAL/unknown → CAT II (default fallback). Used only in `_generate_stig_html_report()` to compute `catLevel` for each finding entry. STIG reports include open CAT I/II/III counts in the report header.

**STIG internal → display status mapping** (verified from `_generate_stig_html_report()` reporter.py lines 250–258):
- `COMPLIANT` → "Not a Finding"
- `NON_COMPLIANT` → "Open"
- `NOT_APPLICABLE` → "Not Applicable"
- `FALSE_POSITIVE` → **"Not a Finding"** (same as COMPLIANT — FPs are NOT separately identified in STIG summary counts)
- `NOT_TESTED` → "Not Reviewed"
- `NEEDS_REVIEW` → "Not Reviewed"

**`STIG_META` consequence: `nafCount` includes false positives.** Since FALSE_POSITIVE maps to "Not a Finding", `nafCount` in `STIG_META` = COMPLIANT + FALSE_POSITIVE controls combined. Individual CONTROLS entries do have `isFalsePositive: true` for FPs, so they're distinguishable at the card level but not in the summary header.

**`STIG_META` full structure** (injected as `var STIG_META = {...}` before `</head>`): `target` (engine.target string), `date` (formatted `%Y-%m-%d %H:%M`), `tester` (hardcoded `"Security Assessment Tool v1.0"`), `totalRules` (total control count), `openCat1/2/3` (NON_COMPLIANT counts per CAT), `nafCount` (COMPLIANT+FP), `naCount` (NOT_APPLICABLE), `nrCount` (NOT_TESTED + NEEDS_REVIEW).

**STIG report fallback** (`_generate_stig_fallback_html()`): If `stig-report-template.html` is missing from `pen-tester/assets/`, the STIG reporter falls back to a minimal static HTML table (Vuln ID, CAT level, Title, Status, Evidence truncated to 120 chars). No JavaScript interactivity — no filtering, no expand/collapse. This is a safety net only; the real template is required for full functionality.

**`scanners.py` name is misleading.** It is the website scanner specifically, not a generic scanner registry. The name predates the multi-scanner architecture.

**Control IDs are a proprietary FAMILY-NNN taxonomy.** The family abbreviations (AUTH, CRYPTO, HEADERS, AGENT, etc.) and three-digit control numbers are the tool's own naming scheme — not borrowed from OWASP, CWE, NIST, or any external standard. There is no external mapping to these IDs. A new session should never try to "align" control IDs to an external taxonomy or renumber them to match one.

**Reports are self-contained HTML files.** All scan data is embedded in the HTML at generation time as a JSON blob inside `<script type="application/json" id="sat-controls-data">`. The report template reads this tag: `JSON.parse(document.getElementById('sat-controls-data').textContent)`. When the user saves the report (after triage), the updated state is re-serialized back to this tag. Reports can be emailed, archived, and reopened offline — no server required.

**`sat-controls-data` JSON schema** — each entry in the array (built by `generate_html_report()` in `reporter.py`):
```
id           - control ID (e.g. "AUTH-001")
name         - control name string
family       - control family abbreviation
status       - COMPLIANT / NON_COMPLIANT / NOT_APPLICABLE / NEEDS_REVIEW / etc.
severity     - CRITICAL / HIGH / MEDIUM / LOW / INFORMATIONAL
cia          - e.g. "C, I"
evidence     - human-readable scanner output
finding      - same value as evidence (duplicate field; kept for template compatibility)
remediation  - remediation text
mitigation   - "YES" if false positive, "NO" otherwise
mitigationDesc - FP justification text (empty string if not FP)
note         - user's triage note (populated post-scan via GUI)
tier         - "automatic_confirmation" / "review_required" / "manual_confirmation"
statement    - control statement text from .md library
review_steps - review_procedure or test_procedure text from .md library
reachability - DIRECT / ONE_HOP / INTERNAL / MULTI_STEP / NONE
cvss         - {"score": float, "vector": str} or null if no CVSS data
frameworks   - [] (always empty; framework display is handled by FW_MAP in templates)
source       - scanner_name string or "manual" for manual_confirmation controls
```
`{{CONTROLS_JSON}}` is inserted with `json.dumps(findings_data).replace('</', '<\\/')` to prevent XSS via early `</script>` tags.

**Template placeholders** substituted by `generate_html_report()` (simple `str.replace`, no Jinja2): `{{REPORT_TITLE}}`, `{{TARGET_NAME}}` (hostname only for URLs, basename for paths), `{{TOTAL_CONTROLS}}`, `{{FRAMEWORK}}` (framework_filter or "All frameworks"), `{{NON_COMPLIANT_COUNT}}`, `{{CRIT_COUNT}}`, `{{HIGH_COUNT}}`, `{{MED_COUNT}}`, `{{LOW_COUNT}}`, `{{INFO_COUNT}}`, `{{CONTROLS_JSON}}`, `{{REPORT_DATE}}` (`%Y-%m-%d %H:%M`), `{{REPORT_ID}}` (random 8-char UUID prefix).

**CVSS scores come from the individual scanners, not from `engine.py`.** Each scanner result (`ScanResult`) carries its own `cvss_score` and `cvss_vector`. `engine.py` copies these onto `AssessmentResult` (`ar.cvss_score = sr.cvss_score`). For controls where no scanner produces a result — review_required with no evidence hit, all manual_confirmation controls — `cvss_score` stays at the dataclass default `0.0` and `cvss_vector` stays `""`. The statement "every finding includes a CVSS score" applies to scanner-generated findings only. Do not remove or stub out CVSS fields from ScanResult or AssessmentResult — this is a key requirement for regulated-environment use.

**`run_automatic_tier()` has a dead code line (engine.py line ~168).** `ar.status = sr.status.replace('_', '-') if sr.status == 'NON_COMPLIANT' else sr.status` is immediately overwritten by the `if/elif` block on lines 169–179. It has no effect. This is a remnant from an earlier version where statuses used hyphens (e.g. `NON-COMPLIANT`). Ignore it when reading the code.

**Auto-tier status assignment (lines 167–188) — exact logic when scanner match exists:**
- `sr.status == 'NON_COMPLIANT'` → `ar.status = 'NON_COMPLIANT'`, copy severity/evidence/cvss/remediation
- `sr.status == 'COMPLIANT'` → `ar.status = 'COMPLIANT'`, copy fields
- `sr.status == 'NEEDS_REVIEW'` → `ar.tier = 'review_required'`, append to `review_items`, **`continue`** (skips field assignment and FindingsDB.save for this control)
- anything else → `ar.status = sr.status`, copy fields
Note: the `continue` for NEEDS_REVIEW means promoted controls have `ar.severity = ""`, `ar.evidence = ""`, etc. at the end of the auto-tier loop. The review-tier processing loop (which runs after) then fills in evidence, severity, and all other fields for the promoted `ar` — because it was appended to `review_items`, the review loop processes it normally.

**Auto-tier family evidence status** (engine.py lines 210–217) — when an auto-tier control has no direct scanner match but related family controls were tested, `ar.status = 'COMPLIANT'` if AND ONLY IF all family results are `COMPLIANT`; otherwise `ar.status = 'NEEDS_REVIEW'` (never `NON_COMPLIANT`). Confidence = 0.5. **This status-setting behavior is ONLY in the auto-tier loop.** The review-tier no-match branch (lines 257–317) builds evidence and sets confidence (0.5 with family, 0.2 without) but **never sets `ar.status`** — review-tier controls stay `NOT_TESTED` regardless of what family siblings produced.

**`ar.remediation` fallback populated by engine for no-scanner controls.** For review-tier with no scanner match: `if not ar.remediation: ar.remediation = ar.control.fix_text or ar.control.statement` (engine.py line ~316). Same logic for manual_confirmation controls (engine.py line ~366). So by the time `reporter.py` serializes the result, `ar.remediation` is already set. `reporter.py`'s `r.remediation or r.control.fix_text or ""` is a second fallback guard for the edge case where the engine didn't set it — in practice the engine already set it.

**`apply_review_decision()` accepts four decision strings** (engine.py lines 397–413): `'false_positive'` → sets is_false_positive=True, status='FALSE_POSITIVE', calls FalsePositivesDB.add() and DecisionsDB.save(); `'accept'` → status='NON_COMPLIANT'; `'compliant'` → status='COMPLIANT'; `'na'` → status='NOT_APPLICABLE'. The `'false_positive'` option is NOT available in `apply_manual_decision()` — manual tier only has `'fail'` (→ NON_COMPLIANT), `'pass'` (→ COMPLIANT), `'na'` (→ NOT_APPLICABLE). None of these methods are called from `main.py` (the DB triage layer is non-functional), so all review and manual decision paths remain unexercised in the current GUI.

**Prior false positive and note carryover from report applies to ALL tiers.** At the end of `run_automatic_tier()` (engine.py lines 370–386), after all scanner processing, the code iterates `self.all_results` and applies `prior_report_data`. If a control ID was marked as FP in the prior report (`mitigation == 'YES'`), `ar.is_false_positive = True`, `ar.fp_justification` = prior justification or "Carried forward from previous assessment report", and `ar.status = 'FALSE_POSITIVE'`. If a note exists in the prior report, `ar.user_notes` is set. This runs AFTER scanner results are set, so a prior FP carryforward will override a scanner's NON_COMPLIANT result for that control.

**Manual_confirmation evidence generation differs from review_required no-scanner in two ways.** (1) Step count: manual shows ALL test procedure steps (no cap); review_required no-scanner caps at 6 steps (`steps[:6]`). (2) Statement handling: for manual controls, `Requirement: {control.statement}` is ALWAYS emitted first (if statement is non-empty), then test procedure steps are added — the statement is not a fallback; it's always present. For review_required no-scanner, the statement is a fallback shown ONLY IF `test_procedure` is empty (`elif ar.control.statement:` branch). Both split on `.` and format as `[ ] N. step.` (review) or `N. step.` (manual). Manual-tier `ar.confidence` is never set by the engine → stays at the dataclass default 1.0. This is the same as auto-tier no-scanner no-family, but for a different reason (no scanner coverage for manual controls by design).

**When multiple scanners return results for the same control, `NON_COMPLIANT` wins.** `run_automatic_tier()` builds `result_by_ctrl` by iterating all `scan_results`: `if sr.control_id not in result_by_ctrl or sr.status == 'NON_COMPLIANT': result_by_ctrl[sr.control_id] = sr`. If two scanners both hit `AUTH-001` — one returning COMPLIANT, one returning NON_COMPLIANT — the NON_COMPLIANT result is stored and used for the assessment. This is "worst-case wins" logic. A COMPLIANT result never overwrites a NON_COMPLIANT result for the same control ID.

**`automatic_confirmation` controls can be promoted to `review_required` at runtime.** If a scanner returns `NEEDS_REVIEW` status for a control that `classify_control()` placed in the auto tier, `run_automatic_tier()` sets `ar.tier = 'review_required'` and `ar.status = 'NEEDS_REVIEW'`, then **adds** the `AssessmentResult` to `self.review_items` (engine.py lines 173–177). The object is NOT removed from `self.auto_results` — it remains in both lists. This means `get_summary()['auto_total']` (=`len(self.auto_results)`) and `get_summary()['review_total']` (=`len(self.review_items)`) both count a promoted control — the tier totals overcount. `all_results` has it once (added during `load_controls()`). The tier in the final report for that control is `review_required` (because `ar.tier` was mutated). Scanner-reported uncertainty overrides the static tier assignment.

**Agent target type runs different scanners depending on input type.** In `run_automatic_tier()`, when `target_type == 'agent'`, the code uses **two independent `if` checks** (not `if/elif`):
```python
if os.path.isfile(self.target):
    scan_results = scan_agent(self.target, ...)      # file → static analysis
if self.target.startswith('http'):
    scan_results.extend(run_all_scanners(self.target, ...))  # URL → HTTP scanners
```
The design is additive (the comment says "# Also run website scanners") — if both conditions were true, both would run. In practice they are mutually exclusive because a URL is not a real file path (`isfile()` returns False for URLs). A URL agent target gets only the website HTTP scanner suite; a file-based agent config gets only static `scan_agent()` analysis.

**`VULN_PATTERNS` tuple format in `code_scanner.py`:** each entry is `(control_id, severity, regex_pattern, description, remediation)`. TypeScript reuses JavaScript patterns (`VULN_PATTERNS['typescript'] = VULN_PATTERNS['javascript']`). C reuses C++ patterns (`VULN_PATTERNS.setdefault('c', VULN_PATTERNS['cpp'])`). The language name in `VULN_PATTERNS` must match what `LANG_EXTENSIONS` returns for a file extension. Current `LANG_EXTENSIONS` mapping:
```
.py → python     .js → javascript   .ts → typescript   .jsx → javascript
.tsx → typescript  .java → java     .go → go           .php → php
.cs → csharp     .cpp → cpp        .c → c             .h → c
.hpp → cpp       .rs → rust
```
To add a new language: add entries to `LANG_EXTENSIONS` (extension → lang name), add a `VULN_PATTERNS[lang_name]` list of tuples, and add the lang name to `code-review-controls.md`'s `Languages:` field for relevant controls.

**`scan_file()` stops at the first match per pattern per file** (line 176: `break`). If a file has 50 SQL injection instances all matching the same regex, only the first is reported. A control with multiple patterns (e.g., SEC-INJ-001 Python has two entries) can produce multiple results — one per distinct pattern that matches — but each pattern stops at its own first match.

**Code scanner produces ONLY `NON_COMPLIANT` results** — `scan_file()` never emits COMPLIANT. If no pattern matches a file, no ScanResult is produced for that control. Auto-tier code controls with no match fall through to the no-scanner NEEDS_REVIEW path in `run_automatic_tier()`.

**`reachability` is hard-coded to `'INTERNAL'`** for all code scanner ScanResults (line 174). Website scanners do not set it explicitly — they also get `"DIRECT"` via the `ScanResult` dataclass default (scanners.py line 45: `reachability: str = "DIRECT"`). The API scanner also does not set it — it too gets the dataclass default `"DIRECT"`. INTERNAL is correct for source code vulnerabilities (exploitation requires access to the codebase); DIRECT is the sensible default for HTTP-based and API findings.

**`_analyze_complexity()` caps function body scanning at 200 lines** (line 254: `range(i + 1, min(len(lines), i + 200))`). Functions longer than 200 lines from their opening line have truncated complexity and nesting analysis. CPX-STRUCT-001 (function length) still fires based on `func_lines > 50`, but CPX-METRIC-001 and CPX-STRUCT-003 may be undercounted for very long functions.

**`SEC-AUTH-001` Python pattern is effectively abandoned.** The regex `r'@app\.route.*\ndef\s+\w+.*\n(?:(?!login_required|...).)*$'` contains `\n` newline sequences and expects multi-line content, but `scan_file()` applies it to one line at a time via `re.search(pattern, line, re.IGNORECASE)`. The regex will never match a single line and never fires. More importantly, SEC-AUTH-001 is in `MANUAL_IDS` — even if the regex were rewritten to scan file content as a block, the scanner result would be silently dropped by the engine (manual-tier controls never read `result_by_ctrl`). The control always shows NOT_TESTED with a test procedure checklist. No fix is planned.

**`DEV-BUILD-001` has no VULN_PATTERNS entry and is never produced.** It's in AUTO_IDS, so it's in `auto_results`. With no direct scanner match, the auto-tier else branch runs: family relatives = scan_results starting with "DEV-BUILD" — DEV-BUILD-002 IS produced for Python/PHP, so DEV-BUILD-001 gets family-based evidence (confidence 0.5) and status COMPLIANT if DEV-BUILD-002 is COMPLIANT, else NEEDS_REVIEW. It stays in `auto_results` (not promoted). `DEV-BUILD-002` (debug mode enabled) IS covered for Python and PHP only.

**`ScanResult` dataclass** — the data contract every scanner must return (defined in `scanners.py` lines 33–46). `engine.py` imports `ScanResult` from `scanners` and copies fields onto `AssessmentResult`. Any new scanner must return a list of `ScanResult` objects:

| Field | Type | Default | Notes |
|---|---|---|---|
| `scanner` | str | — | required; scanner class name string (e.g. `"tls-scanner"`) → copied to `AssessmentResult.scanner_name` |
| `control_id` | str | — | required; FAMILY-NNN control this result maps to |
| `status` | str | — | required; `COMPLIANT` / `NON_COMPLIANT` / `ERROR` / `NEEDS_REVIEW` |
| `severity` | str | `"MEDIUM"` | copied to `AssessmentResult.severity` |
| `evidence` | str | `""` | human-readable scanner output |
| `confidence` | float | `1.0` | 0.0–1.0 |
| `elapsed_seconds` | float | `0.0` | diagnostic only; not stored in `AssessmentResult` |
| `remediation` | str | `""` | copied to `AssessmentResult.remediation` |
| `cvss_score` | float | `0.0` | copied directly; engine does not recompute |
| `cvss_vector` | str | `""` | full CVSS v3.1 vector string |
| `reachability` | str | `"DIRECT"` | default `"DIRECT"`; valid values: `DIRECT`, `ONE_HOP`, `INTERNAL`, `MULTI_STEP`; stored in DB; no automatic re-scoring in standalone |

**`scanners.py` contains 10 website HTTP scanner classes** (the `WEBSITE_SCANNERS` list). All make live HTTP requests. Exact control IDs actually produced per class (verified against source — `.controls` list and actual `scan()` output can differ):

| Scanner class | `.name` | Controls actually produced | Controls declared but never produced |
|---|---|---|---|
| `TLSScanner` | `tls-scanner` | CRYPTO-001, CRYPTO-002, CRYPTO-005 | CRYPTO-003, CRYPTO-004, CRYPTO-006 |
| `HeaderScanner` | `header-check` | HEADERS-001–006, HEADERS-007 (CORS) | — |
| `CookieScanner` | `cookie-audit` | SESSION-001 (no-cookie case only), SESSION-003, SESSION-004, SESSION-005 | SESSION-002 |
| `AuthScanner` | `auth-probe` | AUTH-001, AUTH-004 | AUTH-005 |
| `AuthzScanner` | `authz-probe` | AUTHZ-001, AUTHZ-002, AUTHZ-003, AUTHZ-004 | AUTHZ-005 |
| `InputValidationScanner` | `input-fuzzer` | INPUT-001, INPUT-003, INPUT-004, INPUT-005 | INPUT-002, INPUT-006, INPUT-007 |
| `EndpointDiscoveryScanner` | `endpoint-discovery` | COMP-001, COMP-003, INFRA-001, INFRA-002, INFRA-004, DATA-002, DATA-004, AUDIT-001 | — |
| `SessionScanner` | `session-analyzer` | SESSION-001 (if session cookie found), SESSION-002, AUTH-003, AUTH-006 | — |
| `SecretScanner` | `secret-scan` | SECRETS-001, SECRETS-002 | SECRETS-003 |
| `ErrorHandlingScanner` | `error-check` | ERROR-001 | ERROR-002, ERROR-003 |

**The `.controls` list on each scanner is documentation, not contract** — `scan()` may not produce all declared IDs. CRYPTO-003/004/006, AUTH-005, AUTHZ-005, SECRETS-003, ERROR-002/003, INPUT-002/006/007 are declared in their respective `.controls` lists but have no producing code path. What happens to each when not produced:

- **CRYPTO-003/004/006** (CRYPTO is in `AUTO_FAMILIES` → auto_confirmation tier): no scanner match → auto-tier else branch → related = scan_results starting with "CRYPTO" (e.g. CRYPTO-001, CRYPTO-002, CRYPTO-005 produced by TLSScanner) → family-based evidence, confidence=0.5, status=COMPLIANT if all siblings COMPLIANT else NEEDS_REVIEW. **These controls stay in `auto_results` — they are NOT promoted to `review_required`**. Promotion only happens when the scanner explicitly returns NEEDS_REVIEW; a no-match fallback always stays in auto_results.
- **INPUT-002** (in `AUTO_IDS` → auto_confirmation): family relatives INPUT-001/003/004/005 are produced by InputValidationScanner → family-based evidence, confidence=0.5.
- **SECRETS-003** (in `AUTO_IDS` → auto_confirmation): family relatives SECRETS-001/002 produced by SecretScanner → family-based evidence, confidence=0.5.
- **ERROR-002/003** (in `AUTO_IDS` → auto_confirmation): family relative ERROR-001 produced by ErrorHandlingScanner → family-based evidence, confidence=0.5.
- **AUTH-005** (in `AUTO_IDS` → auto_confirmation): family relatives AUTH-001/003/004/006 produced by AuthScanner/SessionScanner → family-based evidence.
- **AUTHZ-005** (in `MANUAL_IDS` → manual_confirmation): manual tier, receives only checklist evidence from test_procedure; scanner result (if one existed) would be silently dropped anyway.
- **INPUT-006/007** (not in AUTO_IDS/MANUAL_IDS → review_required): review loop; family relatives INPUT-001/003/004/005 produced → family-based evidence, confidence=0.5, **status stays NOT_TESTED** (review loop never sets ar.status).
- **INFRA-003** (in `AUTO_IDS` → auto_confirmation): not in any scanner's `.controls` list and no code produces it (grep confirms zero matches in `scanners.py`). Gets family-based evidence from INFRA-001/002/004 results produced by `EndpointDiscoveryScanner`, confidence=0.5. Stays in `auto_results`.

**`AUDIT-001` is review_required but EndpointDiscoveryScanner always produces a NEEDS_REVIEW result for it** (scanners.py lines 1002–1022). Since AUDIT-001 is not in AUTO_IDS or MANUAL_IDS, `load_controls()` puts it in `review_items`. The scanner result enters `result_by_ctrl` normally, and the review-tier loop finds the match. However — following the Round 19 pattern — the review loop sets `ar.evidence`, `ar.confidence`, `ar.severity` from the scanner result but **never sets `ar.status`**. AUDIT-001 therefore shows as NOT_TESTED with scanner evidence populated, NOT as NEEDS_REVIEW. The NEEDS_REVIEW status from the scanner result is read and discarded.

**`CookieScanner` only produces SESSION-001 in the no-cookies case (COMPLIANT).** When the server sets cookies, `CookieScanner` produces SESSION-003/004/005 from cookie flags — but SESSION-001 and SESSION-002 are NOT produced. When the server sets no cookies at all, `CookieScanner` returns SESSION-001 COMPLIANT and exits early. `SessionScanner` is the only scanner that produces SESSION-002 (always → NEEDS_REVIEW) and the full SESSION-001 analysis (length-based, only when a named session cookie exists). For `result_by_ctrl` dedup: if both scanners produce SESSION-001, SessionScanner runs last and its NON_COMPLIANT wins.

**`AUTH-002` is not in any scanner's control list** — auto_confirmation tier (in AUTO_IDS) with no direct scanner result. Gets family-based evidence from AUTH-001/003/004/006 results (all from AUTH family), confidence=0.5, status=COMPLIANT if all COMPLIANT else NEEDS_REVIEW. Stays in auto_results (not promoted).

**`AuthScanner` makes 6 active POST requests** to the discovered login endpoint with test credentials (`username: test@test.com, password: wrongpassword`). This is active login probing — it can trigger account lockout, IDS alerts, or be logged in security systems. The scanner probes up to 9 common login paths (`/login`, `/signin`, etc.) to find the endpoint first, then sends 6 rapid POSTs to test rate limiting.

**`AuthzScanner` actively probes 18 admin paths and 9 sensitive paths.** The 18 ADMIN_PATHS include `/admin`, `/admin/dashboard`, `/administrator`, `/manage`, `/panel`, `/console`, `/api/admin`, `/wp-admin`, `/phpmyadmin`, `/cpanel`, `/dashboard`, `/settings`, `/config`, and variants. The 9 SENSITIVE_PATHS include `/api/users`, `/api/user/1`, `/api/user/2`, `/api/accounts`, `/api/orders`, `/api/payments`, and variants. All probed with GET requests, `allow_redirects=False`, 5-second timeout per path.

**Scanner crash behavior: only `controls[0]` gets an ERROR result.** If a scanner's `scan()` method raises an unhandled exception, `run_all_scanners()` catches it and appends a single ERROR result using `scanner.controls[0]` as the control_id. The other controls in `scanner.controls` receive no result and fall through to the engine's no-scanner fallback. A scanner crash does NOT produce ERROR for all its declared controls.

If `HAS_REQUESTS = False` (requests not installed), some scanners return early: `HeaderScanner` and `CookieScanner` return a single ERROR ScanResult. `AuthScanner`, `AuthzScanner`, and `SessionScanner` return an empty list `[]` — silent fail, no error result.

**`ScanResult.elapsed_seconds` is a dead field and should be removed.** The dataclass includes `elapsed_seconds: float = 0.0` (line 41). Several scanners in `scanners.py` populate it (e.g., TLSScanner sets `elapsed_seconds=time.time() - start`). However, `engine.py` never reads `sr.elapsed_seconds` — it is not copied to `AssessmentResult`, not stored in `FindingsDB`, and not serialized in any report output. Decision: remove the field from the `ScanResult` dataclass and all scanner assignments to it.

**`HAS_BS4` (BeautifulSoup) is a dead import in `scanners.py` — remove it and its `requirements.txt` entry.** It is imported at lines 27–30 with a try/except guard, but `HAS_BS4` and `BeautifulSoup` are never referenced anywhere else in the file. No scanner conditionally uses BS4. `beautifulsoup4>=4.12.0` is listed in `requirements.txt` but serves no function. Decision: remove the try/except import block from `scanners.py` and remove `beautifulsoup4` from `requirements.txt`.

**`get_scanners_for_type()` in `scanners.py` always returns `WEBSITE_SCANNERS`** for every target type (including code, API, OS). This function is NOT what drives scanner dispatch — `engine.py` has its own explicit dispatch at lines 134–155 that overrides it:

```python
if target_type == 'code' and scan_code:       → scan_code() only
elif target_type == 'api' and scan_api:        → scan_api() only
elif target_type == 'os' and scan_os:          → scan_os() only
elif target_type == 'agent' and scan_agent:
    if os.path.isfile(target): scan_agent()    → scan_agent() for file targets
    if target.startswith('http'): run_all_scanners()  → ALSO website scanners if URL-based
else:                                          → run_all_scanners() (website/fallback)
```

**STIG assessments produce no useful scanner results.** `target_type='stig'` falls to the `else` branch and calls `run_all_scanners()`, which runs WEBSITE_SCANNERS against the XML file path. Each website scanner fails (XML path is not a valid URL/hostname) and the exception handler produces ERROR `ScanResult` objects keyed to each scanner's `controls[0]`. These ERROR results are in `scan_results` and `family_evidence`, but no STIG control family (e.g. `CYLN-OP`, `APSC-DV`) matches the website scanner control families (CRYPTO, HEADERS, etc.) — so all STIG controls fall to the review no-match no-family checklist path. STIG assessments have only review-tier controls (auto_results=[], manual_items=[] — STIG controls are always review_required, never manual_confirmation).

**`result_by_ctrl` deduplication** in `run_automatic_tier()` (engine.py line 160): multiple scanner results for the same control_id are reduced to one, keeping NON_COMPLIANT over any other status. If both are NON_COMPLIANT, later-processed scanner wins. If a control has no scanner result, engine.py checks for family-based evidence from related controls (confidence 0.5).

**NEEDS_REVIEW in the auto tier has two distinct paths with different DB behavior:**
1. **Scanner returns NEEDS_REVIEW** (engine.py line 173): `ar.tier='review_required'`, appended to `review_items`, then `continue` — skips field assignment (severity/evidence/cvss/etc. NOT set from scanner yet) AND skips FindingsDB.save. Fields get set later in the review loop.
2. **No scanner result, family evidence shows partial failure** (line 216): `ar.status='NEEDS_REVIEW'`, stays in `auto_results` (NOT added to `review_items`), evidence and confidence ARE set, FindingsDB.save IS called.
3. **No scanner result, no family evidence either** (line 219): same — stays in `auto_results`, FindingsDB.save IS called, but evidence is the generic "No scanner covers X" message.
Paths 2 and 3 produce NEEDS_REVIEW rows in FindingsDB; path 1 does not.

**`agent_scanner.py` does static analysis, not live HTTP.** It parses configuration files to assess AI agent security posture. This is distinct from `scanners.py` (which makes live HTTP requests to a website). Both map to the same controls library (`controls-library.md`), but the evidence collection method is entirely different.

**`agent_scanner.py` produces results for AGENT-001 through AGENT-011 — but not all 11 always appear.** The exact output depends on what keywords are found in the config file:
- **Always produces a result:** AGENT-001 (NON_COMPLIANT if high-risk tools found, COMPLIANT otherwise), AGENT-002 (NON_COMPLIANT if no validation keywords, NEEDS_REVIEW if found), AGENT-005 (NON_COMPLIANT if injection surface tools found, NEEDS_REVIEW otherwise)
- **Conditional (absent from results if not triggered):** AGENT-003 (only if database/file tools → data exposure risk list is non-empty), AGENT-004 (only if both `high_risk` tools AND `declared_purpose` is non-empty — `declared_purpose` is extracted via `re.search(r'description[:\s]*>?\s*\n?\s*(.+?)(?:\n---|\n#|\Z)', content, re.IGNORECASE | re.DOTALL)`, capped at 200 chars; empty string if no match → AGENT-004 not triggered), AGENT-006 (only if none of `['error', 'exception', 'fail', 'graceful', 'fallback']` found in content — all 5 keywords checked, not just 3), AGENT-007 (only if `DANGEROUS_INSTRUCTIONS` phrases found), AGENT-008 (only if delegation keywords like "delegate", "crew", "chain" found), AGENT-009 (only if no prompt-protection phrases found), AGENT-010 (NON_COMPLIANT only if explicit "without confirmation" or high-risk with no confirmation keywords), AGENT-011 (only if plugin/mcp/extension keywords found)

**Full keyword sets (all verified against source):**

`HIGH_RISK_TOOLS` (triggers AGENT-001, AGENT-003, AGENT-004, AGENT-005, AGENT-010): `bash`, `shell`, `exec`, `execute`, `system`, `command`, `terminal`, `write`, `writefile`, `delete`, `remove`, `rm`, `unlink`, `sendemail`, `send_email`, `email`, `smtp`, `mail`, `database`, `databasequery`, `sql`, `query`, `db`, `webrequest`, `http`, `fetch`, `curl`, `webhook`, `deploy`, `publish`, `push`, `upload`, `payment`, `transfer`, `transaction`.

`MEDIUM_RISK_TOOLS` (triggers AGENT-001 evidence only, not risk flags): `read`, `readfile`, `file`, `filesystem`, `webfetch`, `browse`, `search`, `websearch`, `mcp`, `plugin`, `extension`, `tool`, `api`, `rest`, `graphql`.

`DEFENSIVE_KEYWORDS` (for AGENT-002): `validate`, `sanitize`, `check`, `verify`, `filter`, `whitelist`, `allowlist`, `restrict`, `limit`, `bound`, `escape`, `encode`, `reject`, `deny`, `refuse`.

`DANGEROUS_INSTRUCTIONS` (for AGENT-007): `don't ask`, `do not ask`, `without confirmation`, `without asking`, `just do it`, `no restrictions`, `unrestricted`, `any command`, `any file`, `any database`, `any query`, `all allowed`, `no limits`, `no limitation`, `unlimited`.

`CONFIRMATION_KEYWORDS` (for AGENT-010): `confirm`, `confirmation`, `approve`, `approval`, `ask`, `permission`, `consent`, `verify`, `human-in-the-loop`, `before proceeding`, `user must`, `requires approval`.

**`agent_scanner.py` produces results for AGENT-007 and AGENT-010, but both are `manual_confirmation` tier — the scanner evidence is silently discarded.** AGENT-007 and AGENT-010 are in `MANUAL_IDS`. The engine's `run_automatic_tier()` builds `result_by_ctrl` from scanner output, but the manual-tier loop (lines 343–367) never reads `result_by_ctrl` — it only builds a checklist from `test_procedure`. The agent scanner's AGENT-007/010 findings (danger instructions, no-confirmation patterns) are generated, enter `result_by_ctrl`, and are then silently dropped. These controls show NOT_TESTED with test procedure checklist evidence, regardless of what the scanner found. **This is a known inconsistency worth fixing:** either move AGENT-007 and AGENT-010 to `review_required` tier (remove from `MANUAL_IDS`) so scanner evidence surfaces in reports, or remove their scan logic from `agent_scanner.py` entirely since the results are wasted. Currently unresolved — see Open Question 12.

**Tool detection uses word-boundary regex** (`re.findall(r'\b\w+\b', content_lower)`) — finds discrete words only. `fetch` matches but `fetchUrl` or `web_request` do NOT (the word boundary splits on `_` and case changes don't help). This means config files using camelCase tool names (common in LangChain, MCP manifests) may undercount tool risk.

**AGENT-008 delegation check includes `'agent'` in its keyword list.** Full list: `['delegate', 'agent', 'crew', 'chain', 'graph', 'multi-agent', 'sub-agent', 'handoff']`. The word `'agent'` appears in nearly every agent configuration file, meaning AGENT-008 fires for virtually every agent assessment — the evidence text saying "Multi-agent delegation indicators: agent" is expected and normal.

**AGENT-011 plugin check includes `'tool'`, `'action'`, `'function'` in its keyword list.** Full list: `['plugin', 'extension', 'mcp', 'tool', 'action', 'function']`. `'tool'` and `'function'` are extremely common words in agent config files, so AGENT-011 fires for nearly every assessment.

**AGENT-009 prompt protection keywords** (full list, substring-matched): `'do not reveal'`, `'never share'`, `'keep confidential'`, `'do not repeat'`, `'instructions are private'`, `'system prompt is'`. If none of these exact phrases appear → NON_COMPLIANT. If any appear → no AGENT-009 result (implicitly compliant).

**AGENT-010 has two separate NON_COMPLIANT paths:**
1. Explicit no_confirmation phrases found (`'don't ask'`, `'without confirmation'`, `'send immediately'`, `'execute without'`, `'just do it'`): NON_COMPLIANT, confidence 0.9
2. High-risk tools present AND no confirmation keywords found: NON_COMPLIANT, confidence 0.7
If confirmation keywords ARE found (even without explicit no-confirmation language): no AGENT-010 result produced at all.

**`code_scanner.py` covers 9 languages** (python, javascript, typescript, java, go, php, csharp, cpp/c, rust) via `VULN_PATTERNS` dict + `LANG_EXTENSIONS` map. Each entry is `(control_id, severity, regex_pattern, description, remediation)`. Control families covered: SEC-INJ-001–006 (injection/deserialization), SEC-CRYPTO-001–004 (secrets/weak crypto/insecure random/password hashing), SEC-AUTH-001 (missing auth decorator), SEC-DATA-001/002/004 (sensitive data in logs, SELECT *, error exposure), SEC-MEM-001–002/004 (buffer overflow, use-after-free, unsafe blocks — Rust/C++ only), SEC-MEM-005–006 (resource management — higher-level langs), DEV-BUILD-002 (debug mode), DEV-TEST-003 (test-mode auth bypass). Detection is purely line-by-line regex — no AST, no semantic analysis, no cross-file dataflow. `scan_target()` routes to `scan_file()` (single file) or `scan_directory()` (recursive walk), both return `ScanResult` lists.

**`code_scanner.py` also produces CPX-* and CPX-MAINTAIN-* control results** — not just vulnerability patterns. `_analyze_complexity()` produces: `CPX-STRUCT-004` (file > 500 lines, severity INFORMATIONAL), `CPX-STRUCT-001` (function > 50 lines, severity LOW), `CPX-METRIC-001` (cyclomatic complexity > 10, severity MEDIUM if ≤15 else HIGH), `CPX-STRUCT-003` (nesting depth > 4, severity MEDIUM). `_check_practices()` produces: `CPX-MAINTAIN-002` (unused Python imports, severity LOW), `CPX-MAINTAIN-003` (empty/bare exception handlers, severity MEDIUM — Python/JS/Java/Go/PHP only), `CPX-MAINTAIN-001` (< 50% of Python functions have type annotations, severity LOW). Complexity analysis only examines the first 200 lines of each function body. CPX-STRUCT, CPX-METRIC, CPX-MAINTAIN are in `AUTO_FAMILIES` so these controls are auto-tier. All vulnerability pattern results use `confidence=0.85` and `reachability='INTERNAL'`; complexity results use default confidence (1.0) and no reachability.

**Each vulnerability pattern fires at most once per file** — `scan_file()` calls `break` after the first matching line. A file with 10 SQL injection vulnerabilities produces one ScanResult for that pattern. If a file has two different `SEC-INJ-001` patterns both matching, two ScanResults with `control_id='SEC-INJ-001'` are produced. For directory scans, `result_by_ctrl` dedup in `run_automatic_tier()` keeps only the last NON_COMPLIANT per control ID — so if 5 files each trigger `SEC-INJ-001`, only one finding surfaces in the final assessment. This is the biggest limitation of the code scanner for large codebases.

**Code scanner results for MANUAL-tier controls are silently dropped.** `run_automatic_tier()` only maps scanner results to controls in `self.auto_results` and `self.review_items`. Manual-tier controls (`self.manual_items`) receive only the checklist-from-test_procedure evidence, never scanner evidence. SEC-AUTH-001 and SEC-AUTH-002 are in `MANUAL_IDS` — even if the pattern fires, the result is ignored. DEV-TEST-003 (test-mode auth bypass, flagged by the JS pattern) is also manual tier — same outcome. Additionally, the `SEC-AUTH-001` Python pattern (`@app.route.*\ndef\s+\w+.*\n...`) contains `\n` literals but is applied line-by-line, so it never matches — it's a dead pattern even before reaching the manual-tier drop.

**`scan_directory()` skips common non-source directories**: `{'node_modules', '.git', '__pycache__', 'venv', '.venv', 'target', 'build', 'dist', 'vendor', '.idea', '.vscode'}`. Files with extensions not in `LANG_EXTENSIONS` are silently ignored. Files that raise `IOError`/`OSError` (permission errors, binary files) return an empty results list. File content is read as `encoding='utf-8', errors='ignore'` — non-UTF-8 bytes are silently dropped rather than crashing.

**No `.gitmodules` file exists at root.** Confirmed. Deleting `pen-test-triage-update/` requires no additional git cleanup — there is no `.gitmodules` reference that needs removing.

**`git add -f` is required to stage standalone files from the root repo.** `pen-tester/standalone/` is in the root `.gitignore`. Running `git add -A` from root silently skips all standalone files — no error, no warning. This is intentional. Always commit standalone files from within `pen-tester/standalone/`. If you ever need to force-add from root: `git add -f pen-tester/standalone/<file>` — but this is an anti-pattern; use `manage.ps1` or commit from the standalone dir.

**`PROJECT_HANDOFF.md` is the primary handoff document from June 12, 2026 onward.** `HANDOFF_SUPPLEMENT.md` and `Project_Handoff_Document.docx` are older reference artifacts. Sections 7 and 9 of the supplement are stale (see above). Section 8 (how to work with the user) and section 16 (error history) are inlined here. `HOW_TO_START_NEW_SESSION.txt` has been updated to reference this document, not the supplement.

**`AssessmentResult` dataclass fields** — exact definition at `engine.py` lines 40–58:

| Field | Type | Default | Notes |
|---|---|---|---|
| `control` | Control | — | the Control object from controls.py |
| `status` | str | `"NOT_TESTED"` | `COMPLIANT` / `NON_COMPLIANT` / `NOT_APPLICABLE` / `NEEDS_REVIEW` / `ERROR` / `NOT_TESTED` / `FALSE_POSITIVE` — always uppercase |
| `tier` | str | `""` | `automatic_confirmation` / `review_required` / `manual_confirmation` |
| `severity` | str | `""` | `CRITICAL` / `HIGH` / `MEDIUM` / `LOW` / `INFORMATIONAL` — from the control library; used for summary counts |
| `evidence` | str | `""` | scanner output or fallback message |
| `confidence` | float | `1.0` | 0.0–1.0; scanner-assigned, or fallback: 0.5 (family-based evidence, both tiers), 0.2 (review-tier no-match no-family → checklist), 1.0 default (auto-tier no-match no-family — engine does NOT set confidence, stays at dataclass default) |
| `cvss_score` | float | `0.0` | CVSS v3.1 base score |
| `cvss_vector` | str | `""` | CVSS v3.1 vector string |
| `reachability` | str | `""` | **Auto-tier only**: copied from `ScanResult.reachability` via `sr.reachability or 'DIRECT'` (engine.py line 186). **Review-tier**: never set by the review loop — stays `""` even when a scanner produced a direct match with explicit reachability. The `continue` in the auto-tier NEEDS_REVIEW promotion (line 177) also skips line 186, so promoted controls also have `ar.reachability = ""`. Reporter fallback (`r.reachability or "DIRECT"`, line ~1130) means all review-tier controls show `"DIRECT"` in JSON output. Valid values: `DIRECT`, `ONE_HOP`, `INTERNAL`, `MULTI_STEP`; stored in DB; not auto-re-scored in standalone |
| `remediation` | str | `""` | fix/remediation text from the control's fix_text field |
| `is_false_positive` | bool | `False` | set True when FP is applied; status is also set to `FALSE_POSITIVE` |
| `fp_justification` | str | `""` | the user-entered FP justification text |
| `prior_decision` | Optional[dict] | `None` | carryforward data loaded from assessments.db for this target+control |
| `prior_evidence_changed` | bool | `False` | True when evidence hash differs from the prior FP-suppressed finding |
| `user_decision` | str | `""` | the user's in-app triage decision (e.g. CONFIRM, SUPPRESS) |
| `user_notes` | str | `""` | user-entered notes, populated from prior assessments.db on carryforward |
| `scanner_name` | str | `""` | name of the scanner that produced this result |

`FALSE_POSITIVE` is a valid `status` value (set alongside `is_false_positive = True`). `NOT_TESTED` is the dataclass default and persists for controls that no scanner attempted. Never use lowercase status strings.

**Control library `.md` format — how a control entry looks:**
```markdown
### FAMILY-NNN
- **Name**: Human-readable control name
- **CIA**: A | C | I | AC | CI | ACI  (primary CIA triad impact)
- **Secondary**: C | I | A  (secondary CIA impact, optional)
- **OWASP**: AXX:202X  (OWASP Top 10 mapping)
- **NIST-800**: XX-X  (NIST SP 800-53 control ID)
- **ISO-27001**: A.X.X.X
- **CMMC**: XX.LX-X.X.X
- **DoD-SRG**: SRG-APP-XXXXXX
- **FedRAMP**: XX-X (Low|Moderate)
- **HIPAA**: §164.XXX — description
- **PCI-DSS**: Req X.X — description
- **SOC2**: CCX.X — description
- **SEC-FINRA**: citation
- **EU-DORA**: Art. X — description
- **EU-AI**: Art. X — description
- **Statement**: What the control requires (one or two sentences).
- **Severity if Non-Compliant**: CRITICAL | HIGH | MEDIUM | LOW | INFORMATIONAL
- **Test**: What to test and what outcome indicates non-compliance.
```
Tier is auto-assigned by `classify_control()` in `controls.py` — no `Tier:` field needed in the `.md` and any `Tier:` line present is ignored. Fields with keys not in `_known` will leak into `review_procedure`, so use only the documented field names above.

**`classify_control(control_id, family)` logic** (`controls.py` lines 98–103):
```
if control_id in AUTO_IDS or family in AUTO_FAMILIES:
    return "automatic_confirmation"
if control_id in MANUAL_IDS:
    return "manual_confirmation"
return "review_required"          # default
```
Priority: AUTO check (ID or family) → MANUAL check → default review_required.

**`AUTO_FAMILIES`** (line 43) — entire family is automatic_confirmation regardless of individual ID:
`CRYPTO`, `HEADERS`, `SESSION` (website/agent); `CONFIG`, `RATE` (API); `CPX-STRUCT`, `CPX-METRIC`, `CPX-MAINTAIN`, `DEV-DEP`, `DEV-BUILD`, `DEV-QUAL` (code review)

**`AUTO_IDS`** (line 53) — explicit IDs always automatic_confirmation (regardless of family):
- Website/agent: AUTH-001/002/005/006, INPUT-001–004, SECRETS-001–003, ERROR-001–003, DATA-004, COMP-001/003, INFRA-001–004
- API: BOLA-001, AUTH-001/002/003, BOPLA-001, FUNC-001, SSRF-001, CONFIG-001–004, INPUT-001–003, DATA-001/002/003, SECRETS-001/002, GRAPHQL-001–003, WEBHOOK-001/002
- OS/Software: PATCH-001/003, EOL-001, SVCCONFIG-002, SVCEXPOSE-001
- Code: SEC-INJ-001–006, SEC-MEM-001–006, SEC-CRYPTO-001–004, SEC-DATA-001/003/004, DEV-BUILD-001/002

**`MANUAL_IDS`** (line 82) — explicit IDs always manual_confirmation:
- Website/agent: AUTHZ-005, DATA-003, DATA-001, AUDIT-002/003, COMP-002, AGENT-007/010
- Cross-system: TRUST-001/002/003, INCIDENT-001/002, SUPPLY-001/002
- Code: DEV-QUAL-003, DEV-TEST-002/003, SEC-AUTH-001/002
- OS/Software: PATCH-002, SOFTINV-001

**Critical overlap — DATA-001 and DATA-003 appear in BOTH AUTO_IDS and MANUAL_IDS.** AUTO wins because `AUTO_IDS` is checked first in `classify_control()`. These IDs are `automatic_confirmation` despite also being listed in `MANUAL_IDS`.

**`_infer_family(control_id)`** (controls.py line 263–265): `control_id.rsplit('-', 1)[0]` — splits on the LAST hyphen, so compound families are preserved:
- `AUTH-001` → `AUTH`
- `SEC-INJ-003` → `SEC-INJ`
- `CPX-METRIC-001` → `CPX-METRIC`
- `HEADERS-007` → `HEADERS`
This is called when a control's `.md` entry has no `Family:` field. The inferred family then drives `classify_control()` — if the inferred family is in `AUTO_FAMILIES`, the control becomes `automatic_confirmation`.

**STIG controls** are never classified by `classify_control()` — STIG controls get `tier = "review_required"` as a hardcoded default (set during parsing), not via this function.

The template above applies to `controls-library.md` (website/agent). **`code-review-controls.md` has an additional field** not present in other libraries: `- **Languages**: ALL | Python | JavaScript | Rust | Java | C/C++ | C# | Go | PHP` — this controls which language-specific review steps are shown in reports via `filterReviewSteps()`. When adding a code review control, include this field and ensure the value is in the supported set.

**Multi-line field values in `.md` control libraries require 2-space indented continuation lines.** `_parse_control_section()` (controls.py lines 193–199) extends a field across multiple lines only if continuation lines start with exactly two spaces (`elif current_key and line.startswith('  ')`). A blank line, a line starting with `- **`, or a line with different indentation ends the field. If a `Test:` or `Statement:` value needs to span multiple paragraphs, each continuation line must be indented by 2 spaces. Failure to do so silently truncates the field at the first unindented line.

**`parse_stig_controls()` has NO multi-line continuation support.** Unlike `_parse_control_section()`, the STIG parser (controls.py lines 284–289) only reads single-line `- **Field**: Value` entries. It has no `elif line.startswith('  ')` continuation check. STIG fields that span multiple lines — long `VulnDiscussion`/`Statement` text or lengthy `Check`/`Fix` blocks that `stig_parser.py` writes with embedded newlines — are silently truncated to their first line when parsed into Control objects. The control's `.statement` and `.test_procedure` may be incomplete for verbose STIG checks.

**STIG controls: `review_procedure` is always `""`** — `parse_stig_controls()` never sets `review_procedure`; it's left at the dataclass default (empty string). In the engine's no-scanner fallback path, the review checklist reads `ctrl.test_procedure or ctrl.statement` for STIG controls. In reporter.py, the reviewer sees `review_steps = r.control.review_procedure or r.control.test_procedure` — since `review_procedure` is `""`, it falls back to `test_procedure` (the STIG `check` field).

**STIG controls: `test_procedure` and `check_content` are identical** — both are populated from `fields.get('check', '')` (lines 307 and 314). This is intentional redundancy: `test_procedure` feeds the reviewer checklist; `check_content` is the STIG-specific field for structured XCCDF compliance workflows.

**`fix_text` is ONLY populated for STIG controls — this is an oversight, not intentional.** `_parse_control_section()` (regular control parser, lines 246–260) does NOT include `fix_text` in the `Control()` constructor — it is left at the dataclass default `""`. The key is in `_known` (preventing `review_procedure` leakage) but extraction to `ctrl.fix_text` was simply never added. Only `parse_stig_controls()` (line 308) sets `fix_text=fields.get('fix', '')`. Consequence: for the engine's remediation fallback (`if not ar.remediation: ar.remediation = ar.control.fix_text or ar.control.statement`), non-STIG controls always fall through to `ar.control.statement`. The fix is to add `fix_text=fields.get('fix text', fields.get('fix', ''))` to the `Control(...)` constructor call in `_parse_control_section()`.

**Severity field name precedence in `.md` parser** — `_parse_control_section()` tries these keys in order: `"severity if non-compliant"` → `"severity"` → `"mapped severity"` → default `"MEDIUM"`. Use `**Severity if Non-Compliant**:` in regular control libraries. STIG `.md` files (generated by `stig_parser.py`) use `**Mapped Severity**:`. Do not use plain `**Severity**:` in new controls — it’s the lowest-precedence lookup and exists only as a legacy alias.

**`sat-controls-data` field sources — five non-obvious fallbacks in `reporter.py`:**
1. `severity` → `r.severity or r.control.severity` — if the scanner returns no severity (empty string, the `AssessmentResult` dataclass default), the control library’s severity is used. This applies to HTML, CSV, and JSON outputs.
2. `remediation` → `r.remediation or r.control.fix_text or ""` — scanner remediation wins; falls back to the control library’s `Fix:` field (`fix_text`). If neither exists, empty string. **Critical caveat: `control.fix_text` is always `""` for regular (non-STIG) controls** — `_parse_control_section()` omits `fix_text` from the `Control(...)` constructor call entirely (lines 246–260). The `Fix:` / `Fix Text:` keys are in `_known` (so they don’t leak into `review_procedure`) but the value is never stored. For regular controls, the fallback chain is effectively `r.remediation or ""`. For STIG controls, `fix_text` is correctly populated from the `fix` field (line 308).
3. `reachability` → `r.reachability or "DIRECT"` — `AssessmentResult.reachability` has a dataclass default of `""` (empty string), but the JSON entry is seeded as `"DIRECT"` when the field is empty. The template always sees a non-empty reachability.
4. `review_steps` → `r.control.review_procedure or r.control.test_procedure or ""` — `review_procedure` (test_procedure + all non-`_known` sub-fields concatenated) is preferred; `test_procedure` is the fallback if `review_procedure` is somehow empty.
5. `source` → `r.scanner_name or "manual"` — controls with no scanner (review_required fallback, all manual_confirmation controls) show `source: "manual"`.

**How to work with this user (inlined from supplement section 8):**
- Terse, direct commands. Rarely asks questions. Expects immediate action, not options or clarification.
- ALL CAPS = do it now. "ADD SUPPORT FOR X" means start building immediately.
- When asked "why is X broken" — diagnose AND fix in one response.
- Don’t ask clarifying questions when intent is clear.
- When given options, they pick the most comprehensive one every time. Default to the most complete option.
- Completeness and accuracy matter more than speed — verify before claiming done.
- They are the product owner AND architect. Don’t override their decisions; implement them.
- "How do you load the gui" means give the exact command (`python main.py`), not a tutorial.

---

## Repo State at Handoff

```
Multi-Modal-Scanner     https://github.com/CavenderProjects/Multi-Modal-Scanner
                        last commit: fbb4148  "Resolve merge conflicts - keep remote versions"
                        branch: main
                        UNCOMMITTED CHANGES: PROJECT_HANDOFF.md, HOW_TO_START_NEW_SESSION.txt
                        (modified across multiple sessions — not yet committed or pushed)

Multi-Modal-Scanner_Standalone  https://github.com/CavenderProjects/Multi-Modal-Scanner_Standalone
                                last commit: ecd4c08  "corrected formatting for manual review findings, updated README"
                                branch: main, up to date with origin
```

**To commit the handoff document before starting next session:**
```powershell
cd "C:\Users\slagb\OneDrive\Documents\Claude\Projects\Revised pen tester"
Remove-Item .git\index.lock -Force  # only if needed — clears stale lock from bash sandbox
git add PROJECT_HANDOFF.md HOW_TO_START_NEW_SESSION.txt
git commit -m "Rounds 13-24 handoff — Round 24: fix_text omission confirmed oversight (not intentional); SEC-AUTH-001 pattern confirmed abandoned (manual_confirmation + broken regex); AGENT-007/010 dropped results flagged as inconsistency (Open Question 12); STIG prior carryforward fix path documented; detect_languages() confirmed dead at detector.py line 122; elapsed_seconds decision: remove; HAS_BS4 decision: remove + drop beautifulsoup4 from requirements.txt; _abort_scan fix approach documented; combined mode double-count fix approach documented; os-software-controls.md header bug confirmed unfixed; Windows 11 EOL guidance added to longer term; pyyaml version capture added; pen-tester.skill rebuild process to be confirmed; generate_handoff.js confirmed absent from root"
git push
```

Run `.\manage.ps1 status` to verify current state before starting new work.
