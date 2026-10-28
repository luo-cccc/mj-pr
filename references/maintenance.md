# Maintenance and evidence policy

## Versioning and verification

Use patch versions for wording and compatibility corrections, minor versions for compatible capabilities, and major versions for changed workflow contracts. Record review and parameter-verification dates separately. A documented default is a dated claim, not an evergreen guarantee.

For version-sensitive updates, check the official [Version](https://docs.midjourney.com/hc/en-us/articles/32199405667853-Version) and [Parameter List](https://docs.midjourney.com/hc/en-us/articles/32859204029709-Parameter-List), then record source URL, date, exact model/interface and supported claim in [parameters.md](parameters.md). If checking is unavailable or out of scope, explicitly retain **unverified** status. Do not infer categorical `--cref`/`--oref` retirement from a newer workflow.

## Evidence and severity

| Evidence | What it supports |
|---|---|
| Official documentation checked for a specific model/interface | A scoped syntax or compatibility claim, with source/date |
| Third-party screenshot, including a rule marked “seen” | Evidence that an author used that convention, not official MJ authority |
| User brief or approved project direction | Requirements for that project, not universal model constraints |
| House preset | Optional starting guidance, overridden by intent |
| Small render sample or another image model | Conditional observations; no MJ validation or art law |

Hard failures are reserved for malformed syntax and explicitly supplied operational budgets. The shared [prompt analysis module](../scripts/prompt_analysis.py) expands nested permutations and checks every expanded prompt through the validator. Missing aspect ratios use model/input defaults and are advice, not syntax errors. Documented artistic suggestions are still suggestions. Camera terms, hyphens, multiword exclusions, deep focus, skin/robe color differences and brightness relationships are not hard failures. Conflicts with a brief should be reported as review issues, not mislabeled as invalid syntax. Repeated empirical evidence remains conditional; it does not become syntax by repetition.

Quality review follows explicit user requirements, semantic conflicts, composition/lighting/materials/character/environment, then actual-output acceptance. WARN messages invite contextual review; never rewrite a valid artistic choice just to eliminate them. Record each applicable visual requirement as pass, fail or unverified. A static check cannot supply the last step.

Generation evidence must identify the actual model/version and interface, raw submitted prompt with references/parameters, job ID or output file, and itemized visual observations tied to requirements. Separate observation from interpretation and mark missing evidence unverified. Multi-variable revisions support only a combined-result observation, not attribution to one change. Any numeric measurement must state its regions, method and limits; it is not a universal aesthetic threshold.

## Canonical sources

Negative bank definitions live only in [lexicons.md](lexicons.md#negative-banks-no-presets): A1–A2, B1–B4, C1–C2, D1, E1, F1–F6. Examples may expand selected candidates in runnable prompts, but cite their source and explain exceptions. Update membership in one place. B3 does not suppress anime or illustration; E1 does not broadly suppress realism or texture.

Parameter ranges and compatibility notes live in [parameters.md](parameters.md). Preserve six optional [production presets](production-presets.md) and intent-aware [series guidance](style-lock.md).

## Local checks

Run the [prompt regression suite](../scripts/test_validate.py) after linter changes and the [graph-audit regression suite](../scripts/test_audit_links.py) after audit changes. The [prompt validator](../scripts/validate_prompt.py) checks Discord-style prompt text, including reference URLs after `--edit`; it cannot inspect website attachments, certify model compatibility, or judge image quality. Numeric checks validate shape and finiteness, not every model's allowed range. Legacy reference names are recognized without asserting compatibility. Add false-positive guards for legitimate user intentions rather than new artistic taboos.

Batch expansion and conservative static semantic review share the [analysis module](../scripts/prompt_analysis.py). Modes remain `character`, `scene`, `style`. Use `--expected-count` for total expanded jobs including repeats, `--max-jobs` for each command's cap, `--max-chars` for complete command length and `--json` for itemized results. Expansion is bounded to 256 variants and 32 nesting levels per command to avoid resource exhaustion; repeat accounting accepts at most nine digits as a tool safety bound, not an account entitlement. Provide multiple commands as one `/imagine prompt:` line each; do not paste Markdown fences or explanations into a command file. Count mismatches, supplied budget violations and expansion errors are FAILs; possible semantic conflicts are WARNs. The English clause-based intent heuristics do not understand all natural language, reference images or subject-specific scope. Review their advice rather than treating it as a semantic verdict. Tests use automatic full `unittest` discovery and assert expected warnings or absence of unexpected warnings.

Run the full discovered suite and link audit from the project root. Python 3.9+ is required; the validator itself uses only the standard library. Commands below are instructions; actual execution evidence belongs in REVIEW.md.

```bash
python -m unittest discover -s scripts -p 'test_*.py'
python scripts/audit_links.py --strict
```

Use the [link auditor](../scripts/audit_links.py) to find broken local links, unexpected orphans and inbound counts. Reachability measures static navigation, not runtime loading, actual use or token cost. An orphan warrants inspection and routing review, never automatic deletion. Inspect every file before removing it. README and NOTICE are human-facing entry points but may also be read by agents.

Measure complete demo commands and their Cartesian job counts. Check count preservation, the unknown-plan four-job fallback, and the 2,000-character demonstration budget; these are scoped operational policies, not universal model or image-quality limits. Do not call APIs or generate paid images merely to maintain documentation.

Report completion in four separate categories: documentation fixes (guidance edited), code fixes (implementation changed), runtime regressions (exact command, scope and observed result), and image retests (generation evidence plus itemized visual acceptance). Mark each as completed, pending or not performed as applicable. Report only checks actually run; if Python cannot execute, state that explicitly and distinguish static review from regression execution. Documentation or code changes do not establish runtime success, and passing runtime checks do not establish a visual improvement.

## Publishing and privacy

Keep the installed directory name aligned with frontmatter name. [SKILL.md](../SKILL.md) routes on-demand resources; [README.md](../README.md) describes usage. Preserve [NOTICE.md](../NOTICE.md), upstream copyrights and LICENSE. Do not commit credentials, private reference images, private style/profile IDs or copied full help articles. Link official documentation and summarize only what is needed.
