# Parameters — official documentation snapshot

Checked **2026-10-28** against the official sources linked below. These are documentation-backed claims, not results from live Midjourney generation. Account access, UI changes and model-specific omissions still require checking for a version-sensitive request.

## Model selection

The official [Version page](https://docs.midjourney.com/hc/en-us/articles/32199405667853-Version) identifies **V8.2 as the default since July 24, 2026**. V8.1 was released April 14, 2026; V7 on April 3, 2025; Niji 7 on January 9, 2026. V8.0 early access ended July 24, 2026 and is no longer selectable. Select an available model with `--v`, or use the website/Discord settings. Use `--niji 7` for the documented anime model. Preserve the user's requested model; do not silently replace an unavailable one.

V8.1/V8.2 support SD/HD workflows. The Version comparison lists a maximum aspect ratio of 14:1 for V6, V7 and V8.1/V8.2, with V8.1/V8.2 HD limited to 4:1. Treat the limits symmetrically for wide and tall output. Extreme ratios remain experimental. V8.1 access may require unlocking the Global V7/V8 Personalization profile; check account access rather than promising availability.

Put supported parameters after the description. A space before `--` separates a parameter from text. Commas in `--no` lists and punctuation in URLs are legitimate. Descriptive hyphens and camera terminology are allowed.

## Parameter reference

| Parameter | Documented behavior | Scope / caution |
|---|---|---|
| `--ar` / `--aspect` | Whole-number width:height; default 1:1 | `85:110`, not `8.5:11`; limits depend on model and resolution |
| `--v` / `--version` | Select model | Current documented default V8.2; explicit user selection wins |
| `--niji` | Anime-oriented model selector | Niji 7 documented; do not combine incompatible model selectors |
| `--s` / `--stylize` | 0–1000; default 100 for latest versions | Creative choice, not a required photography/illustration setting |
| `--raw` | Reduce automatic styling for closer prompt control | Optional; also documented with Edit Model |
| `--c` / `--chaos` | 0–100; default 0 | Higher values increase variety and unpredictability |
| `--w` / `--weird` | 0–3000; default 0; V5 onward | Seed compatibility is incomplete; do not promise repeatability |
| `--no` | Comma-separated exclusions | Words are interpreted independently; multiword entries are legal but can remove unintended concepts |
| `--q` / `--quality` | V7: 1 (default), 2, 4; 3 maps to 4 | Initial grid only; V7 q4 cannot combine with Omni Reference. Quality page does not establish V8.1/V8.2 values; omit rather than extrapolate |
| `--seed` | Controlled comparison aid | Does not guarantee identical identity/layout or cross-version repeatability |
| `--iw` | Default 1; V7/V8.1 range 0–3; Niji 7 range 0–2 | Image Prompts table does not separately list V8.2; do not assume its range |
| `--sref`, `--sw`, `--sv` | Style reference; sw 0–1000, default 100 | V6 onward; sv is model-specific; sw/sv do not work with Moodboards. See [image-and-style.md](image-and-style.md) |
| `--edit` | Instruction-based generation/editing with up to four reference images | V8.1/V8.2; references follow `--edit` in Discord; no tile or Remix. See [image-and-style.md](image-and-style.md) |
| `--cref`, `--oref` | Older character/object reference workflows | V8 Edit Model supersedes these workflows; V7 introduced Omni Reference. Do not declare older-model mechanisms globally retired |
| `--tile` | Repeatable patterns | Check target model; not supported by Edit Model |
| `--p` / `--profile` | Personalization profiles / Moodboards | Bare `--p` uses selected defaults after profile unlock; IDs select specific profiles. Account-specific; never invent IDs |
| `--hd`, `--sd` | V8 resolution controls | Parameter List explicitly describes V8.1 2048px/1024px; Version page groups V8.1/V8.2 HD support. Do not infer costs from dimensions |
| `--draft` | Reduced-cost previews | Parameter List documents V7 at half GPU cost; other pages mention V8.1 draft without a complete cost/support specification. Verify target model; do not transfer V7 economics |
| `--repeat` / `--r` | Repeat a prompt | Account/model limits require separate checking; include repeats when budgeting actual work |
| `--fast`, `--relax`, `--turbo` | Speed modes | Account/model dependent. Speed page explicitly excludes V8.1 Turbo; it does not establish V8.2 Turbo support |
| `--stealth`, `--public` | Website visibility | Account/interface dependent |
| `--video`, motion/loop/end/bs options | Video workflow | Verify separately for a video request; not certified by this image-focused snapshot |

## Editing and references

The Version page describes the Edit Model as replacing Omni Reference, Character Reference and Retexture in the newer workflow. The dedicated Edit Model page explicitly supports **V8.1 and V8.2**. This is a scoped migration, not proof that `--cref` or `--oref` has been removed from every older version. Choose the mechanism documented for the user's model.

## Aspect suggestions

Use `1:1` for square, `2:3` or `3:4` for portrait, `16:9` for landscape, `21:9` for panorama, and `9:16` for vertical delivery when they fit the brief. Preserve an explicit user ratio. RAW and stylize are creative controls, not requirements for any medium.

## Sources and remaining gaps

Official pages checked on **2026-10-28**:

- [Version](https://docs.midjourney.com/hc/en-us/articles/32199405667853-Version): default, release history, model comparison and HD limits.
- [Parameter List](https://docs.midjourney.com/hc/en-us/articles/32859204029709-Parameter-List): parameter names and short feature descriptions.
- [Aspect Ratio](https://docs.midjourney.com/hc/en-us/articles/31894244298125-Aspect-Ratio): integer syntax, default and extreme-ratio caution.
- [Stylize](https://docs.midjourney.com/hc/en-us/articles/32196176868109-Stylize), [Chaos / Variety](https://docs.midjourney.com/hc/en-us/articles/32099348346765-Chaos-Variety), [Weird](https://docs.midjourney.com/hc/en-us/articles/32390120435085-Weird): ranges, defaults and Weird seed caveat.
- [No](https://docs.midjourney.com/hc/en-us/articles/32173351982093-No): exclusions and independent word interpretation.
- [Quality](https://docs.midjourney.com/hc/en-us/articles/32176522101773-Quality): V7 values and Omni incompatibility; no V8 quality range supplied.
- [Image Prompts](https://docs.midjourney.com/hc/en-us/articles/32040250122381-Image-Prompts): input syntax and model-specific iw table.
- [Style Reference](https://docs.midjourney.com/hc/en-us/articles/32180011136653-Style-Reference): sw/sv and Moodboard limits.
- [Edit Model References](https://docs.midjourney.com/hc/en-us/articles/48495453462797): V8.1/V8.2, four references, syntax and limitations.
- [Fast, Relax and Turbo](https://docs.midjourney.com/hc/en-us/articles/32016412137741): speed/account conditions and V8.1 Turbo exception.
- [Permutations](https://docs.midjourney.com/hc/en-us/articles/32761322355597-Permutations): interface, modes and subscription caps; summarized in [batching.md](batching.md).

The pages are not a fully synchronized compatibility matrix: some list V8.1 or V7 while newer pages mention V8.2. Missing entries are **unspecified**, not evidence of either support or rejection. Verify omitted compatibility before including an optional flag. GPU prices, live account entitlements and generated-image quality are not certified here.

Not affiliated with Midjourney, Inc.
