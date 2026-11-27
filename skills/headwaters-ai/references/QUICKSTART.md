# Quickstart

From nothing to a face's first choices, from the terminal. Follow the steps in order.

**Claude Code only:** right after the skill is installed, its slash commands do not load until the session restarts. You cannot restart it yourself, so tell the user: *"Type `/exit`, then run `claude --continue` so the new skills load and we pick up where we left off."* Other agents load new skills without a restart.

> TODO (#2080): the hosts below serve only after the move to headwaters.ai. Until then the API is `https://api.faces.sh`.

**Website:** https://headwaters.ai · **API:** https://api.headwaters.ai (schema: https://api.headwaters.ai/openapi.json)

## 1. Install or update the CLI

```bash
npm install -g hwai@latest
hwai --version
```

The same command installs the CLI or updates it.

## 2. Sign in, or sign up

Ask the user where they are starting from:

> To use Maestro you need a Headwaters account. Where are you starting from?
>
> A) I have an account, and I'll log in now
> B) I have an API key, and I'll paste it
> C) I need an account: help me create one here
> D) I'll register at headwaters.ai myself and come back

**A (log in):**
```bash
hwai account:login --email USER_EMAIL --password 'USER_PASSWORD'
hwai account:whoami
```

**B (API key):**
```bash
hwai config:set api_key <key>        # or set HEADWATERS_API_KEY in the environment
hwai account:whoami
```

**C (sign up here):** ask which plan:

> There are three plans. Which fits you?
>
> A) **Free**: add credit to start, then everything is paid as it goes. No monthly fee. Good for trying it out.
> B) **Connect ($17/month)**: monthly allowances for compiling and for Maestro, and eligible chat models run on your linked ChatGPT plan. Anything past the allowances is paid as it goes.
> C) **Pro ($49/month)**: Connect with larger allowances.

Prices and allowances change: check `GET /v1/rates` before quoting them. Then register:

```bash
# Free
RESULT=$(hwai account:register --email USER_EMAIL --password 'USER_PASSWORD' --username USERNAME --json)
echo "$RESULT" | jq -r '.checkout_url'

# Connect or Pro
RESULT=$(hwai account:register --email USER_EMAIL --password 'USER_PASSWORD' --username USERNAME --plan connect --json)   # or --plan pro
echo "$RESULT" | jq -r '.checkout_url'
```

The username is 1 to 32 characters: a lowercase letter, then lowercase letters, numbers or underscores. It becomes the owner name in every model string, `@username~face`. The password needs 8 to 64 characters, with an uppercase letter, a lowercase letter and a digit. If the checkout link could not be fetched, `checkout_url` is missing and `checkout_error` says why.

Ask the user to open the checkout link in their browser and pay. When they confirm:

```bash
hwai account:balance --json | jq '.is_active'
```

`true`: carry on. `false`: the payment may not have gone through; ask them to try the link again.

**D (sign up themselves):** ask them to register at headwaters.ai and come back with their login or an API key.

## 3. A key for programs

```bash
hwai key:create --name "my-key"
```

A program or another agent uses it as `HEADWATERS_API_KEY`.

## 4. Your face

Every account already has a face of its own, aliased **`me`**. To build the user's own face, compile into `me` rather than creating another. For anyone else, create a face; see `FACES.md`.

## 5. Add a source, and compile

Decide first whether it is a **document** (one author's own writing) or a **thread** (a conversation, interview or transcript, where only one named speaker is the face). Every document needs a `--medium` (`email`, `text message`, `social post`, `essay`, `academic paper`, `blog post`, `legal document`, `thread reply`, `conversation`, `lecture` or `other`), and every source a `--perspective`: `first-person` for their own words, `third-person` for writing about them. Ask the user when you do not know; never guess.

```bash
hwai face:compile me --file essay.txt --medium essay --perspective first-person
hwai face:compile me --file interview.txt --kind thread --face-speaker "Sam"
hwai face:import me --url "https://www.youtube.com/watch?v=VIDEO_ID"   # a video, transcribed on the server
```

`hwai face:compile` waits for the compile to finish. If it times out, it exits with an error that says the compile is still queued or running; check it with `hwai face:compile:status`. A face runs at most 3 compiles at once, and more wait their turn.

## 6. Ask it

```bash
hwai maestro:choices --face @USERNAME~me --state "A startup offers me a lead role at a lower salary." \
  --question "Should I take the offer?"                       # the options the face would weigh
hwai maestro:choices --face @USERNAME~me --state "A startup offers me a lead role at a lower salary."   # the question it would ask
```

The options come strongest first, in the face's own terms. For a situation longer than 3,000 tokens, or one your agent keeps building, use a causal state (`STATES.md`).

## 7. Keep the state in view

So that you, and the next session, see where the work stands without having to remember to look:

1. **Install the hooks.** In Claude Code they come with the plugin. In Codex, add `hooks/codex.toml` to `~/.codex/config.toml` (see `SETUP.md`). They show the state at session start, on each user message and on each stop.
2. **Offer the status line** (Claude Code only; a plugin cannot set it). With the user's OK, add the snippet in `hooks/statusline.md` to their `~/.claude/settings.json`.
3. **Offer a project note.** With the user's OK, append this to the harness's instruction file (`CLAUDE.md` for Claude Code, `AGENTS.md` for Codex and most others, `GEMINI.md` for Gemini CLI, `.cursor/rules/headwaters.mdc` for Cursor). Never overwrite the file, and keep the markers so the note is never added twice:

```markdown
<!-- headwaters:start -->
## Causal state (Headwaters)
This project keeps a causal state for long work (`.headwaters/state`).
- At the start of a session, run `hwai state:get` and pick up from its last line.
- For work with several steps, tradeoffs, or goals the user gave you, add the goal and refine it before you start. Skip it for one-step tasks.
- When something happens (an answer, a test run, a new instruction), record it with `hwai state:add` or `hwai state:edit`.
<!-- headwaters:end -->
```

4. **If your harness keeps a memory,** save what you learned here that you would otherwise have to ask again: the username, the faces and what each is for, any budget the user agreed. Don't save instructions to use Headwaters; the note and the hooks do that.

> TODO (#2091): `hwai state:hud`, which the user-message hook and the status line call, ships with the next CLI release.

## What's next

- **Steer a decision:** `hwai maestro:decide --face @USERNAME~me --state "…" --question "…"`.
- **Steer a reply:** `hwai maestro:chat --face @USERNAME~me` with any chat model as the decoder.
- **More faces, and finding public ones:** `FACES.md`.
- **Work on a task as a proof:** `STATES.md`.
- **Connect ChatGPT** (Connect or Pro): `hwai account:connect openai`.
