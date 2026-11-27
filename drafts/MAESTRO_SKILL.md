Maestro is an opinionated upstream model.

It is opinionated because it provides responses specific to the `face` provided as a mask, rather than general responses. A `face` is a compiled module that distills the essential perspectives latent in a given corpus of source texts that can be used to mask Maestro. Applying a `face` as a mask to Maestro biases it with those distilled perspectives, shifting the mode of its its internal distributions and thus its responses. A `face` is not a character prompt or static soul document like SOUL.md nor is it a trained module like the LoRA approach to PEFT, it is instead a lens that adapts to the model inputs in order to distort what passes through to the model. A `face` applied as a mask is thus akin to a perceptual nervous system for a model that shifts its state, and what it attends to, as the input changes.

Maestro is called an upstream model for two reasons: (1) its outputs are meant to flow into the inputs of other models downstream; and (2) it has multiple optional inputs that, if not provided by the caller, are produced as part of the output

### Choices Endpoint (cli: `maestro choices`)
The native form of Maestro is found at the choices endpoint, which requires the input of a state and two additional optional inputs: mask (a `face`) and question (a text). State is the text and application data from which you want to solicit a response. If any of the optional inputs are not provided, Maestro first selects and/or generates, respectively, the `face` and question that best corresponds to the given state. It then generates its principal output, a list of possible choices, alongside any `face` and/or question it was responsible for generating.

### Wrapper Endpoints (cli: `maestro decide`, `maestro chat:chat`)
Maestro generates its list of possible choices by first identifying the motivating `cause` latent in the duet of state and face-mask and then applying them to the question. This cause takes the form of a latent `why code` that can be used for generating choices or steering downstream decision models and chat models. To use the `why code` to steer downstream decision and chat models, use the wrapper endpoints with a given face-mask: they will generate the `why code` with the face and input and then use it to steer the wrapped downstream models. As a caller, you send your input and a face-mask and get an opinionated output in the form of either probabilities over a finite output set or open ended chat text.

## Decomposition
Decomposition is one of the superpowers of Maestro. It 


## Dispatching
