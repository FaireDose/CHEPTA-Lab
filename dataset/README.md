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


## Comparison examples

Use `comparison.template.json` for alternatives producing the same product. Populate `alternatives` with entries shaped like `alternative_record_contract`, then remove that explanatory contract from the completed record. Declare a common basis and record the evidence for all normalization. Keep objectives, fixed inputs, adjustable variables and their bounds distinct. Uncertain inputs without defensible bounds remain unknown.

A correct target may be a conditional recommendation, a trade-off or a request for missing information. Do not label the paper author's preferred option as the universal best route. Evaluate changed objectives/constraints and unseen process families as well as numerical reproduction. See the revised project plan for release and training gates.

The ethanol case in `cases/` is an executed draft, not accepted training data. Its two kinetic variants are not two complete process routes.
