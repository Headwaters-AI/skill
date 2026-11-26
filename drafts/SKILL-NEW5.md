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
Headwaters tools provide a causal layer  for consistent judgement, taste, and discernment over arbitrarily long sessions. They help to tame and exploit the jaggedness of AI models, bring rigor to tasks and problems with no one right answer, and optimize the tradeoffs between halting and proceeding under imperfect partial information so tokens are used optimally.

## Causal Space

**State** is a pragmatic map of your world expressed in text. Headwaters tools let you become aware of and optimally manipulate your state by identifying and exploiting **causal relations**:  directional dependence that answers the question of *why* one state gives rise to another (sequence and consequence), rather than only which inputs are similar. The latent space of causal relations is called **causal space**.

The tools:

- **Causal State** is a goal-oriented external memory map made of co-dependent premises that you maintain to define current and future goal states on the same map. Refining a goal premise decomposes it into a de facto mathematical proof in the form of a probabilistic AND/OR tree that, when a sufficient and necessary set of it's leaf nodes (tasks, tests, data, etc) are verified true, serves as proof that you have reached your goal state. You can thus query the a refined state at any time to to identify the optimal path from current state to goal state so long as you update it on the fly as the environment (including instructions or requests from a human user) changes. Each causal state you create is addressable by a unique identifier (state-id) that you can pass to the Maestro inference models as  input and the state will be expanded into the optimal prompt.
- **Maestro** is a maskable  encoder for causal space. You use it for composing bespoke cause-driven inference models on demand by pairing it with one of three decoder types – choices, decisions, chat – that determine the output shape. By modeling causal relations rather than facts or knowledge drawn from co-occurrence (as in LLMs), Maestro  steers decoder models with causal invocation in an atomic inference call.
- **Faces** are masks compiled from source texts that distill the set of causal relations that define bespoke taste and judgement.

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

**New to Headwaters?** Follow `references/QUICKSTART.md`: it signs the user up or in, compiles their own face and asks it a first example question.

## Causal State (the `state` commands)

State is a pragmatic map of  your environment. If you are assisting a user, the environment includes and privileges the user. At any time, you have a current state and are likely to have a goal state you are working towards. Causal State is a tool to accurately construct your state with the necessary and sufficient precision for achieving your goals using causal relations. It is similar to memory tools, but rather than querying by semantic similarity, you query with `state:get` to identify causal weakness and thus the optimal path from current state to goal state.

 Causal state is built of premises (called `items`) with a finite set of properties and directional dependency edges. You build your current and goal states simultaneously  as information is received, tasks are assigned, tests are run, designs are made and re-made, and data changes. Use the `state:refine` tool to run a recursive sequence of abduction-induction analyses on your goal premises to break them down into probabilistic AND/OR trees that are complete when all leaf nodes can be verified true unequivocally with a single input (a user statement, a fact, a test result, an environment variable, etc). When all leaf nodes are verified true, the refined goal premise will necessarily also be true, and thus that aspect of your task will be achieved.

This process of refining to completion and then verifying each leaf node is called discerning. Discernment is not needed for rote or trivial tasks, but for any that have no one right answer (eg Pareto tradeoffs), are essential cornerstones in a larger task, 

Refining a task to completion effectively builds a punch list of sub-tasks. This allows you to optimally route tasks  by using a fast and cheap model call (including choices and/or decision models in place of a chat model), or a model whose jagged intelligence makes it uniquely suited for a task, or a subagent outfitted with the appropriate LLM and/or token budget, all depending on the nature of the task. Use the `state:claim` command to claim a branch (all the premises below a premise) for a subagent, which allows you to task parallel agents or even orchestrate a swarm of agents that will not collide.



It can take the form of plain text, messages, application data, results from tool calls, an event log including decisions taken, reasoning traces, and the like.



&nbsp;

&nbsp;

&nbsp;

- Querying provides structural weaknesses, get hints and recommendations for next steps, isolate invalidated decision points to roll back to or branch off of, know when to call a tool or ask a human user, and prove that your implementation truly solves the goal you were given based entirely on causal relations in your current and goal states. 

 Chat models often call this a "prompt" or "input". Decision and System One models, like Jev from TypeSafe AI, natively label their input "state".

State is different from context. Context is all the text provided for a single stateless inference request, and so context is updated on every turn. State is the stable but evolving source from which context is assembled. State is to hard disk storage as context is to RAM. Causal state lets you do memory paging using causal relations.

Decision models and choices already call their input a state. Chat models call theirs a prompt, messages, a system prompt, a developer or user message, tool calls and their results. State is the larger idea that holds all of these, so the same state can go to any decoder, and you can swap choices for a decision model or a chat model without rewriting what you send.

A state comes in one of two forms:

- **open-ended text** that you write by hand, in whatever format suits it, JSON included;
- **a state id** (`fs_…`), naming a causal state kept on the server and built with the `state` commands.

### The causal state

The Headwaters state tool allows you to construct a queryable state in the form of a graph of premises (referred to as `items` in the CLI). Each premise item has a finite list of properties:

- **key:** its name, in plain words, unique in the state;
- **value:** what it holds, as text or JSON;
- **description:** what the premise is, in a line;
- **role:** `goal` (to be proved), `test` (true or false of the finished work), or none (a fact);
- **parent:** the premise it refines, as an AND sub-goal (`--and`, all must hold) or an OR candidate (`--or`, one is enough);
- **on:** the premises it reads as inputs, which support it without refining it;
- **status:** `stated`, `verified`, `assumed`, `unresolved` or `invalidated`;
- **await:** what it waits on: `human`, `environment`, a test's key, or `none`;
- **origin:** who it comes from: `human`, `agent`, `tool` or `web`;
- **said:** the human's own words it comes from;
- **refinement:** `complete` or `incomplete`, whether its children are enough;
- **p:** for an OR candidate, how likely it is to work, as a decision ranked it.

It is your responsibility to update the state honestly and regularly. Each state command returns with a summary of the key aspects of the state and hints and recommendations on what to do next that are generated deterministically from the state topology.

#### Using State

Use state commands to `add` and `edit` premise items and their properties (including `await`, which marks a result that needs a tool call, an answer from a human user, or a poll of the outside world), and query the state with `get` to receive a summary of the AND/OR tree and hints and recommendations on what to do next.

- `state:choices` asks a face to propose candidates for an open premise (abduction), and `state:decide` ranks them by how likely each is to work (induction). A decision ranks and never prunes: only a failing test, or the human, refutes a candidate.
- `state:claim` gives a branch to one agent for a while, so several can work on one state in parallel without overwriting each other.
- `state:edit` records a test run: `--status verified|invalidated --tested <candidate> --evidence "<what the run showed>"`.

#### Principal Use Case: Discerning

The most powerful state tool is `hw state:refine`. This tool refines a premise item with `role=goal` into a probabilistic AND/OR tree using the principles of goal-oriented design (eg KAOS). It can be used recursively (`-r`), and it stops when it arrives at a leaf node: an atomic premise that is a test, or that requires input not found in the state (such as an answer from a human user, an event in the world outside the state, or a pending test result). Complete refinement of a goal premise will present you with a finite set of leaf nodes that, when verified true, propagate through the AND/OR tree to the original goal like a truth circuit.

Complete refinement followed by the verification of a sufficient and necessary set of leaf nodes to complete the AND/OR tree circuit and turn the original goal to verified true status is the process of discerning.

```bash
hw state:create --use                                # a new state, used by every hw call in this directory
hw state:add "the dinner is planned" "A dinner for six on Friday" --role goal --said "<their words>"
hw state:refine "the dinner is planned" --face @owner~face -r
hw state:get                                         # the tree, and what to do next
```

#### Handing a state to Maestro

First create a state and note its id (`fs_…`, printed by `state:create` and kept in `.headwaters/state`). Then you can pass that state by id to any Maestro model, in place of hand-written text, and the model reads the causal state as it stands.

> TODO: today only `POST /v1/choices` takes a state id, and the `maestro:*` commands take `--state` text only. Add a state id to `/v1/decisions` and the chat endpoints, and a `--state-id` flag to `maestro:choices`, `maestro:decide` and `maestro:chat`.
