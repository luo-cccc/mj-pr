# Image inputs and style references

Official documentation checked **2026-10-28**. See [parameters.md](parameters.md) for the central model snapshot and unresolved compatibility gaps. Documentation verification does not certify generated identity or visual quality.

## Image prompts

In Discord, put publicly accessible image URLs before the text, followed by parameters. On the website, upload/select images with the Imagine bar image button. Use actual user-supplied or approved references; never invent URLs. Supported extensions are `.png`, `.gif`, `.webp`, `.jpg`, `.jpeg`.

Use at least two images, or one image plus text. Describe the desired final picture rather than giving image-edit instructions; use Edit Model or Editor for targeted modifications. Crop near the target aspect ratio when useful without losing important anchors. Image prompts guide a new result rather than reproduce a source precisely.

The Image Prompts table lists `--iw` default 1, range 0–3 for V7/V8.1 and 0–2 for Niji 7. It does not separately list V8.2. Image-only submissions cannot use `--stylize` or `--weird`. Check the selected model before promising additional combinations or limits.

## Style reference

`--sref` guides medium, texture, palette and lighting. It works with V6 onward and requires accompanying text. It can combine with image prompts and Edit Model references. It is not an identity guarantee, and reference content may influence the result.

On the website, put selected images in the style-reference area. In Discord, append `--sref` followed by accessible image URLs separated by spaces. Relative image weighting is documented as `--sref URL1::2 URL2::1`; URL1/URL2 here are placeholders, not runnable inputs.

- `--sw`: 0–1000, default 100, for reference images and numeric style codes.
- V7 image references: `--sv` 1–6, default 6. V7 codes/random support sv 4 or 6. sv 4 selects the V7 implementation from before June 16, 2025.
- V6: `--sv` 1–4, default 4. Do not transfer these selectors or defaults to V8.2; the page does not supply a V8-specific sv table.
- `--sref <code>` uses a numeric style-library identifier. `--sref random` selects an identifier; rerolls and variations retain it, while permutations/repeats can select different identifiers.
- Multiple codes and images can be combined. An uploaded reference image cannot be converted into a style code. Never invent a code or account profile.
- **Neither `--sw` nor `--sv` works with Moodboards.**

## Identity and editing

For **V8.1/V8.2**, the Edit Model supports instructions and up to **four reference images**. On the website use attached references, Quick Edit or Editor. In Discord, place image URLs after `--edit`, separated by spaces. Output proportions generally follow the first reference; use explicit `--ar` to override, because account aspect defaults do not apply automatically.

Edit Model can combine with image prompts, style references, Moodboards, Personalization and `--hd`. `--raw` can reduce added styling. It does not support `--tile`, and its outputs cannot use Remix. The dedicated page does not document reference-weight controls; do not invent an edit weight or reuse Omni weights without evidence.

The newer workflow supersedes Omni Reference and Character Reference; the Version page also identifies Retexture as replaced. This does not establish global retirement on older versions: V7 introduced Omni Reference, and older mechanisms must be selected according to their own model documentation. Style, identity and editing references serve different purposes. Inspect actual outputs before claiming continuity.

## Official sources

Checked 2026-10-28: [Image Prompts](https://docs.midjourney.com/hc/en-us/articles/32040250122381-Image-Prompts), [Style Reference](https://docs.midjourney.com/hc/en-us/articles/32180011136653-Style-Reference), [Edit Model References](https://docs.midjourney.com/hc/en-us/articles/48495453462797), [Parameter List](https://docs.midjourney.com/hc/en-us/articles/32859204029709-Parameter-List), [Version](https://docs.midjourney.com/hc/en-us/articles/32199405667853-Version).
