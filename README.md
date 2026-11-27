# Headwaters skill

The agent skill for Headwaters: tools for working in causal space.

- **Causal state** (`hwai state:*`): turn a task into a proof you can check at any moment.
- **Maestro** (`hwai maestro:*`): an upstream encoder that reads a state through a face and steers any decoder: choices, a decision model or a chat model.
- **Faces** (`hwai face:*`): masks on causal space, compiled from source texts, each encoding a taste and judgement.

The skill is in `skills/headwaters-ai/`. The hooks in `hooks/` keep the directory's causal state in view (Claude Code through the plugin, Codex through `hooks/codex.toml`). `drafts/` holds working drafts of the skill; they are not loaded.

Install the CLI with `npm install -g @headwaters-ai/cli` (the command is `hwai`), then start from `skills/headwaters-ai/references/QUICKSTART.md`.
