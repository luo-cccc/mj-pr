# Revision playbook

Revise against the user's complaint and actual pixels. Preserve the brief, requested count, language and suffix; change only what addresses the problem. Parameter changes below are optional starting hypotheses and require [model support](parameters.md).

Review in this order: explicit user requirements, semantic conflicts, composition/lighting/materials/character/environment, and actual-output acceptance. Separate a confirmed requirement conflict from an intentional artistic choice. Static WARN messages are review prompts, not orders to rewrite; clearing them is not a quality goal. Without an output, propose a revision hypothesis and leave visual acceptance unverified.

| User signal | Targeted revision |
|---|---|
| Too poetic or artsy | If realism is intended, reduce conflicting medium cues and describe actual surfaces/light; optionally try RAW or lower stylize |
| Want grandeur | Add spatial anchors, foreground scale references or tiny traffic; widen the ratio only if allowed |
| Unwanted cameras/tripods appear | Rephrase the ambiguous gear cue for this image; consider selected A2 exclusions from the canonical bank. Camera words are allowed, and desired selfie/studio gear stays |
| Too many split scenes | For a single-image brief, choose one decisive moment; preserve panels or sequential composition when requested |
| Wrong protagonist | Name identity, role and action clearly; reduce competing subjects or verify supplied identity references |
| Want 唯美 / aesthetic | Select soft light, graceful forms or a suitable palette; RAW and stylize remain optional |
| Want Chinese classical | Specify architecture, costume and era; consider D1 only for unwanted motifs, preserving deliberate hybrids |
| Want people in frame | State role, costume, action and placement; remove people exclusions; avoid likeness guarantees |
| Subject feels weak | Improve staging, silhouette or local contrast; choose focus separation only if appropriate |
| Figure looks pasted on | Check scale, perspective, contact shadows, reflections and motivated lighting; sharp backgrounds can remain |
| Subject merges with scenery | Try color grouping, edge control, detail allocation, staging or focus. A bright background or different skin/robe hue is not itself a defect |
| Unwanted synthetic skin | Describe the intended material; consider B3 only if plastic/resin is unwanted, never automatically on BJD |

Read candidate banks in [lexicons.md](lexicons.md#negative-banks-no-presets) before using them. IDs are internal labels, not MJ syntax. Do not suppress hands to repair anatomy or text when lettering is requested. Multiword exclusions and hyphens are not syntax failures.

Offer one revised prompt and a short reason by default; give variants or longer sets when requested. For a generation comparison, retain the actual model/version and interface, raw submitted prompt including references/parameters, job ID or output file, and itemized visual observations against the complaint and brief. Keep before/after evidence identifiable; label missing evidence unverified. Change one relevant variable when testing a causal hypothesis. If multiple variables change, assess the combined revision without assigning the result to one phrase or parameter. Numeric observations need a stated method, regions and limits; do not turn them into universal thresholds.

Report documentation fixes, code fixes, runtime regressions and image retests separately. Text lint and passing regressions cannot certify a visual fix. Inspect the next actual result and record requirement-by-requirement acceptance before claiming improvement or continuity; otherwise mark the image retest pending.
