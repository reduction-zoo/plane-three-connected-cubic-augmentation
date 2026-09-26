# Partial contract

The current source corpus uses connected plane graphs `{"vertices":n,"edges":[[u,v],...],"rotations":[[neighbors_in_cyclic_order],...]}`. Every edge has `u<v`; the rotation system must be planar. A positive source output `{"edges":augmented_edges,"rotations":augmented_rotations}` adds only edges on the same vertex set, preserves each original vertex's cyclic neighbor order, and is a planar three-connected cubic graph. `NO-SOLUTION` is valid exactly if no such edge-only augmentation exists within this connected finite model.

The target permits new vertices and edges while preserving the fixed input embedding. A finite combinatorial witness encoding for new vertices, a conclusive bound or other NO oracle, and a candidate recovery gate remain to be fixed. `check.py --candidate` exits with the blocker.
