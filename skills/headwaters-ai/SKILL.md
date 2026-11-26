---
name: headwaters-ai
license: MIT
description: >
  Headwaters integration craft for Maestro, an upstream encoder that reads a state through a face
  (a mask compiled from source texts) and steers a downstream decoder: choices, a decision model
  such as Jev, or a chat model. Use when decomposing long-running work into a causal state, deciding
  when to work, wait or ask, dispatching pieces of work to the right model, distilling judgement or
  lessons into a face, building or debugging code that calls the Headwaters API or the `hw` CLI, or
  when one or more specific perspectives help with brainstorming, troubleshooting, targeted
  messaging, or comparison.
---
# Headwaters

Headwaters gives AI a way to work in **causal space**: the space of directional dependencies that explain why one state gives rise to another, and what it will lead to. Most AI tools work in the space of resemblance, finding what looks like what. Headwaters tools works in the space of cause, finding what produces what. That is what judgement, taste and discernment rest on.

Headwaters has three tools for working in causal space:

- **Causal state** is a map: where you are, where the goal is, and how best to get there.
- **Faces** are masks on causal space: each one encodes a particular taste and judgement.
- **Maestro** is the encoder that brings them together: it reads a state through a face into causal `why code` and uses them to steer various  models: choices, decisions, chat.

```
state ─▶ [ face ▸ Maestro ] ─why code ─▶ decoder ─▶ choices · decision · chat
   ▲                                                        │
   └────────────── the results update the state ────────────┘
```

`hw` is the Headwaters CLI. Commands are grouped by topic, as `hw topic:command`.


| topic                 | function                 | commands                                                                                                                                                                          |
| --------------------- | ------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`face`](#face)       | mask                     | `face:create`, `face:list`, `face:compile`, `face:import`, `face:publish`, `face:share`, `face:edit`, `face:delete`                                                               |
| [`maestro`](#maestro) | inference                | `maestro:choices`, `maestro:decide`, `maestro:chat`                                                                                                                               |
| [`state`](#state)     | memory                   | `state:create`, `state:use`, `state:get`, `state:add`, `state:edit`, `state:delete`, `state:claim`, `state:refine`, `state:choices`, `state:decide`, `state:items`, `state:close` |
| [`account`](#account) | sign-in, plan and credit | `account:register`, `account:login`, `account:whoami`, `account:balance`, `account:topup`, `account:usage`, `account:plan`, `account:connect`, `account:show`                     |
| [`key`](#key)         | API keys                 | `key:create`, `key:list`, `key:edit`, `key:revoke`                                                                                                                                |
| `config`              | local settings for `hw`  | `config:set`, `config:show`, `config:clear`                                                                                                                                       |


Every command takes `--help`, and `--json` for machine-readable output. The full manual is in `references/CLI.md`.

> TODO (#2082): generate `references/CLI.md` from `hw --help` for every command, with a script run at each CLI release, so the manual can never drift from the CLI.


## Causal state (`hw state:*`)

**Turn a task into a proof you can check at any moment.** A causal state is like a todo list that has to be proved: each goal is broken into what it depends on, and a box is checked only when a test passes or the human confirms it. Ask it at any point whether you are on track, and it tells you, from the proof rather than from your recollection.

It keeps you from the usual failures of long work:

- **calling it done too early:** the goal is proved only when everything under it is;
- **losing what the user asked for:** their words stay on the premises they came from;
- **dropping alternatives:** a failed option is refuted, and the next one comes up;
- **asking too much or too little:** a premise waits on the human only when only they can settle it;
- **stopping at the wrong time:** the last line says act, wait or ask.

Reading and writing it is free, and its output is short. It works alongside your harness's own todo list: use the todo list for steps, and the state for what has to be true.

### Premises

A causal state is a graph of premises, called `items` in the CLI. Each premise has:

- **key:** a unique name, in plain words.
- **value** and **description:** what it holds, and what it is, in a line.
- **role:** `goal` (to be proved), `test` (true or false of the finished work), or none (a fact).
- **parent:** the premise it refines, either as an AND sub-goal (`--and`: all children must hold) or as an OR candidate (`--or`: one is enough).
- **on:** premises it reads as inputs. They support it without refining it.
- **status:** `stated`, `verified`, `assumed`, `unresolved` or `invalidated`.
- **await:** what it waits on: `human`, `environment`, a test's key, or `none`.
- **origin:** `human`, `agent`, `tool` or `web`.
- **said:** the human's own words it comes from.
- **refinement:** `complete` or `incomplete`.
- **p:** for an OR candidate, how likely it is to work, as a decision ranked it.

A causal link you have not verified is a hypothesis. Say so when a conclusion depends on one.

Keep the state honest and current as information arrives, tasks are assigned, tests run, and the environment changes, including when a human gives new instructions. Every state command returns a summary and next-step hints generated from the tree's structure.

### Refinement and completeness

Refining a goal premise decomposes it into a probabilistic AND/OR tree. The leaves are atomic: a test, or something that needs input the state doesn't contain, such as a human answer, an environment fact, or a pending test result.

`refinement` is set per premise: `complete` means its children are enough. `state:refine` records it, or you set it with `state:edit --refinement complete`. A goal is **completely refined** when every premise in its tree that has children is `refinement=complete`, so that the tree ends in leaves.

The tree works as a proof structure. Truth flows upward through the logic: an AND node holds when all its children hold, and an OR node holds when any one does. **A goal is reached when the leaves required by its completely refined tree are all verified.**

Probabilities rank OR candidates so you know what to try first. They never establish truth. Only verification does, through a passing test or the human's confirmation. A failing test invalidates a candidate, and the next one becomes the one to try.

A premise with children stays open until its refinement is complete, even when every child is proved. Changing a goal's value sets its refinement back to incomplete.

### Discerning

Discerning is the process of completely refining a goal and then verifying a necessary and sufficient set of its leaves. Use it for tasks with no one right answer (such as tradeoffs), for cornerstones of larger tasks, and wherever proof matters. Skip it for rote or trivial work.

```bash
hw state:create --use                                  # a new state, used by every hw call in this directory
hw state:add "the dinner is planned" "A dinner for six on Friday" --role goal --said "<their words>"
hw state:refine "the dinner is planned" --face @owner~face -r
hw state:get                                           # the tree, and what to do next
hw state:edit "<test>" --status verified --tested <candidate> --evidence "<what the run showed>"
```

Example output:

```
[ ] 1 the dinner is planned  AND
[x]   1.1 the guests and their needs (axiom)
[ ]   1.2 the menu  OR
[ ]     1.2.1 curry, quinoa salad, sorbet (p 0.71, next to try)
[ ]     1.2.2 pie, garlic bread, brownies (p 0.21)
[ ]   1.3 test: each guest can eat each dish (not run)

Open. Next to try: 1.2.1 (p 0.71). Proved when 1.3 passes on 1.2.1.
```

### Halting

After each query, every open box falls into one of three groups:

- **Something you can settle now:** refine it, run its test, or weigh its candidates.
- **Something to wait for:** it awaits the environment or a running test.
- **Something only the human knows:** it awaits their answer.

Waiting on one branch never blocks work on the others. The work is done when the root is proved. Short of that, stop when every open box is waiting on something. Ask the human only for what only they can tell you.

### Choices, decisions and the record

- `hw state:choices` asks a face to propose candidates for an open premise (abduction).
- `hw state:decide` ranks them by how likely each is to work (induction). It ranks and never prunes.
- `hw state:edit` records test results.
- `hw state:items` lists the history of every decision and write.

Nothing yet restores the tree to an earlier point. Read the history with `state:items` and work from the current tree.

### Dispatch and parallel work

Once a goal is refined, each leaf is a small, well-defined piece of work that can go to the model that suits it.

1. **Shape the tree with your strongest model.** Refinement is where judgement matters most.
2. **Route the leaves.** Give simple pieces to small, cheap models, hard pieces to stronger models, or keep them yourself. `state:choices` and `state:decide` write candidates and rankings into the state, so each decision stays on the record.
3. **Claim branches for subagents.** `hw state:claim "<key>" <name>` gives a branch to one agent, so several agents can work in parallel without overwriting each other.
4. **Record outcomes as lessons,** in the first person: the situation, and what you learned from it. For example: "When a task merges records across dated changes, I give it to the stronger model: the small one follows the first change and stops."
5. **Distill the lessons into a dispatcher face** (`@you~dispatcher`) and compile it again as lessons accumulate. Then ask a decision steered by that face which model to use, with your shortlist as the options.

**Seeding a dispatcher.** Before you have results of your own, inherit a public one: `hw face:list --public --search "dispatch" --sort usage`. Write what has been reported about each model as lessons too, marked as reported rather than observed ("Reported, not yet seen in my runs: …"), so your own results can overrule them. Dispatch with both your face and the inherited one: `(@you~dispatcher | @someone~dispatcher):maestro-1/jev-latest`. Check the live docs for the current composition syntax before relying on it.

Keep lessons honest. A lesson should come from a run you have actually read, not from a guess. Check the dispatcher from time to time against how its picks turned out.

### Keep it in view

`hw state:hud` prints a three-line summary of the state: the goal, how much of it is proved, the next step, and what waits on whom. The hooks show it to you on each user message and, during long runs, after a state write or every 15 tool calls. `hw state:hud off` turns it off, and `--goal "<key>"` pins which goal it follows. Drill in with `hw state:get "<key>"`.

> TODO (#2091): `state:hud` and its hooks ship with the next CLI release. Until then, the hooks show the state at session start and on each stop.

### Handing a state to Maestro

Every Maestro model takes a state as its input. You can hand it one in two ways:

- **as text:** query the state for what the call needs, and send that, in any format including JSON;
- **by id:** create the state with `hw state:create`, note its id (`fs_…`), and pass the id. The endpoint then reads the state for you, taking what the call needs.

> TODO: today only `POST /v1/choices` takes a state id (`state_id`), and the `maestro:*` commands take text only. Inside a causal state, `state:choices` and `state:decide` read the state for you.

## Maestro

**Maestro is an upstream encoder for causal codes.** It takes a state and a face. Reading the state through the face's mask, it encodes the cause at work in the situation as a **why code**, geometry in causal space. The why code then steers a downstream **decoder**, which gives the output its shape. The why code itself is never returned.

Maestro is never used alone. It is always paired with one face and one decoder, and the three together make an **inference model**, assembled on demand and named in one string.

That is what Maestro makes possible: bespoke inference models, decomposed into parts you can swap, built in a call rather than trained. A face made today works with every decoder, and a decoder released tomorrow works with every face you have.

In the CLI, `maestro:choices` and `maestro:decide` take the state as `--state` or `--state-file`, and `maestro:chat` as `--message`, `--file` and `--system`.

### Model strings

```
@owner~face:encoder/decoder
```

For example:

```
@zerocool~redteam:maestro-1/gpt-6-astra
(@zerocool~redteam | @acidburn~worldspacedev):maestro-1/gpt-6-astra
```

The second form composes faces with `|`. Check the live docs for the current composition syntax before relying on it.

Use `maestro-1-fast` (`--fast`) when latency matters more than cost. It is the same encoder, answering sooner at ten times the price.

### Decoders


| decoder  | models                                                                          | CLI example                               | you send                                                                                                                                 | you get back                                                                                                                                     |
| -------- | ------------------------------------------------------------------------------- | ----------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| choices  | `choices`                                                                       | `hw maestro:choices`                      | a state as text (`--state`, up to 3,000 tokens), optionally a question. Over HTTP, a causal state id instead                             | up to `max_choices` options, strongest first, each a short name and a sentence. Without a question, the face proposes the question it would ask. |
| decision | `jev-latest`, `clef`, `clef-flash`, `gpt-6-luna`                                | `hw maestro:decide --decoder jev-latest`  | a state as text (`--state`) and typed questions: `--type noul` (yes or no; `predicate` on `/v1/decisions`), `choice` or `score` (graded) | a probability for each option, level or yes, plus the top answer                                                                                 |
| chat     | `gpt-*`, `claude-*`, `grok-*`, `gemini-*`, `qwen-*`, `glm-*`, `deepseek-*`, ... | `hw maestro:chat --decoder glm-5-3-flash` | a state as a conversation (`--message`, `--system`)                                                                                      | the chat model's reply, in that API's standard shape                                                                                             |


Each kind of decoder gives a different mode of inference: choices is abduction (the options worth weighing), a decision is induction (a calibrated probability for each option), and chat is broadcast (a reply in that model's own words).

The choices decoder is native to Headwaters. Decision and chat decoders include models from frontier labs and popular open-weight models. Run `hw models:list --kind decision` or `--kind chat` for the current list.

`noul` is not a typo: it is the System One name for a yes-or-no question, and what `--type` takes. On `/v1/decisions` the same type is called `predicate`.

### Use

```bash
hw maestro:choices --face @owner~face --state "<the situation>" [--question "<the choice you face>"]
hw maestro:decide  --face @owner~face --state "<the situation>" --question "<which option?>"
hw maestro:chat    --face @owner~face --decoder <chat model> --message "<…>" [--thread <name>]
```

Run `hw <topic>:<command> --help` before using a flag you have not seen.

**Write the state for a person.** Could a smart person, shown only this state and this question, answer quickly? If not, fix the state before the wording. Give what a person would look at (who said what, names rather than raw IDs), keep every part relevant, ask one judgement per question, and name options by what they are.

**Read the answers.**

- A choice's options come strongest first. The first is the face's lead, not a verdict: weigh them with a decision when you must pick.
- A decision's probability is how likely the answer is correct, as this face judges it. For a yes or no, 0.7 and 0.3 are good starting thresholds; the band between means the state does not settle it, so give that band its own outcome.
- No clear winner among options (top probability under 0.6, or a lead under 0.2) usually means the choice is not the model's to make. Ask the person it belongs to.

### Cascade

Chain them. First, choices proposes the options from a state and a question, or a question and its options from a state alone (abduction). Then a decision ranks those options (induction). The choices' names go straight into the decision as a `choice` question's options.

For example, under `@you~home-cook`, with the state "A dinner for six on Friday; one guest is vegan, one has a nut allergy" and the question "Which menu?", choices proposes "curry, quinoa salad, sorbet", "pie, garlic bread, brownies" and others. A `choice` decision on `jev-latest`, under the same face, then ranks them: curry 0.71, pie 0.21. Under a different face the same options can rank differently, so the face you pick decides the route. Inside a causal state, `state:choices --rank` does both steps and writes the ranking into the state.

## Faces (`hw face:*`)

A face is a mask on causal space that encodes a taste and judgement, compiled from a body of source texts. It adapts to the input and decides which causes Maestro sees in a state. Faces are compiled, not trained. You can make them as new tasks arrive and new lessons are learned, and they compose, so you can use them like building blocks in a steering program.

What you can distill:

- **A person:** their writing, talks and interviews, so you can ask what they would do.
- **A role or craft:** the judgement of a good editor, auditor or home cook.
- **The user:** their own `me` face, built from their writing.
- **Your own lessons:** what worked and what failed in your runs.
- **A model dispatcher:** a face that maps the jagged edges of various models, to decide which one to route to.

### Find one

```bash
hw face:list --for "<the judgement you need>"            # your faces, best fit first
hw face:list --for "<…>" --public                        # including published faces
hw face:list --public --search "<words>" --sort usage    # most-used published faces that match
```

If the best fit is weak, make one. Each branch of a causal state has its own task, so its best face can differ from the root's.

### Make one

```bash
hw face:create --name "Home Cook" --alias home-cook \
  --description "An experienced home cook who plans meals for groups" \
  --specialty "Planning and cooking meals for groups of guests"
hw face:compile home-cook --file notes.md --medium essay
hw face:compile home-cook --file interview.txt --kind thread --face-speaker "Sam"
hw face:import  home-cook --url "https://www.youtube.com/watch?v=VIDEO_ID"
```

- **Description and specialty** are what `face:list --for` matches a task against. Write them as what the face is good for.
- **A face is only as good as its sources.** Give it writing where the judgement shows and/or the taste is evident: how the author decides, what they weigh, what they refuse, what they favor. For lessons, write each as a situation and what you learned from it.
- **A document** is one author's own writing. Every word is read as theirs.
- **A thread** is a conversation, interview or transcript. Name the one speaker who is the face; the others are read as context. Never pass a multi-speaker transcript as a document.
- **More sources sharpen a face,** and you can compile again at any time.
- **Compiling** is billed per source token and takes a while. `--rush` starts it as soon as possible, at a higher rate charged only if it starts ahead of its scheduled start. A face runs at most three compiles at once; others wait their turn.
- **Use a face** once something in it is compiled: `@you~home-cook:maestro-1/<decoder>`. A face with nothing compiled returns `409`.

### Share one

`hw face:publish` lists a face in the public catalog. `hw face:share` gives it to chosen accounts. `face:unpublish` and `face:unshare` undo them.

## Account, keys and cost

```bash
npm install -g @headwaters-ai/cli@latest         # install or update hw
hw account:register --email … --password '…' --username … [--plan connect|pro]   # see references/QUICKSTART.md first
hw account:login --email … --password '…'
hw account:whoami
hw account:balance                               # credit; account:topup adds more
hw account:usage                                 # what has been spent, and on what
hw account:activate --plan connect               # subscribe from Free; account:plan switches a subscription
hw key:create --name "my-key"                    # a key for programs and agents, used as HW_API_KEY
hw key:list
hw key:edit <id> --budget 5                      # a spending cap
hw key:revoke <id>
hw config:set api_key <key>                      # save a key for hw on this machine
```

**Spending is the user's call.** Make no paid call (choices, decisions, chat, refine, compile) until the user has approved a budget, the data to be sent (point out anything personal or private), and which key will be used.

`hw <topic> --help` lists every command. Every command takes `--json` for machine-readable output.

Every account has a face of its own, aliased **`me`**. Compile the user's own writing into it rather than creating another.

**Plans.** Free pays as you go, with no monthly fee. Connect and Pro add monthly allowances for compiling and for Maestro. Eligible chat models run on a linked ChatGPT plan (`hw account:connect openai`).

**Cost.** Choices, decisions and chat are billed per token the encoder processes, plus the decoder's own price for decisions and chat. Compiling is billed per source token. Building and reading a causal state is free; refining it runs billed choices and decisions. For current prices, plans and limits, use `GET /v1/rates` and `GET /v1/models`.

## Building with the API

Use the HTTP API for any language, or `hw` for scripts and probing. The chat endpoints are drop-in replacements for OpenAI's and Anthropic's, so an existing client changes only its `model`: `@owner~face:maestro-1/<chat model>`.

**The live docs are the source of truth** for request syntax, limits, prices and current behaviour. Read the relevant pages as part of the task:

- Documentation index: `https://docs.headwaters.ai/llms.txt`. Append `.md` to a page path for Markdown.
- OpenAPI spec: `https://api.headwaters.ai/openapi.json`.
- Prices and limits: `GET /v1/rates`. Models: `GET /v1/models`.

If those hosts don't resolve, use `https://docs.faces.sh` and `https://api.faces.sh`. If you can't reach the docs at all, say so and leave out version-dependent details rather than guessing them.

### Errors

Errors return JSON with a `detail` you can show as it stands.

- `422`: the request has the wrong shape. The message shows the right form.
- `409`: the face has nothing compiled yet, or is busy.
- `429`: a limit was hit. The message says when it resets.
- `503`: retry after `Retry-After`.
- A long call may return `200` with an `error` body if it fails after it started. Treat that as a failure.

## Glossary


| term                    | meaning                                                                                                |
| ----------------------- | ------------------------------------------------------------------------------------------------------ |
| **Maestro**             | the upstream encoder: it reads a state through a face and produces a why code                          |
| **face**                | a mask on causal space, compiled from source texts, that encodes a taste and judgement                 |
| **why code**            | the latent cause Maestro distills from the state and face; it steers the decoder and is never returned |
| **decoder**             | the downstream model that turns the why code into output: choices, a decision model, or a chat model   |
| **causal space**        | the space of directional dependencies: what a state depends on and what it leads to                    |
| **model string**        | face, encoder and decoder named together: `@owner~face:maestro-1/<decoder>`                            |
| **inference model**     | a face, Maestro and a decoder, paired on demand                                                        |
| **state**               | the situation sent with a call: prose, or a causal state                                               |
| **causal state**        | an AND/OR tree of premises, kept on the server and kept true as things change                          |
| **premise**             | a node of a causal state: a goal, a test or a fact                                                     |
| **complete refinement** | a goal decomposed into leaves all the way down; `refinement=complete`                                  |
| **discerning**          | completely refining a goal, then verifying the leaves that prove it                                    |
| **halting**             | knowing, from the state, when to work, when to wait and when to ask                                    |
| **dispatch**            | sending each piece of work to the model that suits it                                                  |
| **distill**             | compiling intelligence and lessons into a face                                                         |


## References


| file                       | covers                                                                                         |
| -------------------------- | ---------------------------------------------------------------------------------------------- |
| `references/QUICKSTART.md` | from nothing to a first answer: install, sign up or in, a key, your own face, a first question |
| `references/CLI.md`        | every `hw` command and flag (not yet written: use `hw <topic> --help`)                         |
| `references/SETUP.md`      | installing `hw`, keys, and the plugin hooks for Claude Code and Codex                          |
| `references/STATES.md`     | the causal state in full: reading the tree, refinement, every `state:` command                 |
| `references/FACES.md`      | distilling, compiling, finding, combining and sharing faces                                    |
| `references/MODELS.md`     | the decoders you can name, the encoder's two speeds, and how to choose among them              |
