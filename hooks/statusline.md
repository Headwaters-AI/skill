# The state in Claude Code's status line

The status line shows the HUD in one line, for the human. It costs no model tokens: Claude
never sees it.

Add this to `~/.claude/settings.json` (or a project's `.claude/settings.json`):

```json
{
  "statusLine": {
    "type": "command",
    "command": "hwai state:hud --hook statusline",
    "refreshInterval": 30
  }
}
```

It reads the directory from the status line's JSON on stdin (`workspace.current_dir`), cuts
the line to the terminal width (`COLUMNS`), and prints nothing when there is no state (in
`auto`), when `hwai state:hud off` is set, or on any error. A status line that prints nothing
goes blank.

Claude Code runs the command when a session starts, after each assistant message and on a few
other events (debounced 300 ms). `refreshInterval` also re-runs it every 30 seconds, so writes by
other agents show while this session is idle. Leave it out to run on events only.

Example:

```
fs_QPSO… · "the dinner is planned" · open · 1/7 proved · next: 1.2.1 pasta primavera · waiting: human on 1.3
```

## A plugin cannot set it

A plugin ships skills, commands, agents, hooks, MCP and LSP servers, output styles, themes,
monitors, workflows and `bin/` executables; `statusLine` is not among the plugin components or
manifest fields (https://code.claude.com/docs/en/plugins-reference, the Fields table and the
Standard layout; https://code.claude.com/docs/en/plugins/components.md). `statusLine` is a user
or project setting (https://code.claude.com/docs/en/statusline, "Manually configure a status
line"). So the user, or the agent with the user's OK, adds the snippet above by hand; installing
the skill does not.

Your settings hold one `statusLine`. If one is already set, keep it and add the HUD to its
script (for example, pipe the same stdin to `hwai state:hud --hook statusline` and print its line
as one more row: each line a script prints is its own row).
