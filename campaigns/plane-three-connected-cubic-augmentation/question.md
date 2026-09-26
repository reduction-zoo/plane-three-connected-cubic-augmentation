# Edge-only plane cubic augmentation → Plane cubic augmentation allowing new vertices

Category: Complexity open

## Source

The source gives a fixed plane graph. Its outputs are three-connected cubic augmentations adding only edges while extending the embedding, or NO-SOLUTION.

## Target

The target is a fixed plane graph and asks for a three-connected cubic supergraph extending its embedding, allowing additional vertices and edges. The source version permits only additional edges. Valid augmentations require a finite combinatorial embedding encoding.

## Required result

Construct deterministic polynomial-time maps F and G: F sends every legal source instance to a legal target instance, and G(x,y) is a valid source output for every valid output y of F(x). Preserve the stated threshold, domain and promises. The requested complexity conclusion is NP-hardness for the stated target problem.

## Acceptance

Give explicit construction and recovery algorithms, a general proof for every legal input and every valid target output, and polynomial runtime and encoding-size bounds. Specify finite output encodings and handle NO-SOLUTION outputs when applicable. Tests compare recovered source outputs with independent source solutions.

## Why it matters

Allowing new vertices changes the feasible extensions and is not automatically covered by edge-only augmentation hardness.

## Difficulty

Every added-vertex augmentation must decode to an edge-only source solution; prior attempts have not controlled these extra freedoms.

## Literature context

Known edge-only augmentation results do not automatically extend to a target that may insert vertices in the fixed embedding.

Literature checked 2026-09-15. This summarizes the archived literature search on the date above. Unpublished, unindexed and overlooked work remains outside coverage; no new novelty assessment was performed.

## References

- [Recognition Complexity of Subgraphs of k-Connected Planar Cubic Graphs](https://publikationen.bibliothek.kit.edu/1000188407/170710540): - R4: Recognition Complexity of Subgraphs of k-Connected Planar Cubic Graphs, Algorithmica 88:11 (2026), Previous Results, Section 6 and Question 7.1. Earlier edge-only source: Hartmann, Rollin, Rutter, Regular Augmentation of Planar Graphs, Algorithmica (2015); the exact source theorem is stated in R4.
- [Regular Augmentation of Planar Graphs](https://www.fernuni-hagen.de/ti/forschung/publikationen/HRR15.shtml): - R4: Recognition Complexity of Subgraphs of k-Connected Planar Cubic Graphs, Algorithmica 88:11 (2026), Previous Results, Section 6 and Question 7.1. Earlier edge-only source: Hartmann, Rollin, Rutter, Regular Augmentation of Planar Graphs, Algorithmica (2015); the exact source theorem is stated in R4.

Fixed from board record `website/questions/plane-three-connected-cubic-augmentation.json` in board checkout at 6c7d3bd9c0a8f595279969a9c0a4d1853a3f5c17; the record was copied from the current working tree.
