# Faces

A face is a mask compiled from a body of source texts. Paired with Maestro, it steers choices, decisions and chat with the judgement those texts carry. This guide covers making, compiling, finding, combining and sharing faces.

## Finding a face

```
hwai face:list --for "<the judgement you need>"          # your faces, best fit first
hwai face:list --for "<…>" --public                      # with everyone's published faces
hwai face:list --public --search "<words>" --sort usage  # the most used published faces that match
hwai face:list --system                                  # the curated system faces
```

`--for` ranks faces by how well their description and specialty fit the task, with a fit score beside each. A weak best fit is the sign to make a face. `--limit N` shows more than the top 10.

Each branch of a causal state has its own task, so its best face can differ from the root's.

## Making a face

```
hwai face:create --name "Home Cook" --alias home-cook \
  --description "An experienced home cook who plans meals for groups" \
  --specialty "Planning and cooking meals for groups of guests"
```

- **alias** is how the face is named in a model string: `@you~home-cook`.
- **description** and **specialty** are what `--for` matches against. Write them as what the face is good for, in the words someone would use when looking for it.

## Compiling sources into it

A face learns from its author's own words. Give it writing where the judgement shows: how they decide, what they weigh, what they refuse. A face is only as good as its sources.

```
hwai face:compile home-cook --file notes.md --medium essay
hwai face:compile home-cook --file interview.txt --kind thread --face-speaker "Sam"
```

- **A document** (the default kind) is one author's own writing. Every word in it is read as theirs. Say what kind of writing it is with `--medium` (essay, email, speech, journal entry, script and the rest; `other` when nothing fits). `--perspective first-person|third-person` says whose voice it is in.
- **A thread** is a conversation, interview or transcript. Name the face's speaker with `--face-speaker`; the other speakers are read as context, never as the face.
- **Never pass a multi-speaker transcript as a document.** Every word would be read as one author's.
- **More sources sharpen a face,** and a face can be compiled again with new ones at any time. For a dispatcher or any face of lessons, add each new lesson document and compile again.
- **Cost and time:** compiling is billed per source token and takes a while. `--rush` starts it as soon as possible, at a higher rate only if it starts before its scheduled start. A face runs at most 3 compiles at once; more wait their turn. Plans include a monthly compile allowance. `hwai face:compile --help` lists the status and pause commands.

A face can be used as soon as something in it is compiled. A face with nothing compiled answers `409`.

## Combining faces

Faces combine in the model string, with boolean operators: `(@you~home-cook | @someone~sommelier):maestro-1/<decoder>`. Combining is for when two faces together cover a judgement that neither covers alone.

> TODO (#2081): the operators and their meaning are under review, and a set form may replace them. Update this section once #2081 settles the syntax.

## Sharing

```
hwai face:publish home-cook     # list it in the public catalog, for everyone
hwai face:share home-cook ...   # give it to chosen accounts
```

`face:unpublish` and `face:unshare` undo them. Others name a shared face with its owner: `@you~home-cook`.

## What a face is not

A face is not a system prompt or a document pasted into a model's context, and not a fine-tuned copy of a model. It is a mask over Maestro: it takes its shape from each state it reads, and steers what the decoder produces.
