# Executable cases

[ethanol-zsm5-573k](ethanol-zsm5-573k/README.md): first draft benchmark, two kinetic variants at three catalyst loadings, executed through CHEPTA's JSON dispatcher and checked by an independent numerical implementation. Inputs, outputs, provenance and unresolved limitations are retained. Human review is pending; zero accepted training examples.

[benzene-toluene-chemsep-b2](benzene-toluene-chemsep-b2/README.md): CHEPTA's B2 column (The ChemSep Book, as transcribed by CHEPTA) on chepta@0.6.0 through the command line: one converged run within the record's agreement limits, one refused purity specification, one refused literal copy of the record's thermo block. Study record; draft; book not yet checked directly by Lab.

[methanol-separator-flash](methanol-separator-flash/README.md): an illustrative methanol-loop separator flash (state from CHEPTA's decision file, not the paper) with PR + gE (MHV1) and PR with k_ij, and the refused SRK + gE (MHV1); a regression check against CHEPTA's earlier result. Study record; draft.

Add one directory per case. Separate source facts, assumptions and numerical results. Every case needs a pinned engine, reproduction instructions and a review record.
