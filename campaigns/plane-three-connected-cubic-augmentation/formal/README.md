# plane-three-connected-cubic-augmentation: literature-based challenge

This project states the open decision reduction, with an identical unproved
`Solution.lean`. It does not contain a solution or certify any prior candidate.

## Definition and scope

The input is a finite loopless subcubic plane multigraph represented by rational polygonal edge arcs, not a fixed straight-line drawing. This is a concrete representative of the topological embedding; bends are allowed, disconnected components and their actual nesting are retained, and new arcs may have arbitrarily many rational bends. Augmentations retain the old drawing exactly and may add edges between old vertices as well as new vertices. The source forbids new vertices; the target allows them. Both return Boolean decisions. Parallel edges are permitted as in the paper, but no loops or overlapping arcs. Three-connectivity requires at least four vertices. Rational polygonal representatives impose no geometric straight-line restriction on topological plane embeddings. Theorem 6.2 supplies a linear-size certificate construction for the augmentation problem; no bounded oracle is needed to state existence.

The source and target return Boolean decisions. The reduction must be a
deterministic polynomial-time TM2 computation on the self-delimiting binary
encodings in `Challenge.lean`, preserve legality, and preserve both answers.
Recovery of a decision is the identity; no real witness serialization, practical
oracle, or accepted reduction is assumed. Definitions contain no proof holes.
The only proof hole is the open `solve` theorem.

## Sources

- [Recognition Complexity of Subgraphs of k-Connected Planar Cubic Graphs](https://publikationen.bibliothek.kit.edu/1000188407/170710540): Sections 1–2, Theorem 6.2 proof, Question 7.1
- [Regular Augmentation of Planar Graphs](https://arxiv.org/pdf/1209.3865): Fixed-embedding edge-only augmentation definition

## Check

```sh
LEAN_NUM_THREADS=2 lake build
lake env lean Audit.lean
./scripts/verify-comparator.sh
```

The build includes semantic examples in `Tests.lean`. `Audit.lean` checks the
definition's axiom dependencies separately from the unproved theorem. The Linux
workflow checks statement agreement and the expected `sorryAx` rejection with
the bundled comparator. macOS cannot run its required bubblewrap sandbox.
Green setup CI is not evidence that the open reduction has been proved.
