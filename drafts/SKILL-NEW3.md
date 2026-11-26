---
name: headwaters-ai
license: MIT
description: >
  Headwaters integration craft for Maestro, an upstream encoder model that reads state through a
  face (a mask compiled from a body of source texts) and steers a downstream model: choices, a
  decision (aka System One) model such as Jev, or a chat model. Use when decomposing long-running tasks to know
  when and how to work, wait or ask, and to dispatch each piece to the optimal model or agent; when distilling intelligence,
  taste, judgement, or wisdom (lessons learned by failing) into a face; when building, reviewing, or
  debugging code that calls the Headwaters API or the `hw` CLI; or when one or more specific perspectives are useful in
  brainstorming, troubleshooting, targetted messaging, comparing and contrasting, and the like.
---
Headwaters tools are designed to give you judgement, taste, and discernment. They help to tame and exploit the jaggedness of AI models and bring rigor to tasks and problems with no one right answer.

`hw` is the Headwaters CLI. Every command is `tool:verb`.


| tool                  | commands                                                                                                                                                                          |
| --------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`maestro`](#maestro) | `maestro:choices`, `maestro:decide`, `maestro:chat`                                                                                                                               |
| [`face`](#face)       | `face:create`, `face:list`, `face:compile`, `face:import`, `face:publish`, `face:share`, `face:edit`, `face:delete`                                                               |
| [`state`](#state)     | `state:create`, `state:use`, `state:get`, `state:add`, `state:edit`, `state:delete`, `state:claim`, `state:refine`, `state:choices`, `state:decide`, `state:items`, `state:close` |
| [account](#account)   | `auth:register`, `auth:login`, `auth:whoami`, `keys:create`, `billing:balance`, `config:set`                                                                                      |


Every command takes `--help`, and `--json` for machine-readable output. The full manual is in `references/CLI.md`.

> TODO (#2082): generate `references/CLI.md` from `hw --help` for every command, with a script run at each CLI release, so the manual can never drift from the CLI.

**New to Headwaters?** Follow `references/QUICKSTART.md`: it signs the user up or in, compiles their own face and asks it a first example question.

The sections below are organized by product.

## `maestro`

**Maestro** is an upstream view encoder for composing inference models on demand. You pair it with an off-the-shelf **decoder** to determine the shape of its output, and give it a **face** to determine its judgement and taste.

A face is a mask compiled from a body of source texts through which Maestro interprets its input. This reading is distilled into a latent **why code**: an upstream causal representation of the state that steers the decoder in generating its output.

Every inference model is defined by its face, encoder and decoder, specified in a single model string:

`@owner~face:encoder/decoder`

For example, using a Headwaters account username as the owner:

`@zerocool~redteam:maestro-1/gpt-6-astra`

Multiple faces can be composed directly within the model string using boolean operators:

`(@zerocool~redteam | @acidburn~worldspacedev):maestro-1/gpt-6-astra`

> TODO (#2081): every face is to be named with its owner, even your own, and the composite operators are under review. Update the examples here once #2081 settles the syntax.

### Decoders

Maestro can be paired with three different decoders, each providing a different function and output shape.


| decoder  | model options                                                                   | CLI (example)                           | you send                                                                                                    | you get back                                                                                                                                     |
| -------- | ------------------------------------------------------------------------------- | --------------------------------------- | ----------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| choices  | `choices`                                                                       | `hw maestro:choices`                    | a state (prose up to 3,000 tokens, or a causal state id), and optionally a question                         | up to `max_choices` options, strongest first, each a short name and a sentence. Without a question, the face proposes the question it would ask. |
| decision | `jev-latest`, `clef`, `clef-flash`, `gpt-6-luna`                                | `hw maestro:decide --model jev-latest`  | the situation and typed questions: `choice` (pick one), `predicate` (yes or no) or `score` (a graded scale) | a probability for each option, level or yes, plus the top answer                                                                                 |
| chat     | `gpt-*`, `claude-*`, `grok-*`, `gemini-*`, `qwen-*`, `glm-*`, `deepseek-*`, ... | `hw maestro:chat --model glm-5.3-flash` | a conversation                                                                                              | the chat model's reply, in that API's own standard shape                                                                                         |


The sole choices decoder is native to Headwaters. Decision and chat decoders  include models from frontier labs and popular open weight models. The full model list can be found with `hw maestro:list`

`maestro-1-fast` (`--fast`) is the same encoder, answering sooner, at ten times the price. Use it when latency matters more than cost.

### Use

```bash
hw maestro:choices --face @owner~face --state "<the situation>" [--question "<the choice you face>"]
hw maestro:decide  --face @owner~face --state "<the situation>" --question "<which option?>"   # the choices' names as options
hw maestro:chat    --face @owner~face [--thread <name>]
```

### Cascade

The choices decoder is designed to sit upstream of decision models by extracting the optimal set of choices from a (state, question) input pair, or extracting the optional question and choices from a state alone. The upstream choices decoder provides abduction, the decision model downstream of it provides induction. Different faces applied to each will result in different routes.



## `face`

A face is compiled from a body of source texts into a recursive mask: it first adapts to the input and then is used to mask the Maestro encoder that processes it. It can be understood as providing a responsive lens distilled from the source texts that shapes the way Maestro isolates the driving cause that is then used to steer the decoder's output.

Faces are much cheaper and faster than trained modules like LoRA, and are designed to be created on the fly as new tasks are needed and new lessons are learned. And because they are composable, they are like an object-oriented metaprogramming language for agents to steer AI models. When used to identify the jagged cartography of AI models, they can transfer the idiosyncrasies of one to another, or route to the optimal model for the current task.

What you can distill:

- **a person:** their writing, talks and interviews, so you can ask what they would do;
- **a role or a craft:** the judgement of a good editor, auditor or home cook;
- **the user:** their own `me` face, built from their writing;
- **your own lessons:** what worked and what failed in your runs. The dispatcher under [`state`](#state) is one example; a face of a project's hard-won lessons is another.

### Find one

```bash
hw face:list --for "<the judgement you need>"            # your faces, best fit first
hw face:list --for "<…>" --public                        # with everyone's published faces
hw face:list --public --search "<words>" --sort usage    # the most used published faces that match
```

A weak best fit means it is time to make one. Each branch of a causal state has its own task, so its best face can differ from the root's.

### Make one

```bash
hw face:create --name "Home Cook" --alias home-cook \
  --description "An experienced home cook who plans meals for groups" \
  --specialty "Planning and cooking meals for groups of guests"
hw face:compile home-cook --file notes.md --medium essay
hw face:compile home-cook --file interview.txt --kind thread --face-speaker "Sam"
hw face:import  home-cook --url "https://www.youtube.com/watch?v=VIDEO_ID"
```

- The **description** and **specialty** are what `face:list --for` matches a task against, so write them as what the face is good for.
- **A face is only as good as its sources.** It learns from the author's own words, so give it writing where the judgement shows: how they decide, what they weigh, what they refuse. For lessons, write each one as a situation and what you learned from it.
- **A document** is one author's own writing: essays, notes, posts, a set of lessons. Every word is read as theirs.
- **A thread** is a conversation, interview or transcript, where only one speaker is the face. Name that speaker, and the others are read as context. Never pass a multi-speaker transcript as a document.
- **More sources sharpen a face,** and it can be compiled again at any time with new ones.
- **Compiling** is billed per source token and takes a while. `--rush` starts it as soon as possible, at a higher rate only if it starts before its scheduled start. A face runs at most 3 compiles at once; more wait their turn.
- **Use it** as soon as something in it is compiled: `@you~home-cook:maestro-1/<decoder>`. A face with nothing compiled answers `409`.

### Share one

`hw face:publish` lists it in the public catalog, and `hw face:share` gives it to chosen accounts. `face:unpublish` and `face:unshare` undo them.

The full guide is in `references/FACES.md`.

### Canonical Faces

`me` 

## `state`

A causal state is how you, the agent, do long work well. It gives you three things.

**1. Optimized halting.** At every moment the state tells you whether there is work you can do now, something you must wait for, or a question only the human can answer. So you neither stop too early, leaving the job half done, nor keep going on guesses, wasting tokens and the human's time.

**2. Optimal dispatch.** A task broken into premises is a set of small, well-defined pieces of work. Each can go to the cheapest model that does it well, so you never send a simple request to an expensive model, or a hard one to a model that will fail it.

**3. Rails for long-running tasks.** Ask for several points of view (abduction, with choices) and decide between them (induction, with decisions), so each step stays on the path toward the goal. Every decision is kept with what it rested on. When you find yourself off track, the trace shows where you went wrong.

### The proof

A causal state lets you work under the direction of a human the way a mathematician works on a proof over time. The human gives you the problem, often in pieces. Maestro helps you assemble them into a probabilistic AND/OR tree that shows at once what you are trying to prove and how much of it is proved so far.

The tree follows goal-oriented requirements engineering (KAOS). A goal is refined into sub-goals that must all hold (AND), or into alternatives of which one is enough (OR). Every box is proved, refuted or open, and truth flows upward: an AND is proved when all its children are, an OR when any one is.

The work follows Peirce's cycle, with refinement before it: **refine** a premise into its children; **propose** candidates for an open choice (abduction); **weigh** them, to know which to try first (induction); **verify** with tests that are true or false of the finished work (deduction). `hw state:refine` does the first three for you, using choices and decisions under a face of your choosing.

```bash
hw state:create --use
hw state:add "the dinner is planned" "A dinner for six on Friday" --role goal --said "<their words>"
hw state:refine "the dinner is planned" --face @owner~face
hw state:get
```

```
[ ] 1 the dinner is planned  AND
[x]   1.1 the guests and their needs (axiom)
[ ]   1.2 the menu  OR
[ ]     1.2.1 curry, quinoa salad, sorbet (p 0.71, next to try)
[ ]     1.2.2 pie, garlic bread, brownies (p 0.21)
[ ]   1.3 test: each guest can eat each dish (not run)

Open. Next to try: 1.2.1 (p 0.71). Proved when 1.3 passes on 1.2.1.
```

When a test runs, record it: `hw state:edit "<test>" --status verified --evidence "<what the run showed>"`.

### Halting

The last line names what still stands between you and a proved goal. Each open box on it is one of three things:

- **something you can settle now:** refine it, run its test, or weigh its candidates;
- **something to wait for:** a box that awaits the environment or a running test;
- **something only the human knows:** a box that awaits their answer.

Waiting on one branch never stops work on the others. The work is done when the root is proved, and you stop when every open box is waiting on something. The plugin hooks show you this line when a session starts and whenever you stop.

### Choices and decisions in the state

`hw state:choices` and `hw state:decide` work like `maestro:choices` and `maestro:decide`, and write the candidates and their ranking into the state, so the decision becomes part of the trace. A decision ranks candidates by how likely each is to work; it never rules one out. Only a failing test, or the human, refutes a candidate, and the next one becomes the one to try.

> TODO: a command to return the state to an earlier point (the "rails"). Today the state keeps every decision and every write in its history, and `hw state:items` lists them, but nothing restores the tree to how it stood before a given decision.

### Dispatching intelligence

Once a task is refined into premises, each leaf is a small, well-defined piece of work that can go to the model that suits it. Curating the right face and the right model for each piece is intelligence dispatch.

1. **Shape the proof with your strongest model.** Refinement is where judgement matters most, so it gets the best model.
2. **Dispatch the leaves.** From a whitelist of models, give simple pieces to smaller, cheaper models and hard ones to stronger models, or keep them yourself. `hw state:claim "<key>" <name>` gives a branch to a subagent, so several can work in parallel without overwriting each other.
3. **Record what happened.** When a dispatched piece succeeds or fails, write the lesson in the first person, as the situation and what you learned. For example: "When a task merges records across dated changes, I give it to the stronger model: the small one follows the first change and stops."
4. **Distil the lessons into a dispatcher face** (see [`face`](#face)). Add each new lesson document to your own face, e.g. `@you~dispatcher`, and compile it again. The face now carries your routing judgement.
5. **Dispatch with the face.** For each new piece of work, ask a decision steered by your dispatcher which model to use: `@you~dispatcher:maestro-1/jev-latest`, with the question "Which model should this task be dispatched to?" and your shortlist as the options.

**Seeding the dispatcher.** Before you have your own results, start from what others have learned:

- **Inherit a public dispatcher:** `hw face:list --public --search "dispatch" --sort usage`. Take the one that fits your whitelist as a baseline.
- **Research your whitelist.** Write what has been reported about each model as lessons too, marked as reported rather than observed ("Reported, not yet seen in my runs: …"), so your own results can overrule them.

**Keep your lessons beside the inherited ones,** and dispatch with both: `(@you~dispatcher | @someone~dispatcher):maestro-1/jev-latest`.

> TODO (#2081): the meaning of `|` and the other composite operators is under review, and a set form such as `@you~{dispatcher,…}` may replace them. Update this example once #2081 settles the syntax.

Keep the lessons honest. A lesson comes from a run you have read, not from a guess, and a dispatcher is worth checking now and then against how its picks actually turned out.

The full guide, with every `state:` command, is in `references/STATES.md`.

## account

```bash
npm install -g @headwaters-ai/cli@latest         # install or update hw
hw auth:register --email … --username … [--plan connect|pro]   # a new account, from the terminal
hw auth:login --email … --password '…'           # or sign in
hw auth:whoami
hw keys:create --name "my-key"                   # a key for programs, used as HW_API_KEY
hw config:set api_key <key>                      # or set HW_API_KEY in the environment
hw billing:balance
```

Every account has a face of its own, aliased **`me`**: compile the user's own writing into it rather than creating another.

**Plans.** Free pays as it goes, with no monthly fee. Connect and Pro add monthly allowances for compiling and for Maestro, and eligible chat models run on a linked ChatGPT plan (`hw auth:connect openai`).

**Cost.** Choices, decisions and chat are billed per token the encoder processes, plus the decoder's own price for decisions and chat. Compiling a face is billed per source token. Building and reading a causal state is free; refining it runs billed choices and decisions. Current prices, plans, allowances and limits: `GET /v1/rates` and `GET /v1/models`.

The whole sign-up, step by step, is in `references/QUICKSTART.md`. The plugin hooks for Claude Code and Codex are in `references/SETUP.md`.

## SDK and API

Build software, agents and products that include Maestro.

- **The SDK,** for code. It handles model strings, retries and errors, and gives you the causal state and refine as library calls.
- **The HTTP API,** for any language. The chat endpoints are drop-in replacements for OpenAI's and Anthropic's, so an existing client only changes its `model`.
- **`hw`,** for scripts, prototypes and probing the API by hand.

> TODO (#2080 section 8): the TypeScript SDK, `@headwaters-ai/sdk` or similar, built as the core that `hw` itself runs on, so refine and everything else has one implementation. Then the Python SDK. Until they exist, use the HTTP API or `hw`. Add `references/SDK.md`, generated from the SDK's types, and lead this section with it.

### Maestro in a circuit

When you wire Maestro into software, treat each decoder as a smart version of a familiar hardware module:


| decoder            | component                     | what it does in a circuit                                                                            |
| ------------------ | ----------------------------- | ---------------------------------------------------------------------------------------------------- |
| `choices`          | a **smart demultiplexer**     | one state in, several weighted choices out                                                           |
| `<decision model>` | a **smart demux→mux cascade** | the situation fanned out, then collapsed back onto the options you give, as calibrated probabilities |
| `<chat model>`     | a **smart modulator**         | the why code's signal carried on the chat model's reply                                              |


Each module is a black box with an input, an output and a control: select lines for mux and demux, and for a modulator a signal that rides on the carrier wave. For Maestro, the face is an adaptive control line that is itself a function of the input, changing the mask it applies according to the perspectives the face holds. So a choices call fans one state out into branches, a decision collapses branches back to one, and chat carries the result to a person; chain them the way you would chain the modules.

**The live docs are the source of truth** for request syntax, limits, prices and current behaviour. Read the relevant pages as part of the task.

- Start at the [documentation index](https://docs.headwaters.ai/llms.txt). Append `.md` to a page path to get it as Markdown.
- Exact schemas: the [OpenAPI spec](https://api.headwaters.ai/openapi.json).
- Prices and limits: `GET /v1/rates`. Every model you can name: `GET /v1/models`.

If you can't reach the live docs, say so, and leave out details that depend on the version rather than guessing them.

> TODO (#2080): these hosts are live only after the move from faces.sh. Until then, use `https://docs.faces.sh` and `https://api.faces.sh`.

### Building with it

1. **Start from what the application decides.** Write down what your code will show, pick, change or hand off, and what judgements it needs to get there. Arithmetic, dates, lookups and policy belong in code. Judgements that need someone's taste belong to a face.
2. **Pick the decoder for the shape you need:** options to consider (choices), a number to act on (a decision), or words to show someone (chat).
3. **Find or distil the face** (see [`face`](#face)).
4. **Probe the live API** with representative, hard and negative cases.
5. **Integrate.** Keep the model strings, questions and options in one module. Log the exact request. Surface a failed call as an error, never as an answer.

For a feature with many parts, plan it as a causal state first (see [`state`](#state)).

**Errors** come back as JSON with a `detail` you can show as it stands. `422` means the request is the wrong shape, and its message shows the right form. `409` means the face has nothing compiled yet, or is busy. `429` names the limit and when it resets. `503` is the one to retry, after `Retry-After`. A long call may answer `200` with an `error` body if it fails after it started: treat that as the failure.

**Steer a reply.** Swap the `model` of an existing OpenAI or Anthropic client for `@owner~face:maestro-1/<chat model>`. Nothing else changes.

### Test with the live API

Ask the user before sending test requests. Agree a budget, say what data will be sent (point out anything personal or private), and say which key will be used.

- Start with a few representative cases, plus hard ones and ones whose answer is "no".
- Compare faces or wordings on the same state, side by side.
- **Read the individual outputs, not only the counts.** Two faces can return the same number of options where one is faithful to the situation and the other is fluent nonsense.
- Keep the exact request for each case so any result can be rerun.

**When an answer looks wrong,** check in this order: the request as actually sent, including the model string; the state, against the human test; the face (does `face:list --for` rank it well, and is it compiled?); the options (is the right answer among them?); the scope (can the question be split?); and last, the wording.

**Yellow flags.** Wording written to produce a particular answer tends to break on the next input. Watch for options that name test cases, thresholds fitted to a handful of cases, and code that quietly overrides answers. The fix is usually a better state, a separate question, a different face, or code.

## Glossary


| term             | meaning                                                                                                   |
| ---------------- | --------------------------------------------------------------------------------------------------------- |
| **Maestro**      | the upstream encoder model: it reads a state through a face and produces a why code                       |
| **face**         | a mask compiled from a body of source texts; whose judgement steers the output                            |
| **why code**     | the latent cause Maestro distils from the state and the face; it steers the decoder and is never returned |
| **cause**        | what a why code holds: why the face would act                                                             |
| **decoder**      | the downstream model that turns the why code into output: choices, a decision model or a chat model       |
| **model string** | face, encoder and decoder named together: `@owner~face:maestro-1/<decoder>`                               |
| **state**        | the situation sent with a call: prose, or a causal state                                                  |
| **causal state** | an AND/OR proof tree of premises, kept on the server and kept true as things change                       |
| **premise**      | a node of a causal state: a goal, a test or a fact                                                        |
| **halting**      | knowing, from the state, when to work, when to wait and when to ask                                       |
| **dispatch**     | sending each piece of work to the model that suits it                                                     |
| **distil**       | compile intelligence and wisdom into a face                                                               |
| **wisdom**       | a lesson learned the hard way, from failure                                                               |


## References


| file                       | what it covers                                                                                                       |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| `references/QUICKSTART.md` | from nothing to a first answer: install, sign up or in, a key, your own face, a first question                       |
| `references/CLI.md`        | every `hw` command and flag (TODO: generated from `hw --help`)                                                       |
| `references/SDK.md`        | the SDK (TODO: once the SDK exists)                                                                                  |
| `references/SETUP.md`      | installing `hw`, keys, and the plugin hooks for Claude Code and Codex                                                |
| `references/STATES.md`     | the causal state in full: reading the tree, what the human says, refine, builders and claims, every `state:` command |
| `references/FACES.md`      | distilling, compiling, finding, combining and sharing faces                                                          |
| `references/MODELS.md`     | the decoders you can name, the encoder's two speeds, and how to choose among them                                    |
