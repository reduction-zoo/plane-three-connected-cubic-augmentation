# Edge-only plane cubic augmentation → Plane cubic augmentation allowing new vertices

Independent campaign for the [fixed question](campaigns/plane-three-connected-cubic-augmentation/question.md). [State](campaigns/plane-three-connected-cubic-augmentation/state.md) records progress. [Partial Prepare evidence](campaigns/plane-three-connected-cubic-augmentation/work/preparation.md) includes a fixed 112-graph source corpus and exact small-graph edge-only checks.

Prepare is blocked on a conclusive added-vertex target oracle. No reduction or solution is claimed. Reproduce the source checks with `uv sync --locked` and `uv run --locked python campaigns/plane-three-connected-cubic-augmentation/work/check.py --self-test`.

## Literature-based formal definition

The current [decision challenge](campaigns/plane-three-connected-cubic-augmentation/formal/README.md) defines the
problem from primary literature and pins Lean/Mathlib 4.35.0. Its semantic examples
and local axiom audit pass. The reduction theorem is open; Linux comparator
checking remains pending. Earlier executable preparation is retained as historical
evidence and does not restrict the mathematical definition.
