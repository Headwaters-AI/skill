# Setup

## The CLI

```
npm install -g @headwaters-ai/cli     # needs Node 20 or later; the command is hwai
hwai --version
```

## A key

```
hwai account:register        # a new account (or hwai account:login for an existing one)
hwai key:create          # a key for programs
```

For a new user, `QUICKSTART.md` walks through signing up, the plans and payment step by step.

Or set `HEADWATERS_API_KEY` in the environment that runs the agent. `HEADWATERS_BASE_URL` points the CLI at another API host; it defaults to the live API.

> TODO (#2082, #2080): the package, the config directory and the default API host are set by the `hwai` CLI as built, and by the move to headwaters.ai. Check this page against `hwai --help` once #2082 is dogfooded.

## The skill

```
npx skills add headwaters-ai/skill
```

> TODO (#2080): the skill's repo name in the Headwaters-AI org.

## The hooks

The hooks keep an agent aware of its causal state. None of them ever blocks the agent.

| hook | what it does |
|---|---|
| session start | prints the tree of the directory's state, or says there is none |
| stop | prints the state's last line |
| session end | releases the session's claims (Claude Code only; in Codex, claims expire after 30 minutes) |

**Claude Code:** the hooks come with the plugin, installed with the skill.

**Codex:** add the hooks from the skill repo's `hooks/codex.toml` to `~/.codex/config.toml`, pointing at where you cloned the repo, then approve them when Codex asks. Codex's sandbox needs network access for the CLI to reach the API: under `[sandbox_workspace_write]`, set `network_access = true`.

## Checking it works

In an empty project directory:

```
hwai state:create --use
hwai state:add "it works" "The CLI reaches the API" --role goal
hwai state:get
```

The tree prints with one open goal.
