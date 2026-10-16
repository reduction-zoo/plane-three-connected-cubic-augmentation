# Edge-only plane cubic augmentation → Plane cubic augmentation allowing new vertices

Category: Complexity open

## Source

Given a finite loopless subcubic plane graph, with parallel edges permitted and its full topological embedding fixed, output YES exactly when adding edges on the same vertex set can produce a three-vertex-connected cubic plane supergraph extending that embedding, and NO otherwise. The embedding includes disconnected-component nesting, face boundaries and the outer face. A finite rational polygonal drawing represents it; edges may bend.

## Target

Given the same kind of fixed plane input, output YES exactly when some finite three-vertex-connected cubic plane supergraph extends its embedding, allowing both additional vertices and additional edges, and NO otherwise. Three-connectivity requires at least four vertices. The graph is a subgraph, not necessarily induced. All disconnected components and their nesting must be preserved. Rational polygonal edge arcs represent topological embeddings; straight-line geometry is not fixed.

## Required result

Construct a deterministic polynomial-time map F from the edge-only fixed-embedding three-connected cubic augmentation decision problem to its variant allowing new vertices, preserving YES and NO. Boolean-answer recovery G is the identity. The requested conclusion is NP-hardness of the fixed-embedding target.

## Acceptance

Specify the finite input encodings and a deterministic instance construction. Prove legality and YES/NO equivalence for every legal source input, together with polynomial runtime and output bit-length bounds. The source and target return Boolean decisions; recovery returns the same answer. Real or geometric realizations are existential objects, and no witness reconstruction or exhaustive target oracle is required to state the problem. A compiling open Lean challenge is a specification, not a completed reduction proof.

## Why it matters

Allowing new vertices changes the feasible extensions and is not automatically covered by edge-only augmentation hardness.

## Difficulty

Allowing new vertices introduces feasible extensions absent from the edge-only source. A hardness reduction must preserve NO instances despite these additional choices and must retain the complete fixed embedding, including disconnected-component nesting.

## Literature context

Known edge-only augmentation results do not automatically extend to a target that may insert vertices in the fixed embedding.

Literature classification checked: 2026-09-15.

This summarizes the archived literature search on the date above. Unpublished, unindexed and overlooked work remains outside coverage; no new novelty assessment was performed. Definition audit 2026-10-16 reconstructs the mathematical decision definition from primary literature; it does not establish a new hardness result or constitute an exhaustive search for later resolutions. Historical executable preparation contracts do not limit the existential mathematical witnesses in this definition.

## References

- [Recognition Complexity of Subgraphs of k-Connected Planar Cubic Graphs](https://publikationen.bibliothek.kit.edu/1000188407/170710540): - R4: Recognition Complexity of Subgraphs of k-Connected Planar Cubic Graphs, Algorithmica 88:11 (2026), Previous Results, Section 6 and Question 7.1. Earlier edge-only source: Hartmann, Rollin, Rutter, Regular Augmentation of Planar Graphs, Algorithmica (2015); the exact source theorem is stated in R4.
- [Regular Augmentation of Planar Graphs](https://www.fernuni-hagen.de/ti/forschung/publikationen/HRR15.shtml): - R4: Recognition Complexity of Subgraphs of k-Connected Planar Cubic Graphs, Algorithmica 88:11 (2026), Previous Results, Section 6 and Question 7.1. Earlier edge-only source: Hartmann, Rollin, Rutter, Regular Augmentation of Planar Graphs, Algorithmica (2015); the exact source theorem is stated in R4.
