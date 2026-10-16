import Challenge
open PlaneAugmentation

example : legalEmbedding ⟨⟨4, [(0,1),(2,3)]⟩,
    [(0,0),(1,0),(0,2),(1,2)], [[(0,0),(1,0)],[(0,2),(1,2)]]⟩ = true := by
  native_decide

example : legalEmbedding ⟨⟨4, [(0,1),(2,3)]⟩,
    [(0,0),(2,2),(0,2),(2,0)], [[(0,0),(2,2)],[(0,2),(2,0)]]⟩ = false := by
  native_decide

example : simpleArc [(0,0),(1,0),(1,1),(2,1)] = true := by native_decide
example : simpleArc [(0,0),(2,2),(0,2),(2,0)] = false := by native_decide

example : threeConnected ⟨4,[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]⟩ = true := by
  native_decide
example : threeConnected ⟨4,[(0,1),(1,2),(2,3),(0,3)]⟩ = false := by
  native_decide

def tetrahedron : EmbeddedGraph :=
  ⟨⟨4,[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]⟩,
   [(0,0),(4,0),(0,4),(1,1)],
   [[(0,0),(4,0)],[(0,0),(0,4)],[(0,0),(1,1)],
    [(4,0),(0,4)],[(4,0),(1,1)],[(0,4),(1,1)]]⟩

example : legalSource tetrahedron = true := by native_decide
example : sourceYes tetrahedron ∧ targetYes tetrahedron := by
  constructor
  · exact ⟨tetrahedron, by native_decide, rfl⟩
  · exact ⟨tetrahedron, by native_decide⟩
