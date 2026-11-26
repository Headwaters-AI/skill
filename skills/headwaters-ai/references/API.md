# Building with the API

Use the HTTP API for any language, or `hw` for scripts and probing. The chat endpoints are drop-in replacements for OpenAI's and Anthropic's, so an existing client changes only its `model`: `@owner~face:maestro-1/<chat model>`.

**The live docs are the source of truth** for request syntax, limits, prices and current behaviour. Read the relevant pages as part of the task:

- Documentation index: `https://docs.faces.sh/llms.txt`. Append `.md` to a page path for Markdown.
- OpenAPI spec: `https://api.faces.sh/openapi.json`. The API base is `https://api.faces.sh/v1`, and every call sends the key as `Authorization: Bearer <key>`.
- Prices and limits: `GET /v1/rates`. Models: `GET /v1/models`.

These move to `docs.headwaters.ai` and `api.headwaters.ai` after the move to headwaters.ai; use whichever resolves. If you can't reach the docs at all, say so and leave out version-dependent details rather than guessing them.

## Errors

Errors return JSON with a `detail` you can show as it stands.

- `422`: the request has the wrong shape. The message shows the right form.
- `409`: the face has nothing compiled yet, or is busy.
- `429`: a limit was hit. The message says when it resets.
- `503`: retry after `Retry-After`.
- A long call may return `200` with an `error` body if it fails after it started. Treat that as a failure.
