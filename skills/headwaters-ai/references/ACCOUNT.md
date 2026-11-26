# Account, keys and cost

```bash
npm install -g @headwaters-ai/cli@latest         # install or update hw
hw account:register --email … --password '…' --username … [--plan connect|pro]   # see references/QUICKSTART.md first
hw account:login --email … --password '…'
hw account:whoami
hw account:balance                               # credit; account:topup adds more
hw account:usage                                 # what has been spent, and on what
hw account:subscription                          # the plan you are on (read only)
hw account:activate --plan connect               # subscribe from Free (charges the card)
hw account:plan pro                              # switch a subscription (charges the difference)
hw key:create --name "my-key"                    # a key for programs and agents, used as HW_API_KEY
hw key:list
hw key:edit <id> --budget 5                      # a spending cap
hw key:revoke <id>
hw config:set api_key <key>                      # save a key for hw on this machine
```

**Spending is the user's call.** Make no paid call (choices, decisions, chat, refine, compile) until the user has approved a budget, the data to be sent (point out anything personal or private), and which key will be used. A budget the user gives you with the task covers sending that task's own content; ask again before sending anything beyond it.

`hw <topic> --help` lists every command. Every command takes `--json` for machine-readable output.

Every account has a face of its own, aliased **`me`**. Compile the user's own writing into it rather than creating another.

**Plans.** Free pays as you go, with no monthly fee. Connect and Pro add monthly allowances for compiling and for Maestro. Eligible chat models run on a linked ChatGPT plan (`hw account:connect openai`).

**Cost.** Choices, decisions and chat are billed per token the encoder processes, plus the decoder's own price for decisions and chat. Compiling is billed per source token. Building and reading a causal state is free; refining it runs billed choices and decisions. For current prices, plans and limits, use `GET /v1/rates` and `GET /v1/models`.
