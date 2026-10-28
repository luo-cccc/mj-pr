# Validation record — v3.1.0

Reviewed **2026-10-28**. Official documentation sources and model-specific gaps are maintained in [parameters.md](references/parameters.md).

## Implemented checks

- Parameter aliases and value cardinality, optional Personalization values and Edit Model reference syntax.
- Conservative intent advice for negated people and competing positive/negative descriptions.
- Bounded nested permutations, escaped separators, repeat accounting, duplicate review, requested totals and per-command job/character budgets.
- Invalid/empty input, file encoding errors and safe expansion limits.
- Local reference targets and static resource reachability from SKILL.md.

User intent overrides presets. Artistic choices such as brightness, palette and depth of field are not syntax constraints. See [maintenance](references/maintenance.md) for review and evidence policy.

## Native verification

Executed on **Python 3.14.6** from the repository root:

```bash
python -m unittest discover -s scripts -p 'test_*.py' -v
python scripts/audit_links.py --strict
```

Results:

- **36 tests passed; zero skipped, zero failures or errors.** This includes real CLI subprocess exit checks and test-entry failure propagation.
- All six batch demonstration files and 18 commands passed count and budget regressions: ten jobs per theme, at most four jobs and 2,000 characters per command.
- Strict audit passed with zero broken local targets and zero unreachable resources. External links are counted rather than fetched; Markdown heading anchors are not validated.

The current native results supersede earlier environment-blocked or fallback execution records. Regression counts refer to unittest methods; parameterized cases execute inside those methods.

## Verification boundaries

No current Midjourney generation was performed. Model availability, account entitlements, URL accessibility and visual acceptance remain outside text-test coverage. English intent analysis is heuristic and requires contextual review.

Previous small-sample experiments used another image model. Their fixed-region brightness and HSV measurements neither validate Midjourney nor establish universal aesthetic thresholds. Document and code corrections, runtime regressions and generated-image acceptance are separate evidence levels.
