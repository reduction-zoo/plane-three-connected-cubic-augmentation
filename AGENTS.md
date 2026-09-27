# Research instructions

Read the [fixed question](campaigns/plane-three-connected-cubic-augmentation/question.md), [prior state](campaigns/plane-three-connected-cubic-augmentation/state.md) and [preparation notes](campaigns/plane-three-connected-cubic-augmentation/work/preparation.md). The fixed [test corpus](campaigns/plane-three-connected-cubic-augmentation/work/cases.json) and [verifier](campaigns/plane-three-connected-cubic-augmentation/work/check.py) are the starting evidence; the preparation notes state their coverage and any pending checks.

Run `uv sync --locked`, then `uv run --locked python campaigns/plane-three-connected-cubic-augmentation/work/check.py --self-test` before relying on that evidence. Follow the current user's AutoResearch pipeline. Scope and budgets in the state describe earlier work and do not limit a new campaign. Preserve prior evidence, commit new work incrementally and make only evidence-backed claims.
