"""Fix small plane graphs before edge-only augmentation research."""

import json
import random
from functools import lru_cache
from itertools import product
from pathlib import Path


def graph(n,edges,rotations):
    return {"vertices":n,"edges":sorted([list(edge) for edge in edges]),
            "rotations":[list(order) for order in rotations]}


@lru_cache(None)
def cube():
    from check import plane_rotation
    n = 8
    edges = [[u,v] for u in range(n) for v in range(u+1,n) if (u^v) in (1,2,4)]
    adjacent = [sorted([v for v in range(n) if (u^v) in (1,2,4)]) for u in range(n)]
    for bits in product((0,1),repeat=n):
        rotations = [[row[0],row[1+bits[u]],row[2-bits[u]]] for u,row in enumerate(adjacent)]
        if plane_rotation(n,edges,rotations):
            return graph(n,edges,rotations)
    raise AssertionError("Cube embedding missing")


@lru_cache(None)
def prism():
    from check import plane_rotation
    n = 6
    edges = [[0,1],[0,2],[1,2],[3,4],[3,5],[4,5],[0,3],[1,4],[2,5]]
    adjacent = [[v for v in range(n) if [min(u,v),max(u,v)] in edges] for u in range(n)]
    for bits in product((0,1),repeat=n):
        rotations = [[row[0],row[1+bits[u]],row[2-bits[u]]] for u,row in enumerate(adjacent)]
        if plane_rotation(n,edges,rotations):
            return graph(n,edges,rotations)
    raise AssertionError("Prism embedding missing")


def subgraph(base,remaining_vertices,retained_edges):
    mapping = {v:i for i,v in enumerate(remaining_vertices)}
    edges = [[mapping[u],mapping[v]] for u,v in retained_edges]
    rotations = [[mapping[w] for w in base["rotations"][v]
                  if w in mapping and [min(v,w),max(v,w)] in retained_edges]
                 for v in remaining_vertices]
    return graph(len(remaining_vertices),edges,rotations)


def random_source(seed):
    from check import connected
    rng = random.Random(seed)
    base = cube()
    vertices = list(range(8))
    if seed % 2:
        vertices.remove(rng.randrange(8))
    edges = [edge for edge in base["edges"] if all(v in vertices for v in edge)]
    rng.shuffle(edges)
    retained = set(map(tuple,edges))
    for edge in edges:
        if rng.randrange(3) == 0:
            trial = retained-{tuple(edge)}
            mapped = [[vertices.index(u),vertices.index(v)] for u,v in trial]
            if connected(len(vertices),mapped):
                retained = trial
    return subgraph(base,vertices,[list(edge) for edge in sorted(retained)])


def k4():
    from check import plane_rotation
    edges = [[u,v] for u in range(4) for v in range(u+1,4)]
    for bits in product((0,1),repeat=4):
        adjacent = [[v for v in range(4) if v != u] for u in range(4)]
        rotations = [[row[0],row[1+bits[u]],row[2-bits[u]]] for u,row in enumerate(adjacent)]
        if plane_rotation(4,edges,rotations):
            return graph(4,edges,rotations)
    raise AssertionError("K4 embedding missing")


base4 = k4()
base6 = prism()
base8 = cube()
EDGE_CASES = [
    (graph(1,[],[[]]),False),
    (graph(2,[[0,1]],[[1],[0]]),False),
    (graph(3,[[0,1],[1,2]],[[1],[0,2],[1]]),False),
    (graph(3,[[0,1],[0,2],[1,2]],[[1,2],[0,2],[0,1]]),False),
    (base4,True),
    (subgraph(base4,list(range(4)),base4["edges"][:-1]),True),
    (subgraph(base4,list(range(4)),base4["edges"][:3]),True),
    (base6,True),
    (subgraph(base6,list(range(6)),base6["edges"][:-1]),True),
    (base8,True),
    (subgraph(base8,list(range(8)),base8["edges"][:-1]),True),
    (subgraph(base8,list(range(7)),[e for e in base8["edges"] if 7 not in e]),False),
]


def build_cases():
    from check import solve_source
    cases,seen = [],set()

    def add(instance,kind,seed=None,expected=None):
        key = json.dumps(instance,sort_keys=True,separators=(",",":"))
        if key in seen:
            return False
        answer = solve_source(instance)
        if expected is not None and ("edges" in answer) != expected:
            raise AssertionError(f"Hand label disagrees with oracle: {instance}")
        seen.add(key)
        case = {"source":instance,"kind":kind,"expected":answer}
        if seed is not None:
            case["seed"] = seed
        cases.append(case)
        return True

    for instance,expected in EDGE_CASES:
        add(instance,"edge",expected=expected)
    seed = 0
    while sum(case["kind"] == "random" for case in cases) < 100:
        add(random_source(seed),"random",seed=seed)
        seed += 1
    return cases


if __name__ == "__main__":
    path = Path(__file__).with_name("cases.json")
    cases = build_cases()
    path.write_text(json.dumps(cases,indent=2)+"\n")
    print(f"Wrote {len(cases)} cases to {path}")
