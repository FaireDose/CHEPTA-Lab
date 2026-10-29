# Dataset preparation

There are currently **zero accepted training examples**. The catalogue is research metadata, not a dataset of correct engineering answers.

Copy example.template.json to create a draft. Each completed example should record:

1. The user's engineering request and which information is missing.
2. Referenced inputs with original units and a page/table/equation locator.
3. Component and reaction identities, catalyst and rate basis, property method and valid operating range.
4. Concise engineering decisions, assumptions and alternatives.
5. Executable input files plus the simulator commit/version.
6. Actual tool calls and tool outputs, including warnings and failed attempts.
7. Material/element/energy checks and an independent numerical or experimental comparison with justified tolerances.
8. Human engineering review and a source-rights review.

Keep measured data, source-reported simulations, our simulations and assumptions labelled separately. Do not put invented successful outputs in an example.

Only release examples after all checks are complete. Store related variations under the same family/source group when splitting training and evaluation data. Reserve unseen processes to test transfer.

A future training exporter can convert accepted examples into conversations with tool calls and results. No exporter or training configuration is supplied until the first real case establishes the format.
