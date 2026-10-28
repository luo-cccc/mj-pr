---
name: midjourney-prompt-suite
description: >-
  Write, refine, batch, and lint Midjourney prompts. Use for MJ parameter help,
  style vocabulary, Chinese classical and ink-wash looks, character sheets,
  scene plates, Discord permutations, version comparisons, and series visual
  consistency. Includes optional semi-realistic Chinese CG and BJD presets.
license: MIT
metadata:
  version: "3.1.0"
  reviewed: "2026-10-28"
  parameter_verified: "2026-10-28"
  parameter_verification: "Official documentation snapshot; see references/parameters.md for model scopes and unresolved gaps"
---

# Midjourney Prompt Suite

## Priority and scope

Follow explicit user requirements first, the project visual brief second, selected presets third, and fallback defaults last. Defaults are suggestions, not Midjourney constraints. Preserve the requested subject, style, framing, aspect, language and output count.

Three composable workflows: craft a prompt, apply a production template, and package a batch. Series consistency is an optional layer across them. A character standing in a scene does not automatically mean BJD, shallow focus, or a white-background sheet.

This skill primarily delivers prompts. Generate images or call a paid service only when requested. If the requested model is unavailable, report that result; do not silently substitute another model. Never store credentials in the skill or generated code. Results from another model are not Midjourney validation.

## Read by task

| Task | Resource to load |
|---|---|
| Parameters, aspect, version compatibility | [parameters.md](references/parameters.md) |
| Image inputs and style references | [image-and-style.md](references/image-and-style.md) |
| Style, material, light, palette vocabulary | [lexicons.md](references/lexicons.md) |
| Any negative bank | [lexicons.md](references/lexicons.md#negative-banks-no-presets), the only bank definition source |
| Full-body sheets, turnarounds, scene plates, six optional styles | [production-presets.md](references/production-presets.md) |
| Series consistency or subject/environment differentiation | [style-lock.md](references/style-lock.md) |
| Variations, permutations, command splitting, version A/B | [batching.md](references/batching.md) |
| User feedback on an image | [revision-playbook.md](references/revision-playbook.md) |
| Updating or auditing this skill | [maintenance.md](references/maintenance.md) |

Read only the resources relevant to the deliverable. Read a bank's definition before using its identifier; identifiers such as E1 are internal documentation labels and must never appear as literal MJ arguments.

## Craft workflow

1. Extract the subject, visible action, medium, composition, lighting, palette and intended use. Infer modest defaults when details are absent; ask only if a missing decision changes the result materially.
2. Write concrete visible descriptions. Default to concise English prompts and explanations in the user's language; honor a requested language. Quoted text to appear inside an image may use its original language.
3. Prioritize subject and composition, then the relevant style qualities. Use one coherent direction, without mechanically inserting every lexicon word. Camera terminology, hyphens, film stocks and artist/technical references are not inherently syntax errors.
4. Describe desired features positively. Use `--no` only for unwanted content, checking that it does not remove something requested. Multiword exclusions are not automatically invalid, but their words can be interpreted independently. Never "fix hands" by suppressing hands.
5. Place image inputs, text and supported parameters in the appropriate model syntax. Parameters normally follow the description. Commas in a `--no` list and punctuation inside valid URLs are allowed. Do not invent a version, reference URL, style code or profile ID.
6. Default delivery: one copyable prompt and a short note where useful. Add variants or translations when requested or helpful; do not force duplicate output.
7. Review against the explicit brief, then check competing descriptions and positive/negative conflicts. Scope material and style anchors to the relevant subject. Keep syntax checks, tentative semantic advice and actual-output acceptance separate. Never rewrite a valid artistic choice just to clear WARNs; only actual pixels can validate image quality.

## Production workflow

1. Identify the deliverable. A portrait, full-body asset sheet, turnaround and narrative composition require different framing.
2. For a full-body humanoid sheet, describe head/face, upper clothing, hands/pose, lower clothing and feet in order. Make all requested parts visible; allow barefoot, hidden hands and nonhuman anatomy when intended. White background and 9:16 are optional asset-sheet defaults.
3. For a turnaround, explicitly name front/side/back panels, consistent scale and neutral pose. A single standing portrait is not a turnaround. Verify panel continuity in the output; prompting cannot guarantee it.
4. For a scene plate, define spatial layout, viewpoint, important surfaces, palette and atmosphere. 16:9 and an unoccupied environment are fallback choices; populated battlefields and vertical environments remain valid.
5. Select a style preset only when it matches the brief. Preserve user styles outside the six presets. Do not put character anatomy into environment-only prompts or scenery into a white asset sheet merely because it occurs in a preset.
6. For the selected template, run [validate_prompt.py](scripts/validate_prompt.py), for example `python scripts/validate_prompt.py --mode character --file prompt.txt`. Resolve syntax FAILs. WARNs are review prompts, not vetoes and not reasons to override intent. Scene and series checks use `--mode scene` and `--mode style` respectively.

## Series consistency and same-frame differentiation

Lock project-specific invariants: medium, degree of stylization, material family, character identity anchors and reference strategy. Keep episode palette, shot lighting, pose and atmosphere as controlled variables.

For character/environment compositions, describe the character and background separately, then connect them through compatible light direction, perspective, contact shadows, reflections and grading. Differentiate through selected contrast, edge treatment, detail, value, color or focus. Choose what fits the shot: deep-focus staging, silhouettes and mixed warm/cool light are all legitimate. Neither a bright sky nor skin differing from blue clothing proves a failure.

Use BJD resin skin and doll geometry only when that look was selected. Share rendering language across assets without applying skin/eyes/hair language to architecture. References can help consistency but do not guarantee identity.

Inspect actual pixels for intent, anatomy, composition and continuity. Text linting cannot certify visual quality. Small-sample experiments and third-party screenshot conventions are evidence of preferences or observations, not universal MJ rules.

## Batch workflow

Preserve the user's requested count and suffix; default to ten variations when a batch count is absent. Vary only requested axes, or choose one explicit axis. Preserve a series' invariants.

Read [batching.md](references/batching.md) before permutation output. Group identical suffixes, escape literal commas within alternatives, and validate the full Cartesian expansion including repeats. Use `python scripts/validate_prompt.py --mode style --file commands.txt --expected-count 10 --max-jobs 4 --max-chars 2000 --json` for an unknown-plan ten-job Discord batch; adjust explicit budgets/counts to the brief and interface. Every nonblank line in a multi-command file must begin `/imagine prompt:`. Do not turn an unspecified theme into fifty jobs. RAW and PERMUTATION are available formats, not mandatory duplicates when one is requested.

For version A/B, verify both versions and every flag's compatibility first. A fixed seed helps comparison but cannot guarantee identical layouts across versions.

## Examples: select, do not preload

| Purpose | Example |
|---|---|
| Short form | [01](examples/01-official-short.md) |
| Colossal scale | [02](examples/02-photoreal-colossal.md) |
| Chinese classical | [03](examples/03-chinese-classical-figure.md) |
| Revision | [04](examples/04-revision-cameras-and-scale.md) |
| Soft aesthetic | [05](examples/05-aesthetic-soft.md) |
| Full-body sheet | [06](examples/06-production-character.md) |
| Scene plate | [07](examples/07-production-scene.md) |
| BJD series example | [08](examples/08-style-lock-series.md) |
| Character/environment composition | [09](examples/09-character-in-scene.md) |

Batch examples are linked individually from [batching.md](references/batching.md). They illustrate packing, not universal style recipes or proof of model-version support.

## Maintenance gate

Follow [maintenance.md](references/maintenance.md). The [final review](REVIEW.md) records corrections and verification limits. Run [test_validate.py](scripts/test_validate.py) and [audit_links.py](scripts/audit_links.py) after relevant changes. A static reference is reachable, not demonstrably used at runtime; report those two claims separately. Preserve source attribution and distinguish official documentation, user requirements, house defaults and tentative observations.
