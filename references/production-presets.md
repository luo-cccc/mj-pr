# Production presets

## Evidence and priority

Screenshot-visible choices are house conventions, not official MJ requirements. Six style names were visible; the English blocks and parameter suggestions below were authored here. Explicit user constraints override presets. Check [parameters.md](parameters.md) for version-sensitive requests. Never copy unresolved placeholders into a real command.

## Optional defaults

| Deliverable | Fallback when unspecified |
|---|---|
| Full-body humanoid sheet | neutral pose, white background, 9:16, intended body parts framed |
| Turnaround | front/side/back panels, matching scale, neutral pose |
| Environment plate | wide composition, 16:9, unoccupied unless people requested |
| Character/environment composition | narrative framing with [shared art direction](style-lock.md#7-character-and-environment-in-one-frame) |

Custom ratios, bare feet, concealed hands, nonhuman anatomy, populated scenes and custom styles are valid. A portrait is not a full-body sheet; a single standing view is not a turnaround.

## Assembly

For humanoid sheets: head/face → upper garments → hands/arms → lower garments → feet. Fill relevant slots only. Describe full-body margins when needed, and barefoot anatomy when shoes are not intended. Name actual hand placement rather than mechanically requiring two visible hands.

For turnarounds: explicitly name view count/order, matching scale and neutral pose. Inspect orientation, proportions and costume continuity in the final image; prompts cannot guarantee correct orthographic views. Separate views may be easier to revise than one combined sheet.

For environments: scene type → layout/viewpoint → surfaces → light/palette → atmosphere. Describe spatial relationships and stable landmarks. An empty plate can say `unoccupied courtyard`; add `--no people` only when appropriate. Crowd scenes must not inherit an exclusion for people.

Lens, aperture and shutter terms are stylistic descriptors, not physically enforced optics. Use them when they serve the requested medium; do not add a lens to every ink painting.

## Output and parameters

Default to a copyable prompt. A Chinese translation is useful for Chinese-speaking teams but can be omitted or changed. Order parameters consistently for readability; their order is not an artistic law. Do not force a version or personalization profile. Use only supplied valid IDs and supported syntax.

## Six optional style libraries

Names came from screenshots; blocks and numeric suggestions are untested starting points. Select relevant traits, not every word. Subject-specific details must not leak into unrelated assets. Negative bank definitions live only in [lexicons.md](lexicons.md#negative-banks-no-presets).

| Style | Rendering vocabulary | Starting parameter suggestion | Optional bank |
|---|---|---|---|
| 写实电影 CG | `cinematic CG render, physically based materials, dimensional soft lighting, restrained film grain` | `--raw --s 100` | F1 |
| 中国水墨仙侠 | `Chinese ink wash, rice paper texture, ink gradients, cyan and ink black with vermilion accents` | `--s 250` | F2 |
| 暗黑废土科幻 | `dark wasteland science fiction, weathered metal, toxic haze, desaturated olive and rust palette` | `--raw --s 80` | F3 |
| 史诗古战场 | `ancient battlefield atmosphere, bronze and iron, dust and smoke, worn banners` | `--raw --s 60` | F4 |
| 自然柔美 | `soft natural light, gentle color transitions, quiet organic atmosphere` | `--s 220` | F5 |
| 中国风山水 | `Chinese shanshui, layered mountains, ink gradients, atmospheric negative space` | `--s 280` | F6 |

These values are not measured optima. Verify flag support and tune only when output warrants it. A style is not a command to add troops, flowers or mountains to every image.

## Review, not taboo enforcement

Prefer concrete descriptions and coherent art direction. Hyphens, camera terminology, deep focus, different color temperatures and quality descriptors are not inherently invalid. Remove or change words to address an observed issue, rather than to satisfy an arbitrary blacklist.

For full-body framing, shoes and hand poses are useful descriptive choices, not guarantees against cropping or anatomical defects. Avoid suppressing body parts to repair them. Negative exclusions may affect each word independently; inspect the actual intended semantics.

## Examples and checks

Read [character example](../examples/06-production-character.md) or [scene example](../examples/07-production-scene.md) only for that selected preset.

Run [validate_prompt.py](../scripts/validate_prompt.py) with `--mode character`, `--mode scene` or `--mode style` and `--file prompt.txt`. Resolve syntax failures and interpret warnings against the brief. Text checks cannot establish visual quality, real model support or continuity.
