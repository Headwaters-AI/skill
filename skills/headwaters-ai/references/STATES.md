# Causal state

Causal state lets you work under the direction of a human the way a mathematician works on a proof over time. The human gives you the problem, often in pieces. Maestro helps you assemble those pieces into a state: a probabilistic AND/OR tree that shows at once what you are trying to prove and how much of it is proved so far.

The tree follows goal-oriented requirements engineering (KAOS). A goal is refined into sub-goals that must all hold (AND), or into alternatives of which one is enough (OR). A refinement is complete when its children together are sufficient, and minimal when none of them can be dropped. Every box in the tree is proved, refuted or open, and truth flows upward: an AND is proved when all its children are, and an OR when any one is.

The work follows Peirce's cycle, with refinement before it:

1. Refine a premise into its children, which gives the tree its shape.
2. Propose candidates for an open choice (abduction).
3. Weigh them, to know which to try first (induction).
4. Verify with tests that are true or false of the finished work (deduction).

`hw state:refine` does steps 1 to 3 for you. It decides whether a premise needs splitting into conditions, pinning to one meaning, a single test, or the human's answer, then proposes and judges the children with tested prompts. That leaves you free to do what only you can: write the tests, and the code that passes them.

The state also tells you where you are. Your commands, and hooks that run in the background, show you the tree with its checkboxes and a last line naming what still stands between you and a proved goal: what to refine, what to run, and where to wait. Waiting is how a branch pauses: on the human's answer, a test that is running, or something outside that has to change. The other branches go on.

Every task becomes part of a proof in progress. Your job is to complete it, and to keep it true as things change. That is truth maintenance.

## Reading the tree

`hw state:get` prints the tree, one box per line:

```
[ ] 1 the dinner is planned  AND
[x]   1.1 the guests and their needs (axiom)
[ ]   1.2 the menu  OR
[-]     1.2.1 curry, quinoa salad, sorbet (p 0.71)
[ ]     1.2.2 pasta, salad, tiramisu (p 0.29, next to try)
[ ]   1.3 test: each guest can eat each dish (failed on 1.2.1)

Open. Next to try: 1.2.2 (p 0.29). Proved when 1.3 passes on 1.2.2.
```

- `[x]` proved, `[ ]` open, `[-]` refuted. The operator is written once, on the parent: AND or OR.
- The numbers belong to the view and change as the tree changes. Every command names a premise by its key, the text after the number.
- A box the human stated is an axiom: true because they said it. A box with children is proved only once its refinement is complete, and then by its children. A box you or a face wrote with no children is open until a test that reads it passes.
- An OR's candidates are listed highest p first. p is how likely each one is, which says which to try first; it never rules one out. A candidate is refuted when a test run on it fails, or when the human turns it down, and the next one becomes the one to try.
- A test is proved or refuted by its runs. A test that reads an OR records each run against the candidate it ran on.
- A box that waits says on what: `awaits human`, `awaits environment`, or the test it waits for. A claimed box names who holds it.
- The last line is the whole state in one sentence: proved, refuted and why, or open, with the next candidate to try and the open boxes whose proof would prove the root. The work is done when the root is proved. Each open box on that line is either something the state can settle (refine it, run its test, weigh its candidates) or something only the human knows, and waiting on one branch leaves the others free to go on.

`state:get "<key>"` shows one box and its branch the same way, then every message linked to it in full: what the human said, notes, and the evidence of each run. `--query "<text>"` on either finds the boxes that best match by meaning.

## What the human says, in the state

- A task is a goal: `state:add "<key>" "<value>" --role goal --said "<their words>"`. A condition they set on it (a budget, a deadline, a must) is a goal of its own under it, `--and "<the task's key>"`.
- A fact they give (what they have, who is coming, what is true) is a box with no role, linked to their words with `--said`, placed under what needs it (`--and`) or read by what uses it (`--on`).
- Their answer to a box that waits on them fills it: `state:edit "<key>" --value "<the answer>" --await none --said "<their words>"`. Filled with their words, it is their fact.
- An explanation, a part of an answer or a metaphor is linked to the box it is about: `state:edit "<key>" --said "<their words>"`. It changes nothing else.
- A question about progress is answered from the tree; reading it writes nothing.
- A change to the task itself is a new value on its goal (`state:edit "<the goal's key>" --value "<new value>" --said "<their words>"`). Its refinement becomes incomplete, and the next `state:refine` checks its children against the new value. A new name is `state:edit "<key>" --key "<new key>"`; everything that named it follows.
- A candidate they turn down: `state:edit "<candidate>" --status invalidated --said "<their words>"`.

## Faces and builders

A face is an expert the state consults: it proposes the children of a premise and the candidates of a choice, and steers the decisions that judge and weigh them. `hw face:list --for "<the task>"` ranks the faces that fit a task; each branch has its own task, so its best face can differ from the root's. Every command that consults a face takes it as `--face @owner~alias` and is billed per call.

A builder is a subagent that works one branch. `state:claim "<key>" <name>` gives it the branch: the box and everything under it, never its inputs. Any write into the branch by anyone else is refused until the claim is released (`state:claim "<key>" --release`) or expires after 30 minutes, and the session-end hook releases the session's claims. A builder writes with `--as <name>`. `state:get "<key>"` is the branch as a builder reads it.

A test run is recorded on the test: `state:edit "<test>" --status verified|invalidated --tested "<candidate>" --evidence "<what the run showed>"`. `--tested` names the candidate the run was on, when the test reads an OR. A run that cannot happen yet is `--await environment`, or `--await "<the test it needs first>"`.

## Commands

```
hw state:create --use                          a new state for this directory (.headwaters/state)
hw state:use <id>                              point this directory at a state
hw state:get [--query "<text>"] [--json|--problog|--dot]   the tree and its last line
hw state:add "<key>" "<value>"               a new box; refused if the key exists
    --role goal|test   --and "<parent>" | --or "<parent>"   --on "<a>,<b>"
    --said "<their words>"   --await human|environment|<test key>   --origin   --status   --description   --as <who>
hw state:edit "<key>"                        changes only what it is given; refused if the key does not exist
    --value   --key "<new key>"   --status   --description   --await ...|none   --note "<text>"
    --evidence "<text>"   --tested "<candidate>"   --on "<a>,<b>"   --said "<their words>"   --as <who>
hw state:get "<key>" [--depth N] [--up] [--query "<text>"]   one box, its branch, and its messages
hw state:delete "<key>"                      removes it and its edges; the history keeps it
hw state:claim "<key>" <who> | --release     claims or releases a branch
hw state:refine "<key>" --face @owner~alias [-r [--depth N|all]]   refines it: conditions, candidates ranked, one test, or a question for the human; -r goes on down its branches, breadth first (3 levels by default), and its last line gives the calls, the dollars and the branches waiting
hw state:choices "<key>" --face @owner~alias [--question "<q>"]   candidates for it, from the face
hw state:decide "<key>" --face @owner~alias       ranks its candidates
hw face:list --for "<task>"                    the faces that fit a task, best first
```

> TODO (#2082): the project directory name (`.headwaters/state` here) and the exact flags follow the `hw` CLI as built; check against `hw state --help` once #2082 is dogfooded.
