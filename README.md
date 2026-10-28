# Midjourney Prompt Suite

An agent skill for writing, refining and batching Midjourney prompts. **Version 3.1.0.** User requirements take priority over project defaults and optional presets. The skill delivers prompts; image generation requires an explicit request.

## Capabilities

- Prompt craft and targeted revision from image feedback.
- Character sheets, turnarounds and scene plates with six optional production styles.
- Series consistency and coherent character/environment compositions.
- Permutation expansion, repeat accounting, count preservation and command budgets.
- Text syntax checks and conservative semantic-conflict advice without prescribing artistic choices.

Official documentation was checked on **2026-10-28**. The Version page identifies V8.2 as the default at that date. Some pages omit V8.2-specific parameter ranges; see [parameters](references/parameters.md) for sources, exact model scopes and remaining gaps. Documentation verification is separate from generated-image testing.

## Install

Copy or clone the repository into a skill directory with the name `midjourney-prompt-suite`:

```bash
git clone https://github.com/luo-cccc/mj-pr.git ~/.zcode/skills/midjourney-prompt-suite
```

Reload skill discovery or restart the client as required. For project-local use, place it under `.agents/skills/midjourney-prompt-suite/` or the directory supported by your agent.

## Use

Ask the agent for a prompt, revision, asset sheet or batch, for example:

- “写一段古风剑客提示词，水墨风格，横构图。”
- “把这十条提示词打包为排列组合，每条命令最多四个任务。”
- “设计角色正侧背三视图，保留已有服装和身份特征。”

[SKILL.md](SKILL.md) routes the agent to references on demand. Optional [production presets](references/production-presets.md), [vocabulary and negative banks](references/lexicons.md), [series guidance](references/style-lock.md) and [batching](references/batching.md) provide reusable guidance and examples. BJD is selected only when it fits the brief.

## Local validation

Requires **Python 3.9+**, with no third-party runtime dependencies.

```bash
python scripts/validate_prompt.py --mode character --file prompt.txt
python scripts/validate_prompt.py --mode style --file commands.txt --expected-count 10 --max-jobs 4 --max-chars 2000 --json
python -m unittest discover -s scripts -p 'test_*.py' -v
python scripts/audit_links.py --strict
```

Modes are `character`, `scene` and `style`. Multi-command files contain one `/imagine prompt:` command per nonblank line. Count budgets include repeats. FAIL indicates malformed input or a supplied operational limit violation; WARN invites contextual review. Exit codes: 0 for no FAIL, 1 for validation failure, 2 for usage errors.

Text checks cannot certify model compatibility, account access or image quality. The English semantic heuristics do not understand every phrase or subject-specific scope. Actual output must be inspected for anatomy, identity, composition and continuity. See [maintenance](references/maintenance.md) and the current [validation record](REVIEW.md).

## Attribution

Adapted from the MIT-licensed `HaaaappyDay/midjourney-prompt-engineering` and `georgespelllens/mj-agent` projects. Preserve [NOTICE.md](NOTICE.md) and [LICENSE](LICENSE) when redistributing. Not affiliated with Midjourney, Inc.
