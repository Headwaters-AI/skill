# Models

Every call names one complete model: a face, the encoder, and a decoder, `@owner~face:encoder/decoder`. This guide covers the parts you choose and how to choose among them. Current names, prices and limits are on `GET /v1/models` and `GET /v1/rates`; read them rather than relying on any list here.

## The encoder

| encoder | use it when |
|---|---|
| `maestro-1` | the default |
| `maestro-1-fast` | latency matters more than cost: it answers sooner, at ten times the price |

## The decoders

**Choices** is our own decoder, on `POST /v1/choices`, named like any other: `@owner~face:maestro-1/choices`. Any other decoder there is refused, and `/choices` is refused on every other endpoint.

**Decision models** answer typed questions with probabilities, on `POST /v1/decisions` or `POST /v1/systemone`. List them with `GET /v1/models?kind=decision`. They differ in price and in how much state they can read; the limits are on `GET /v1/rates`. A state that does not fit one decision model's limit has to go to another, or be cut down.

**Chat models** write replies, on `POST /v1/chat/completions`, `/v1/messages` and `/v1/responses`. Any model `GET /v1/models` lists as `kind: "chat"` can follow the slash. On the Connect and Pro plans, a linked ChatGPT account can carry eligible chat models on the user's own plan.

## Choosing

Choose along each of these, in this order:

| axis | the choice | what decides it |
|---|---|---|
| output shape | choices, a decision model, or a chat model | options to consider, a number to act on, or words to show |
| face | which face, or which combination | whose judgement the work needs |
| decoder size | a small, cheap model or a large one | how hard the judgement is, and what it is worth |
| context | each model's limit | a hard rule: what does not fit must go elsewhere |
| encoder speed | `maestro-1` or `maestro-1-fast` | latency against price |

**Start small and escalate.** Send each call to the cheapest pairing that might do, and escalate to a larger decoder only when the answer is unsettled: a yes or no near 0.5, or options with no clear winner. Most of the saving comes from the calls that never needed the large model.

**Measure, don't assume.** Which model handles which work well is learned, not given. Run the same state through two pairings, read the outputs side by side, and record what you find as lessons in a dispatcher face (see Dispatching Intelligence in `SKILL.md`). Counts alone are not quality: two models can return the same number of options where only one is faithful to the situation.
