# What Faces is

Faces are **causal models**. A face distills the essence of a particular author from
unstructured source texts: essays, blog posts, emails, letters, interviews, talks. When
prompted, a face returns a **cause**: the principal *why* that would motivate that author's
response in the given context. Causes steer other AIs, so an agent keeps a consistent, specific
point of view however long it runs.

Causes are upstream of reasons. A reason is what you tell a police officer when they ask why
you did not stop at a red light; a cause is how you decided what to say.

## The APIs

| API | Endpoints | Returns |
|---|---|---|
| Choices | `/v1/choices` | the options the face would weigh, strongest first, or the question it would ask |
| Decisions | `/v1/decisions`, `/v1/systemone` | typed `answers`, with a `cause` per question |
| Causes | `/v1/causes` | the `cause` alone |

In the CLI: `faces choices` asks a face what it would do, `faces decide` asks for typed answers
(`face@decision-model`), and `faces causes alice -m "…"` returns the cause alone. Chat is
retired: its endpoints answer `410`.

A choice is open: the face proposes the options. A decision is closed: the decision model picks
among the options or levels given, and returns typed answers. The two chain: a choice's option
names can be the options of a decision.

## Compiled, not trained

A face is compiled from unstructured text. There is no dataset to prepare and no training run,
and a face is not tied to any one model. Add a
source and compile it; delete one and what it contributed goes with it. A face's cost per
request does not depend on how much has been compiled into it.

Sources come in two kinds. A **document** is the face's own writing (an essay, letter, paper,
book or poem), and every word in it is read as the face's. An **interview, transcript or
dialogue is a thread**, uploaded with the face's speaker named, so only the face's turns are
used.

## Composable and comparable

Faces combine with **boolean set algebra** into composites:

| Operator | Syntax |
|---|---|
| Union | `a \| b` |
| Intersection | `a & b` |
| Difference | `a - b` |
| Symmetric difference | `a ^ b` |

Parentheses group: `(a | b) - c`. A composite can be **persisted** as a named face
(`face:create --formula "a | b"`) or composed **per request** by putting the formula where a
face goes (`faces choices "(a | b)" --state "…"`). A formula whose result is empty is refused with `422 empty_composite` ("the
intersection between these two faces is null"). See
[REFERENCE.md → Run-time composite faces](REFERENCE.md#run-time-composite-faces).

Compiled faces are also **comparable**: `face:diff` scores how alike two faces are, from `-1` to
`1`, and `face:neighbors` finds the most and least similar faces to one face. When either face
is not yours, the similarity is rounded to one decimal place, and neighbors with the same rounded
score are listed by owner, then alias.

## Style

Every source text has a **medium**: `email`, `text message`, `social post`, `essay`,
`academic paper`, `blog post`, `legal document`, `thread reply`, `conversation`, `lecture` or
`other`. A **style build** reads a face's own writing in one medium and installs a style for
that medium, so the face writes better in it. A face holds a separate style per medium.

A style was applied with `--style <medium>` on the chat commands, which are retired with chat;
no command applies one now. See
[REFERENCE.md → Style](REFERENCE.md#style-how-a-face-writes-style).

For example use cases, see [USE_CASES.md](USE_CASES.md).
