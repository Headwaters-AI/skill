---
name: headwaters-ai
license: MIT
description: >
  Headwaters integration craft for Maestro, an upstream encoder model that reads application state
  through a face (a mask compiled from a body of source texts) and steers a downstream model: our
  choices, a decision model such as Jev, or a chat model. Use when building, reviewing, or debugging
  code that calls Headwaters or the `hw` CLI; when making, choosing, or combining faces; when
  breaking a task into a causal state and keeping it true; when dispatching work to the right model;
  or when brainstorming where someone's taste and judgement fits in an app.
---

# Build with Maestro

**Maestro** is an upstream encoder model that is always atomically paired with a downstream model which acts as its decoder. Maestro reads a state (the text and data of a situation) through a **face**, a mask compiled from a body of source texts, and distils both into a latent **why code**, the cause that steers the decoder. The why code passes from encoder to decoder inside the model and is never part of the output. The decoder type you specify determines the output shape.

Face, encoder and decoder together make up a complete inference model. They are specified as a single string in API and CLI calls, `@owner~face:encoder/decoder`, for example: `@zerocool~redteam:maestro-1/gpt-6-astra`.

Faces are composable, so boolean algebra can combine them on the fly right in the model string, for example: `(@zerocool~redteam | @acidburn~worldspacedev):maestro-1/gpt-6-astra`.

> TODO (#2081): every face is to be named with its owner, even your own, and the composite operators are under review. Update the examples here once #2081 settles the syntax.

## Natural Language Signal Processing

Maestro can be used in many different ways. The most complete metaphor that encapsulates all of them is that of building natural language signal processing (NLSP) circuits out of three software primitives that behave like smart versions of existing hardware modules: the demultiplexer, a demux→mux cascade, and a modulator. Each provides a different mode of inference.

| decoder | component | inference mode | output |
|---|---|---|---|
| `choices` | a **smart demultiplexer** | **abduction** | one state in, a set of possible choices out, weighted by what the face sees |
| `<decision model>` | a **smart demux→mux cascade** | **induction** | the situation fanned out, then collapsed back onto the options you give, as calibrated probabilities |
| `<chat model>` | a **smart modulator** | **broadcast** | the chat model's own reply, carrying the why code's signal |

Each of these components can be modeled as a black box with an input, an output and a control: select lines for mux and demux, and for a modulator a signal that rides on the carrier wave. For Maestro, a face is like an adaptive control line that is itself a function of the input, mutating the mask it applies to the input based on the perspectives captured by the face.

Faces thus impart a layer of taste and judgement over the model as a whole. Making faces and choosing the right face at the right time is a form of metaprogramming.

In short: Choose the face for whose taste and judgement you want and choose the decoder for the form you want it in and the level and type of intelligence you need.

### The three decoders in practice

| decoder  | endpoint                                                                                           | CLI                  | you send                                                                                                    | you get back                                                                                                                                                       |
| -------- | -------------------------------------------------------------------------------------------------- | -------------------- | ----------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| choices  | `POST /v1/choices`                                                                                                   | `hw maestro:choices` | a state (prose up to 3,000 tokens, or a causal state id), and optionally a question                         | up to `max_choices` options, strongest first, each a short name and a sentence. Without a question, the face proposes the question it would ask. |
| decision | `POST /v1/decisions` (OpenAI's Decisions format) or `POST /v1/systemone` (TypeSafe AI's Jev model System One format) | `hw maestro:decide`  | the situation and typed questions: `choice` (pick one), `predicate` (yes or no) or `score` (a graded scale) | a probability for each option, level or yes, plus the top answer                                                                                 |
| chat     | `POST /v1/chat/completions`, `/v1/messages`, `/v1/responses`                                                         | `hw maestro:chat`    | a conversation                                                                                              | the chat model's reply, in that API's own standard shape                                                                                         |

On `/v1/choices` the decoder is our own, `choices`, named like any other: `@owner~face:maestro-1/choices`. The chat endpoints are drop-in replacements for the OpenAI and Anthropic APIs: point a client at the API base and change only `model`.

`maestro-1-fast` is the same encoder, answering sooner, at ten times the price. Use it when latency matters more than cost.

## Live docs

The live docs are the source of truth for request syntax, limits, prices and current behaviour. Read the relevant pages as part of the task.

- Start at the [documentation index](https://docs.headwaters.ai/llms.txt). Append `.md` to a page path to get it as Markdown.
- Exact schemas: the [OpenAPI spec](https://api.headwaters.ai/openapi.json).
- Prices, plans, allowances and limits: `GET /v1/rates`. Every model you can name, with its price: `GET /v1/models`.

If you can't reach the live docs, say so, and leave out details that depend on the version rather than guessing them.

> TODO (#2080): these hosts are live only after the move from faces.sh. Until then, use `https://docs.faces.sh` and `https://api.faces.sh`.

## Setup

```
npm install -g @headwaters-ai/cli      # the hw CLI
hw auth:register                        # a new account, from the terminal (or hw auth:login)
hw keys:create                          # a key for programs
```

Or set `HW_API_KEY` in the environment. **New to Headwaters? Follow `references/QUICKSTART.md`:** it signs the user up or in, compiles their own face and asks it a first question. The plugin hooks (Claude Code and Codex) are in `references/SETUP.md`.

## Workflow

1. **Start from what the application decides.** Write down what your code will show, pick, change or hand off, and what judgements it needs to get there. Arithmetic, dates, lookups and policy belong in code. Judgements that need someone's taste belong to a face.
2. **Pick the decoder for the shape you need:** options to consider (choices), a number to act on (a decision), or words to show someone (chat).
3. **Find or make the face.** `hw face:list --for "<the judgement>"` ranks faces by fit, `--public` includes everyone's published faces. Make one when nothing fits well (see [Making a Face](#making-a-face)).
4. **Probe the live API** with representative, hard and negative cases (see [Test with the live API](#test-with-the-live-api)).
5. **Integrate.** Keep the model strings, questions and options in one module. Log the exact request. Surface a failed call as an error, never as an answer.

For work with many parts, build a causal state first (see [Causal State](#causal-state)): it breaks the task into premises, and each one becomes a small decision or a test.

## Design the state and the questions

The **human test**: could a smart person, shown only this state and this question, answer quickly? When a call fails the test, fix the state before the wording.

- **Give what a person would look at:** who said what, the full situation rather than a truncated line, names rather than raw IDs. State facts your code already knows.
- **Keep every part relevant.** A detail added for one question can sway the answer to another.
- **One judgement per question.** Two conditions joined by "and" or "or" are two questions. Combine the answers in code.
- **Name options by what they are.** `refund_request` helps; `option_1` gives nothing to go on. Choices' `name`s are written to be used directly as a decision's options.
- **Write plainly.** A question is not a prompt: no preambles, no output-format instructions.

## Read the answers

- **A choice's options come strongest first,** in the face's own terms. The first is the face's lead, not a verdict: weigh them with a decision when your code must pick.
- **A decision's probability is the likelihood the answer is correct, as this face judges it.** Do any arithmetic on it in code. For a yes or no, 0.7 and 0.3 make good starting thresholds, and the band between means the state does not settle it: give that band its own outcome.
- **No clear winner** among options (top probability under 0.6, or a lead under 0.2) usually means the choice is not the model's to make. Ask the person it belongs to.
- **A chat reply is the chat model's own,** steered by the face. The why code itself is never returned.

**Errors** come back as JSON with a `detail` you can show as it stands. `422` means the request is the wrong shape, and its message shows the right form. `409` means the face has nothing compiled yet, or is busy. `429` names the limit and when it resets. `503` is the one to retry, after `Retry-After`. A long call may answer `200` with an `error` body if it fails after it started: treat that as the failure.

## Cost

Choices, decisions and chat are billed per token the encoder processes, plus the decoder's own price for decisions and chat. Compiling a face is billed per source token. Building and reading a causal state is free; refining it runs billed choices and decisions. Plans include monthly allowances. Current prices: `GET /v1/rates` and `GET /v1/models`.

## Test with the live API

Ask the user before sending test requests. Agree a budget, say what data will be sent (point out anything personal or private), and say which key will be used.

- Start with a few representative cases, plus hard ones and ones whose answer is "no".
- Compare faces or wordings on the same state, side by side.
- **Read the individual outputs, not only the counts.** Two faces can return the same number of options where one is faithful to the situation and the other is fluent nonsense.
- Keep the exact request for each case so any result can be rerun.

### When an answer looks wrong

Check, in this order:

1. the request as actually sent, including the model string;
2. the state, against the human test;
3. the face: does `hw face:list --for` rank it well for this judgement, and is it compiled?
4. the options: is the right answer among them?
5. the scope: can the question be split into smaller judgements?
6. the wording.

**Yellow flags.** Wording written to produce a particular answer tends to break on the next input. Watch for options that name test cases, thresholds fitted to a handful of cases, and code that quietly overrides answers. The fix is usually a better state, a separate question, a different face, or code.

## Making a Face

**Why.** A face is the judgement you want carried into a decision: a person's, a role's, or one you assemble for a job, such as a dispatcher. Make one when no existing face fits the work. `hw face:list --for "<the task>"` ranks your faces, and with `--public` everyone's published faces, by how well each fits; a weak best fit means it is time to make one.

**What to compile from.** A face is only as good as its sources. It learns from the author's own words, so give it writing where the judgement shows: how they decide, what they weigh, what they refuse.

- **A document** is one author's own writing: essays, notes, posts, a set of lessons. Every word is read as theirs.
- **A thread** is a conversation, interview or transcript, where only one speaker is the face. Name that speaker, and the others are read as context.
- Several sources can go into one face. More sources sharpen it, and a face can be compiled again later with new ones.

**How.**

```
hw face:create --name "Home Cook" --alias home-cook \
  --description "An experienced home cook who plans meals for groups" \
  --specialty "Planning and cooking meals for groups of guests"
hw face:compile home-cook --file notes.md --medium essay
hw face:compile home-cook --file interview.txt --kind thread --face-speaker "Sam"
```

- The **description** and **specialty** are what `face:list --for` matches a task against, so write them as what the face is good for.
- **Compiling** is billed per source token, and takes a while. `--rush` starts it as soon as possible, at a higher rate only if it starts before its scheduled start. A face runs at most 3 compiles at once; more wait their turn. Plans include a monthly compile allowance.
- **Use it** as soon as it is compiled: `@you~home-cook:maestro-1/<decoder>`.
- **Share it:** `face:publish` lists it in the public catalog, and `face:share` gives it to chosen accounts.

The full guide is in `references/FACES.md`.

## Causal State

Causal state lets you work under the direction of a human the way a mathematician works on a proof over time. The human gives you the problem, often in pieces. Maestro helps you assemble those pieces into a state: a probabilistic AND/OR tree that shows at once what you are trying to prove and how much of it is proved so far.

The tree follows goal-oriented requirements engineering (KAOS). A goal is refined into sub-goals that must all hold (AND), or into alternatives of which one is enough (OR). Every box in the tree is proved, refuted or open, and truth flows upward: an AND is proved when all its children are, an OR when any one is.

The work follows Peirce's cycle, with refinement before it: **refine** a premise into its children; **propose** candidates for an open choice (abduction); **weigh** them, to know which to try first (induction); **verify** with tests that are true or false of the finished work (deduction). `hw state:refine` does the first three for you, using choices and decisions under a face of your choosing.

```
hw state:create --use                                  # a state for this directory
hw state:add "the dinner is planned" "A dinner for six on Friday" --role goal --said "<their words>"
hw state:refine "the dinner is planned" --face @you~home-cook
hw state:get                                           # the proof, with its checkboxes
```

Every task becomes part of a proof in progress. Your job is to complete it, and to keep it true as things change. The full guide to the state is in `references/STATES.md`.

## Dispatching Intelligence

Faces compile the perspectives latent in a corpus of source texts. They can be made, updated and combined on the fly to suit the task. Curating the right face and the right model for each piece of work is intelligence dispatch, and a causal state is what makes it possible: once a task is refined into premises, each leaf is a small, well-defined piece of work that can go to the model that suits it.

**The loop:**

1. **Shape the proof with your strongest model.** Run on the most capable model you have, create a state, and refine the task down into premises. Refinement is where judgement matters most, so it gets the best model.
2. **Dispatch the leaves.** With the premises written, take a whitelist of models and assign each piece of work: simple ones to smaller, cheaper models, hard ones to stronger models, or keep them yourself.
3. **Record what happened.** When a dispatched piece succeeds or fails, write the lesson down in the first person, as the situation and what you learned. For example: "When a task merges records across dated changes, I give it to the stronger model: the small one follows the first change and stops."
4. **Compile the lessons into a dispatcher face.** Add each new lesson document to your own face, e.g. `@you~dispatcher`, and recompile. The face now carries your routing judgement.
5. **Dispatch with the face.** For each new piece of work, ask a decision steered by your dispatcher which model to use: `@you~dispatcher:maestro-1/jev-latest`, with the question "Which model should this task be dispatched to?" and your shortlist of models as the options.

**Seeding the dispatcher.** Before you have your own results, start from what others have learned:

- **Inherit a public dispatcher.** Published faces are listed with `hw face:list --public --search "dispatch" --sort usage`. The most used ones have been relied on most by others. Take the one that fits your whitelist as a baseline.
- **Research your whitelist.** Find what has been reported about each model, and write it as lessons too. Mark each one as reported rather than observed ("Reported, not yet seen in my runs: …"), so your own results can overrule it as they arrive.

**Keep your lessons beside the inherited ones.** Your own `@you~dispatcher` holds your lessons, and the inherited face holds theirs. Combine the two in the model string, so you dispatch with both: `(@you~dispatcher | @someone~dispatcher):maestro-1/jev-latest`.

> TODO (#2081): the meaning of `|` and the other composite operators is under review, and a set form such as `@you~{dispatcher,…}` may replace them. Update this example once #2081 settles the syntax.

Keep the lessons honest. A lesson comes from a run you have read, not from a guess, and a dispatcher is worth checking now and then against how its picks actually turned out. The models you can dispatch to, and how to weigh them, are in `references/MODELS.md`.

## Patterns

Each of these combines the decoders to serve one goal.

- **Propose, then decide.** Ask a face for the options it would weigh (choices), then hand those names straight to a decision as a `choice` question, under the same face or a different one. Abduction then induction, in two calls.
- **A panel.** Ask the same decision under several faces, side by side, and compare how each leans before anything is written.
- **Steer a reply.** Swap the `model` of an existing OpenAI or Anthropic client for `@owner~face:maestro-1/<chat model>`. Nothing else changes.
- **Run a task as a proof.** Build a causal state, refine the goal, dispatch the leaves, and record each test run, until the root is proved.
- **Route with a dispatcher.** Ask `@you~dispatcher:maestro-1/jev-latest` which model a piece of work should go to, and keep the shortlist in code.

## Glossary

| term | meaning |
|---|---|
| **Maestro** | the upstream encoder model: it reads a state through a face and produces a why code |
| **face** | a mask compiled from a body of source texts; whose judgement steers the output |
| **why code** | the cause Maestro distils from the state and the face; it steers the decoder and is never returned |
| **cause** | what a why code holds: why the face would act |
| **decoder** | the downstream model that turns the why code into output: choices, a decision model or a chat model |
| **model string** | face, encoder and decoder named together: `@owner~face:maestro-1/<decoder>` |
| **state** | the situation sent with a call: prose, or a causal state |
| **causal state** | an AND/OR proof tree of premises, kept on the server and kept true as things change |
| **premise** | a node of a causal state: a goal, a test or a fact |

## References

| file | what it covers |
|---|---|
| `references/QUICKSTART.md` | from nothing to a first answer: install, sign up or in, a key, your own face, a first question |
| `references/SETUP.md` | installing `hw`, keys, and the plugin hooks for Claude Code and Codex |
| `references/FACES.md` | making, compiling, finding, combining and sharing faces |
| `references/STATES.md` | the causal state in full: reading the tree, what the human says, refine, builders and claims, every `state:` command |
| `references/MODELS.md` | the decoders you can name, the encoder's two speeds, and how to choose among them |
