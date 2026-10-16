module

public import Mathlib.Computability.TuringMachine.Computable
public import Mathlib.Analysis.Real.Sqrt

@[expose] public section

namespace PlaneAugmentation

def encodeNat (n : Nat) : List Bool :=
  let bits := (Nat.toDigits 2 n).map (fun c => c == '1')
  List.replicate bits.length true ++ [false] ++ bits

def encodeList {α : Type} (encode : α → List Bool) (xs : List α) : List Bool :=
  encodeNat xs.length ++ xs.flatMap encode

def encodeInt (z : Int) : List Bool := [decide (z < 0)] ++ encodeNat z.natAbs
def encodeRat (q : Rat) : List Bool := encodeInt q.num ++ encodeNat q.den

structure Graph where
  n : Nat
  edges : List (Nat × Nat)
  deriving Repr

def loopless (g : Graph) : Bool :=
  g.edges.all (fun e => e.1 < g.n && e.2 < g.n && e.1 != e.2)

def simple (g : Graph) : Bool := loopless g &&
  decide ((g.edges.map (fun e => (min e.1 e.2, max e.1 e.2))).Nodup)

def adjacent (g : Graph) (u v : Nat) : Bool :=
  g.edges.any (fun e => (e.1 == u && e.2 == v) || (e.1 == v && e.2 == u))

def encodeGraph (g : Graph) : List Bool :=
  encodeList encodeNat (List.range g.n) ++
  encodeList (fun e => encodeNat e.1 ++ encodeNat e.2) g.edges

abbrev Point := Rat × Rat

def cross (a b c : Point) : Rat :=
  (b.1-a.1)*(c.2-a.2) - (b.2-a.2)*(c.1-a.1)

def onSegment (p a b : Point) : Prop :=
  cross a b p = 0 ∧ min a.1 b.1 ≤ p.1 ∧ p.1 ≤ max a.1 b.1 ∧
  min a.2 b.2 ≤ p.2 ∧ p.2 ≤ max a.2 b.2

def intersectsSegment (a b c d : Point) : Prop :=
  max (min a.1 b.1) (min c.1 d.1) ≤ min (max a.1 b.1) (max c.1 d.1) ∧
  max (min a.2 b.2) (min c.2 d.2) ≤ min (max a.2 b.2) (max c.2 d.2) ∧
  cross a b c * cross a b d ≤ 0 ∧ cross c d a * cross c d b ≤ 0

/-- Intersection is permitted only at a common endpoint; overlaps are forbidden. -/
def segmentsCompatible (a b c d : Point) : Prop :=
  ¬ intersectsSegment a b c d ∨
  ((a = c ∨ a = d ∨ b = c ∨ b = d) ∧
   ¬ ((a = c ∧ b = d) ∨ (a = d ∧ b = c)) ∧
   ¬ (onSegment a c d ∧ a ≠ c ∧ a ≠ d) ∧
   ¬ (onSegment b c d ∧ b ≠ c ∧ b ≠ d) ∧
   ¬ (onSegment c a b ∧ c ≠ a ∧ c ≠ b) ∧
   ¬ (onSegment d a b ∧ d ≠ a ∧ d ≠ b))

instance (p a b : Point) : Decidable (onSegment p a b) := by
  unfold onSegment; infer_instance
instance (a b c d : Point) : Decidable (intersectsSegment a b c d) := by
  unfold intersectsSegment; infer_instance
instance (a b c d : Point) : Decidable (segmentsCompatible a b c d) := by
  unfold segmentsCompatible; infer_instance

def pointAt (points : List Point) (i : Nat) : Point := points[i]?.getD (0,0)

def planeDrawing (g : Graph) (points : List Point) : Bool :=
  points.length == g.n && decide points.Nodup &&
  g.edges.all (fun e => (List.range g.n).all (fun v =>
    decide (v = e.1 ∨ v = e.2 ∨ ¬ onSegment (pointAt points v)
      (pointAt points e.1) (pointAt points e.2)))) &&
  (g.edges.zipIdx).all (fun (e,i) => (g.edges.zipIdx).all (fun (f,j) =>
    i == j || decide (segmentsCompatible (pointAt points e.1) (pointAt points e.2)
      (pointAt points f.1) (pointAt points f.2))))

def encodePoint (p : Point) : List Bool := encodeRat p.1 ++ encodeRat p.2

def arcSegments (points : List Point) : List (Point × Point) :=
  points.zip (points.drop 1)

def simpleArc (points : List Point) : Bool :=
  points.length ≥ 2 && decide points.Nodup &&
  (arcSegments points).zipIdx.all (fun (e,i) =>
    (arcSegments points).zipIdx.all (fun (f,j) =>
      i == j || decide (segmentsCompatible e.1 e.2 f.1 f.2)))

structure EmbeddedGraph where
  graph : Graph
  points : List Point
  arcs : List (List Point)
  deriving Repr

/-- Rational polygonal arcs represent a topological plane embedding, not straight edges. -/
def legalEmbedding (x : EmbeddedGraph) : Bool :=
  loopless x.graph && x.points.length == x.graph.n && decide x.points.Nodup &&
  x.arcs.length == x.graph.edges.length &&
  (x.graph.edges.zip x.arcs).all (fun (e,path) =>
    simpleArc path && path.head? == some (pointAt x.points e.1) &&
    path.getLast? == some (pointAt x.points e.2) &&
    (List.range x.graph.n).all (fun v => v == e.1 || v == e.2 ||
      (arcSegments path).all (fun s => !decide (onSegment (pointAt x.points v) s.1 s.2)))) &&
  x.arcs.zipIdx.all (fun (a,i) => x.arcs.zipIdx.all (fun (b,j) => i == j ||
    (arcSegments a).all (fun e => (arcSegments b).all (fun f =>
      decide (segmentsCompatible e.1 e.2 f.1 f.2) &&
      [e.1,e.2].all (fun p => !decide (onSegment p f.1 f.2) ||
        ((a.head? == some p || a.getLast? == some p) &&
         (b.head? == some p || b.getLast? == some p)))))))

def degree (g : Graph) (v : Nat) : Nat :=
  (g.edges.filter (fun e => e.1 == v || e.2 == v)).length

def reachAvoiding (g : Graph) (removed : List Nat) : Nat → List Nat → List Nat
  | 0, seen => seen
  | fuel+1, seen => reachAvoiding g removed fuel ((List.range g.n).filter (fun v =>
      !removed.contains v && (seen.contains v || seen.any (fun u => adjacent g u v))))

def connectedAfter (g : Graph) (removed : List Nat) : Bool :=
  let remaining := (List.range g.n).filter (fun v => !removed.contains v)
  match remaining.head? with
  | none => false
  | some root => reachAvoiding g removed g.n [root] == remaining

def threeConnected (g : Graph) : Bool :=
  g.n ≥ 4 && connectedAfter g [] &&
  (List.range g.n).all (fun u => connectedAfter g [u] &&
    (List.range g.n).all (fun v => connectedAfter g [u,v]))

def cubic (g : Graph) : Bool := (List.range g.n).all (fun v => degree g v == 3)

def extendsEmbedding (small large : EmbeddedGraph) : Bool :=
  small.graph.n ≤ large.graph.n &&
  large.points.take small.graph.n == small.points &&
  large.graph.edges.take small.graph.edges.length == small.graph.edges &&
  large.arcs.take small.arcs.length == small.arcs

def augmentation (x y : EmbeddedGraph) : Bool :=
  legalEmbedding y && extendsEmbedding x y && cubic y.graph && threeConnected y.graph

def encodeEmbedding (x : EmbeddedGraph) : List Bool :=
  encodeGraph x.graph ++ encodeList encodePoint x.points ++
  encodeList (encodeList encodePoint) x.arcs

abbrev Source := EmbeddedGraph
abbrev Instance := EmbeddedGraph
def legalSource (x : Source) : Bool := legalEmbedding x &&
  (List.range x.graph.n).all (fun v => degree x.graph v ≤ 3)
def legalTarget := legalSource
def sourceYes (x : Source) : Prop := ∃ y, augmentation x y = true ∧ y.graph.n = x.graph.n
def targetYes (x : Instance) : Prop := ∃ y, augmentation x y = true
def encodeSource := encodeEmbedding
def encodeTarget := encodeEmbedding

/-- Standard decision reduction. Boolean-answer recovery is the identity. -/
def Reduction (forward : Source → Instance) : Prop :=
  Nonempty (Turing.TM2ComputableInPolyTime encodeSource encodeTarget forward) ∧
  (∃ bound : Polynomial Nat, ∀ x,
    (encodeTarget (forward x)).length ≤ bound.eval (encodeSource x).length) ∧
  (∀ x, legalSource x = true → legalTarget (forward x) = true) ∧
  (∀ x, legalSource x = true → (sourceYes x ↔ targetYes (forward x)))

def Goal : Prop := ∃ forward, Reduction forward

/-- The open reduction is deliberately unproved. -/
theorem solve : Goal := by
  sorry

end PlaneAugmentation
