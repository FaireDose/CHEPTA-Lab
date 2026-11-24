# Inherent safety (generated; do not edit)

Safer routes from the first flowsheet: principles, indices and missing hazard data. 8 rules. [All topics](../rules-readable.md)

Each rule starts with what to do in one line, then When (the situation you recognise), Do, Why, Check (how to verify it, in CHEPTA where it applies) and Result (what the source got), then its status and source with page. A lead is a rule from the literature that Lab has not yet tested.

- **Detailed safety indices belong to detailed engineering, not the concept stage**
  - When: You choose a safety method for the current stage of design.
  - Do: Use simple indicator-based indices early. Keep indices that need equipment, complexity and vulnerability data, such as the inherent system safety index, for detailed engineering.
  - Why: The data these methods need differ by stage.
  - Check: Check that the index's inputs are available at your stage.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Park et al. 2022, *Progress in Inherently Safer Design for Chemical…* (https://doi.org/10.3303/CET2290078), Section 2.3, p. 466. <!-- park-2022-inherently-safer-design.detailed-indices-later -->

- **Missing flash point or flammability limits for a pure organic: estimate them from simple correlations and label them**
  - When: Flash point, heat of combustion or flammability limits are missing for a pure organic compound.
  - Do: Estimate them with simple regressions on atom counts, molar mass and normal boiling point. Label the values as estimated and replace them with data later.
  - Why: The correlations use molecular data that are readily known.
  - Check: Treat the upper flammability limit with most caution, as it is the least reliable, and keep estimated and measured values apart.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Park et al. 2022, *Progress in Inherently Safer Design for Chemical…* (https://doi.org/10.3303/CET2290078), Section 2.2.2, pp. 464-466 (Eqs. 1-4, Figs. 1-2). <!-- park-2022-inherently-safer-design.estimate-missing-flammability-data -->

- **Remove or reduce a hazard before adding protection**
  - When: A hazard is to be handled by add-on safety devices.
  - Do: Apply the four principles when choosing operations: intensify (less hazardous inventory), substitute (a safer material), attenuate (milder conditions), simplify.
  - Why: A hazard that is not there cannot be released; [Park et al. 2022](https://doi.org/10.3303/CET2290078) call safety devices much less reliable.
  - Check: For each hazardous stream, write down which principle was tried.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Park et al. 2022, *Progress in Inherently Safer Design for Chemical…* (https://doi.org/10.3303/CET2290078), Section 1, p. 463. <!-- park-2022-inherently-safer-design.four-principles-before-devices -->

- **Safety index scores are indicative only**
  - When: You present a safety index ranking.
  - Do: Report index rankings as indicative.
  - Why: Indicators and their weights are expert choices, not fitted to incidents: an analysis of 94 CSB (US Chemical Safety Board) incident reports found too much missing data to fix them.
  - Check: State the weights used next to the ranking.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Park et al. 2022, *Progress in Inherently Safer Design for Chemical…* (https://doi.org/10.3303/CET2290078), Section 2.2.1, p. 464; Section 4, p. 468. <!-- park-2022-inherently-safer-design.indicators-not-yet-validated -->

- **Mixture flammability: treat estimates with caution**
  - When: You estimate the hazard of a process stream that is a mixture.
  - Do: Flag mixture estimates as uncertain.
  - Why: Mixture flammability does not follow the pure components proportionally, and few data exist to check it.
  - Check: Look for measured data on the actual mixture before relying on an estimate.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Park et al. 2022, *Progress in Inherently Safer Design for Chemical…* (https://doi.org/10.3303/CET2290078), Section 3.2, p. 467. <!-- park-2022-inherently-safer-design.mixture-flammability-caution -->

- **Rank alternatives early with a safety index built from chemical and process indicators**
  - When: You compare routes, units or streams on safety with little data.
  - Do: Build an index from chemical indicators (flammability, explosiveness, toxicity) and process indicators (pressure, temperature), all known from a simple flowsheet. [Park et al. 2022](https://doi.org/10.3303/CET2290078) count 22 hazard-based, 33 risk-based and 18 cost-based tools.
  - Why: These indicators are available at the concept stage.
  - Check: Report the ranking as indicative: the indicators' weights are not yet verified against incident data.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Park et al. 2022, *Progress in Inherently Safer Design for Chemical…* (https://doi.org/10.3303/CET2290078), Section 2.1, p. 464. <!-- park-2022-inherently-safer-design.rank-alternatives-with-indicators -->

- **Consider inherent safety from the first flowsheet**
  - When: You are in conceptual design, before the route and configuration are fixed.
  - Do: Screen the routes for inherent safety now.
  - Why: Once technology and configuration are fixed, changes are costly; [Park et al. 2022](https://doi.org/10.3303/CET2290078) hold inherently safer design to be the most cost-effective risk reduction.
  - Check: Record a safety ranking next to the cost ranking of the routes.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Park et al. 2022, *Progress in Inherently Safer Design for Chemical…* (https://doi.org/10.3303/CET2290078), Abstract and Section 1, p. 463. <!-- park-2022-inherently-safer-design.safety-from-first-flowsheet -->

- **Judge safety together with cost, sustainability and resilience**
  - When: A safety index alone is used to choose a route.
  - Do: Combine safety with life-cycle cost, sustainability and resilience, for example in one return-on-investment metric.
  - Why: Design trade-offs are made under several constraints at once.
  - Check: Show how the route ranking changes when safety is included.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Park et al. 2022, *Progress in Inherently Safer Design for Chemical…* (https://doi.org/10.3303/CET2290078), Section 2.3, p. 466; Section 3.1, p. 467. <!-- park-2022-inherently-safer-design.safety-with-cost-and-life-cycle -->
