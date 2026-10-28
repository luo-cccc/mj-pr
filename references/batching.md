# Batching and Discord permutations

Adapted from `georgespelllens/mj-agent` (MIT). Use for variations, themed sets, permutation packing, command splitting and version comparisons. Follow user intent before inherited examples.

## Generate variations

1. Parse the subject/core, variable details and parameter suffix.
2. Preserve the user's requested count and suffix. Default to **ten variations only when the count is absent**.
3. Vary only the requested axes. If none are named, choose one useful axis and state it; do not expand every detail at once.
4. Preserve project invariants and the requested prompt language. English is a fallback, not a requirement.
5. Deliver RAW lines or PERMUTATION commands as requested. Supply both only when useful; do not force duplicates.

For an unspecified themed batch, use the same ten-item default. Do not silently expand a theme into fifty jobs. Use supplied valid profiles and IDs; do not invent account settings.

## Pack and split

Group identical suffixes. Move genuinely shared text outside braces. Escape literal commas **inside alternatives** with `\,`; unescaped commas there separate alternatives. Do not escape separator commas or ordinary commas outside alternatives.

Count jobs as the Cartesian product of all alternative groups, including parameter groups. Two groups of 3 and 2 produce six jobs, not five. Count after parsing escaped commas. Count the actual full command, including `/imagine prompt:`, whitespace, escapes, braces, URLs and suffix. Keep every command at **2,000 characters or fewer** for these Discord demos; leave room if surrounding text will be pasted with it. Report the measured length and expanded jobs per command.

Split to both the user's plan/job cap and message length. If the plan is unknown, use conservative chunks of **at most four jobs**; split ten alternatives as 4 + 4 + 2. Preserve exactly the requested outputs without accidental Cartesian combinations, duplication or loss. Do not rely on rough word-count estimates. When suffixes differ, keep separate groups rather than changing the user's parameters.

Official [Permutations documentation](https://docs.midjourney.com/hc/en-us/articles/32761322355597-Permutations), checked **2026-10-28**, supports both the website Imagine bar and Discord. Per-submission prompt caps are **Basic 4, Standard 10, Pro/Mega 40**. Permutations require Fast or Turbo and are unavailable in Relax; the selected model must also support that speed mode (V8.1 does not support Turbo). Each expanded prompt consumes GPU time. Discord presents a confirmation step. Do not submit jobs without a generation request.

The four-job unknown-plan fallback is house packing guidance aligned with the documented Basic cap; it does not prove an account has remaining GPU time or access. The official permutations page does not specify a command-length limit. The **2,000-character budget is a conservative policy for this repository's Discord demos**, not a verified universal Midjourney input limit. The website may have different input constraints.

## Executable preflight

Use the [validator](../scripts/validate_prompt.py) to expand and check every alternative, including nested groups and escaped commas. For a ten-job unknown-plan Discord batch, save commands as one `/imagine prompt:` line each and run:

```bash
python scripts/validate_prompt.py --mode style --file commands.txt --expected-count 10 --max-jobs 4 --max-chars 2000 --json
```

`--expected-count` checks total jobs across commands, including `--repeat` / `--r`. `--max-jobs` applies to each command; `--max-chars` counts the entire command. Adjust limits to the selected interface and account. Expansion is bounded to 256 variants and 32 nesting levels per command. Duplicate expanded prompts produce review advice. Do not change the requested count merely to satisfy a limit: split commands. This validates packaging and text, not account access, parameter compatibility or generated-image quality.

## Version A/B

Verify both model versions and each flag's compatibility first using [parameters.md](parameters.md). A version permutation is suitable only after that check; otherwise provide separate conditional templates or clearly label inherited version labels unverified. Count the version alternatives in the job product. Same seed helps comparison but does not guarantee matched composition or equivalence across versions.

Quoted image text is a descriptive technique rather than an established V8.x-only rule. Keep desired lettering, labels and logos out of negative banks. Inspect rendering fidelity instead of promising exact typography.

## Worked examples

These preserve inherited visual themes as concrete style examples, not universal recipes or model-support evidence. Version pins were omitted rather than asserting an unverified live version. Their remaining flags are illustrative and require target-model verification. Every demo is split into 4 + 4 + 2 jobs, with measured command lengths.

- [Floral portraits](../examples/batches/01-floral-portraits.md)
- [Band posters](../examples/batches/02-band-posters.md)
- [Mythical pairings](../examples/batches/03-mythical-pairings.md)
- [Anime aesthetics](../examples/batches/04-anime-girls-aesthetics.md)
- [Mannequin heads](../examples/batches/05-mannequin-heads.md)
- [Anthropomorphic selfies](../examples/batches/06-anthropomorphic-selfies.md)
