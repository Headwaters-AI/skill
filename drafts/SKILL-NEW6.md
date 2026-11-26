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

Headwaters is a causal layer for consistent judgement over long sessions. It helps you work through tradeoffs that have no single right answer, decide when to keep going and when to stop and ask, and send each piece of work to the model that suits it.

## Core concepts

**State** is a pragmatic map of your situation, expressed in text: what is true, what the goal is, and what is still open. State is the stable, evolving source from which the context for each model call is assembled. Context is what one stateless request receives; state persists across calls. Context is to RAM what state is to disk.

**Causal relations** are directional dependencies: the answers to *why* one state gives rise to another. They cover sequence and consequence.

**Causal space** is the space these relations live in. For instance, representational convergence (the "platonic representation hypothesis") describes models agreeing on which inputs are similar. Causal space is the layer that answers what produces what. It is a modelling layer: the causal links in a state are the tool's model, not established facts. When a conclusion depends on a link, say so.

The three parts:

- **Causal state** holds your current and goal states as an AND/OR tree of premises.
- **Maestro** composes inference over a state, using a face and a decoder.
- **Faces** are masks compiled from source texts that carry a particular judgement or taste.

## Causal state (`hw state:*`)

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

Keep the state honest and current as information arrives, tasks are assigned, tests run, and the environment changes, including when a human gives new instructions. Every state command returns a summary and next-step hints generated from the tree's structure.

### Refinement and completeness

Refining a goal premise decomposes it into a probabilistic AND/OR tree. The leaves are atomic: a test, or something that needs input the state doesn't contain, such as a human answer, an environment fact, or a pending test result.

A goal is **completely refined** (`refinement=complete`) when every branch under it has been decomposed down to leaves.

The tree works as a proof structure. Truth flows upward through the logic: an AND node holds when all its children hold, and an OR node holds when any one does. **A goal is reached when the leaves required by its completely refined tree are all verified.**

Probabilities rank OR candidates so you know what to try first. They never establish truth. Only verification does, through a passing test or the human's confirmation. A failing test invalidates a candidate, and the next one becomes the one to try.

Do not mark a goal achieved while its refinement is incomplete or a required leaf is unverified.

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

Waiting on one branch never blocks work on the others. Stop when every open box is waiting on something. Ask the human only for what only they can tell you.

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
5. **Distil the lessons into a dispatcher face** (`@you~dispatcher`) and compile it again as lessons accumulate. Then ask a decision steered by that face which model to use, with your shortlist as the options.

**Seeding a dispatcher.** Before you have results of your own, inherit a public one: `hw face:list --public --search "dispatch" --sort usage`. Write what has been reported about each model as lessons too, marked as reported rather than observed ("Reported, not yet seen in my runs: …"), so your own results can overrule them. Dispatch with both your face and the inherited one: `(@you~dispatcher | @someone~dispatcher):maestro-1/jev-latest`.

Keep lessons honest. A lesson should come from a run you have actually read, not from a guess. Check the dispatcher from time to time against how its picks turned out.

## Maestro

Maestro is an upstream encoder for composing inference on demand. You pair it with a decoder, which sets the output shape, and a face, which sets the judgement. Maestro reads the state through the face and distills a **why code**: a latent causal representation of the state that steers the decoder. The why code is never returned.

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


| decoder  | models                                                                          | CLI example                             | you send                                                                                 | you get back                                                                                                                                     |
| -------- | ------------------------------------------------------------------------------- | --------------------------------------- | ---------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| choices  | `choices`                                                                       | `hw maestro:choices`                    | a state (prose up to 3,000 tokens, or a causal state id), optionally a question          | up to `max_choices` options, strongest first, each a short name and a sentence. Without a question, the face proposes the question it would ask. |
| decision | `jev-latest`, `clef`, `clef-flash`, `gpt-6-luna`                                | `hw maestro:decide --model jev-latest`  | the situation and typed questions: `choice`, `predicate` (yes or no) or `score` (graded) | a probability for each option, level or yes, plus the top answer                                                                                 |
| chat     | `gpt-*`, `claude-*`, `grok-*`, `gemini-*`, `qwen-*`, `glm-*`, `deepseek-*`, ... | `hw maestro:chat --model glm-5.3-flash` | a conversation                                                                           | the chat model's reply, in that API's standard shape                                                                                             |


The choices decoder is native to Headwaters. Decision and chat decoders include models from frontier labs and popular open-weight models. Run `hw maestro:list` for the current list.

Today only `POST /v1/choices` accepts a causal state id. `maestro:decide` and `maestro:chat` take the state as text through `--state`.

### Use

```bash
hw maestro:choices --face @owner~face --state "<the situation>" [--question "<the choice you face>"]
hw maestro:decide  --face @owner~face --state "<the situation>" --question "<which option?>"
hw maestro:chat    --face @owner~face [--thread <name>]
```

### Cascade

Chain them. The choices decoder sits upstream: it extracts the choices from a (state, question) pair, or extracts a question and choices from a state alone. It provides abduction. A decision model downstream provides induction. Different faces produce different routes.

## Faces (`hw face:*`)

A face is a mask compiled from a body of source texts. It adapts to the input, then masks the Maestro encoder that processes it, providing a lens that shapes which causal driver Maestro isolates. Faces are compiled, not trained. You can make them as new tasks arrive and new lessons are learned, and they compose, so you can use them like building blocks in a steering program.

What you can distill:

- **A person:** their writing, talks and interviews, so you can ask what they would do.
- **A role or craft:** the judgement of a good editor, auditor or home cook.
- **The user:** their own `me` face, built from their writing.
- **Your own lessons:** what worked and what failed in your runs.
- **Model Dispatcher**: a face that maps the jagged edges of various models and determines which to route to

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
- **Compiling** is billed per source token and takes a while. `--rush` starts it as soon as possible. A face runs at most three compiles at once; others wait their turn.
- **Use a face** once something in it is compiled: `@you~home-cook:maestro-1/<decoder>`. A face with nothing compiled returns `409`.

### Share one

`hw face:publish` lists a face in the public catalog. `hw face:share` gives it to chosen accounts. `face:unpublish` and `face:unshare` undo them.

## Account, keys and cost

```bash
npm install -g @headwaters-ai/cli@latest         # install or update hw
hw account:register --email … --username … [--plan connect|pro]
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


| term                    | meaning                                                                                               |
| ----------------------- | ----------------------------------------------------------------------------------------------------- |
| **Maestro**             | the upstream encoder: it reads a state through a face and produces a why code                         |
| **face**                | a mask compiled from source texts, whose judgement steers the output                                  |
| **why code**            | the latent cause Maestro distils from the state and face; it steers the decoder and is never returned |
| **decoder**             | the downstream model that turns the why code into output: choices, a decision model, or a chat model  |
| **model string**        | face, encoder and decoder named together: `@owner~face:maestro-1/<decoder>`                           |
| **state**               | the situation sent with a call: prose, or a causal state                                              |
| **causal state**        | an AND/OR tree of premises, kept on the server and kept true as things change                         |
| **premise**             | a node of a causal state: a goal, a test or a fact                                                    |
| **complete refinement** | a goal decomposed into leaves all the way down; `refinement=complete`                                 |
| **discerning**          | completely refining a goal, then verifying the leaves that prove it                                   |
| **halting**             | knowing, from the state, when to work, when to wait and when to ask                                   |
| **dispatch**            | sending each piece of work to the model that suits it                                                 |
| **distil**              | compiling intelligence and lessons into a face                                                        |


## References


| file                       | covers                                                                                         |
| -------------------------- | ---------------------------------------------------------------------------------------------- |
| `references/QUICKSTART.md` | from nothing to a first answer: install, sign up or in, a key, your own face, a first question |
| `references/CLI.md`        | every `hw` command and flag                                                                    |
| `references/SETUP.md`      | installing `hw`, keys, and the plugin hooks for Claude Code and Codex                          |
| `references/STATES.md`     | the causal state in full: reading the tree, refinement, every `state:` command                 |
| `references/FACES.md`      | distilling, compiling, finding, combining and sharing faces                                    |
| `references/MODELS.md`     | the decoders you can name, the encoder's two speeds, and how to choose among them              |
