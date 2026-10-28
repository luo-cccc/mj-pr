# Series style lock

## 1. Purpose and priority

Maintain a coherent project look across characters, environments, props and shots. User intent and the project brief override presets. The attached methodology document supplies production principles, not Midjourney API documentation.

A series need not use Chinese CG or BJD. Choose the project's medium first. A consistent style core helps continuity; copying every word into every shot is neither necessary nor sufficient.

## 2. Invariants and controlled variables

| Keep consistent | Allow controlled variation |
|---|---|
| Medium and degree of stylization | Composition, distance and pose |
| Material and surface-detail family | Shot-specific surfaces and costumes |
| Character face/proportion anchors | Expression and intended costume variants |
| Color-grading language | Episode palette and motivated lighting |
| Environmental design and detail scale | Weather, location and atmosphere |

Record approved anchors and references. Change an invariant deliberately and version the project brief. References can help but do not guarantee identity or geometry. Style reference and identity conditioning serve different purposes; use mechanisms supported by the selected model. Read [image-and-style.md](image-and-style.md).

## 3. Optional BJD / Chinese CG preset

Use only when requested or selected for the project.

- Form: semi-realistic Chinese animation character design, softened facial planes and refined doll proportions.
- Character material: fine matte resin skin, subtle doll makeup, clear glass-like eyes and arranged smooth hair. Exposed ball joints are optional.
- Rendering: dimensional CG lighting and coherent interaction with the environment.
- Environment: compatible stylized CG surfaces and detail scale; architecture does not need skin, eyes or hair.

Example character core: `semi-realistic Chinese animation CG, refined BJD-inspired facial design, fine matte resin skin, subtle doll makeup, clear glass-like eyes`.

Example environment core: `semi-realistic Chinese animation CG environment, refined matte surfaces, clean stylized architectural forms`.

These share rendering language without identical materials. Avoid combining a resin look with an anti-plastic negative bank. Read optional E1 and applicable banks in [lexicons.md](lexicons.md#negative-banks-no-presets).

## 4. Minimal brief and visual bible

Start with the approved style direction, relevant character/location references, palette intent and current shot purpose. A test shot may establish these; do not block it on a complete production bible.

For a larger series, expand to character/costume/expression sheets, location/atmosphere sheets, props, color scripts and lighting references. Warm romance, cool intrigue and muted grief are examples, not genre laws. Post-production grading helps but cannot repair all geometry or identity defects.

## 5. Per-shot assembly

1. State subject/action or environment layout.
2. Add the project's medium/rendering core.
3. Apply character-specific form/material anchors only to visible characters.
4. Add controlled palette and motivated light.
5. Select valid references and supported parameters; preserve requested aspect and never invent IDs.
6. Select relevant exclusions from [lexicons.md](lexicons.md#negative-banks-no-presets), allowing exceptions for signage, aging and intended texture.
7. Inspect actual pixels before claiming continuity.

## 6. Environment-only plates

Use environment rendering, layout, surfaces, light and grading. Do not accidentally introduce people by pasting a complete character paragraph. Empty and populated environments are both valid; follow the brief.

## 7. Character and environment in one frame

Treat the character and environment as distinct design subjects joined by one coherent world.

**Shared:** compatible rendering language, perspective, motivated light direction, grading, scale, contact shadows and reflected light.

**Differentiated:** choose some combination of silhouette, local contrast, shape, detail, material response, color grouping, staging, edges or focus. Characters may have refined facial treatment while scenery uses broader material/detail treatment, within one CG art direction.

No single separation tool is mandatory. Deep focus, rim light, softened scenery, silhouettes, bright skies, mixed warm/cool sources and reflective floors may all be intentional. Do not turn daylight into night to pass a brightness check.

```text
<character form, costume, pose and material>, <environment layout and surfaces>, <shared rendering and motivated lighting>, <selected differentiation>, <project grading> <supported parameters>
```

Review in order: explicit user requirements; semantic conflicts; composition, lighting, materials, character and environment; then actual-output acceptance at thumbnail and full size. Does the intended subject read, is it grounded, do light and materials belong together, and are requested background details preserved? Record each applicable requirement as pass, fail or unverified against the output. A dark silhouette against a bright sky can pass; a clean lint report cannot establish visual acceptance.

## 8. Evidence limits

Previous revisions generalized five renders of one palace/nobleman composition from `gpt-image-2.5-flare`. These were not Midjourney outputs and cannot establish MJ rules about sun removal, compulsory keys, face brightness, depth of field, resin keywords or a skin-to-costume hue gap.

The old fixed rectangles could include hair, clothes or sky rather than comparable surfaces. Arithmetic HSV hue averages ignore circular wraparound and become unreliable at low saturation. Different material colors do not measure illumination temperature. The old numeric thresholds are removed from operational guidance.

Use observations to form a hypothesis for that image. Record the actual generation model/version and interface, raw submitted prompt and references/parameters, job ID or output file, and itemized visual observations tied to the brief. Distinguish observation from interpretation and mark unavailable evidence unverified. Test appropriate regions, intended lighting and representative subjects before claiming a trend. If multiple variables change, report the combined result without attributing it to one change. Measurements must state regions, method and limitations; numbers are not universal aesthetic thresholds. Even a repeated trend remains conditional, not a syntax constraint.

## 9. Lint and examples

Run [validate_prompt.py](../scripts/validate_prompt.py) with `--mode style --file prompt.txt` for text checks. The shared [analysis module](../scripts/prompt_analysis.py) expands batches and performs conservative static semantic review; each expansion is checked. Use `--expected-count`, `--max-jobs`, `--max-chars` and `--json` when applicable. Modes remain `character`, `scene` and `style`. Static checks cannot certify model support, identity, composition or visual quality. Review WARN messages against the brief; never rewrite valid artistic choices merely to clear them. Distinguish documentation fixes, code fixes, runtime regressions and image retests in status reports.

See [series example](../examples/08-style-lock-series.md) and [same-frame example](../examples/09-character-in-scene.md). They illustrate an optional BJD project, not universal defaults.
