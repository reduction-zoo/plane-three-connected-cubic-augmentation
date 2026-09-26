"""Partial exact edge-only plane cubic augmentation oracle."""

import argparse
import json
import subprocess
import sys
from itertools import combinations,product
from pathlib import Path


def connected(n,edges,deleted=()):
    remaining = set(range(n))-set(deleted)
    if not remaining:
        return True
    adjacent = [set() for _ in range(n)]
    for u,v in edges:
        adjacent[u].add(v)
        adjacent[v].add(u)
    seen,frontier = {min(remaining)},[min(remaining)]
    while frontier:
        for v in adjacent[frontier.pop()] & remaining:
            if v not in seen:
                seen.add(v)
                frontier.append(v)
    return seen == remaining


def plane_rotation(n,edges,rotations):
    if (type(n) is not int or n < 1 or not isinstance(edges,list)
            or not isinstance(rotations,list) or len(rotations) != n
            or any(not isinstance(edge,list) or len(edge) != 2
                   or any(type(v) is not int or not 0 <= v < n for v in edge)
                   or edge[0] >= edge[1] for edge in edges)
            or len({tuple(edge) for edge in edges}) != len(edges)):
        return False
    adjacent = [set() for _ in range(n)]
    for u,v in edges:
        adjacent[u].add(v)
        adjacent[v].add(u)
    if any(not isinstance(rotations[v],list)
           or len(rotations[v]) != len(adjacent[v])
           or any(type(w) is not int for w in rotations[v])
           or set(rotations[v]) != adjacent[v] for v in range(n)):
        return False
    if not connected(n,edges):
        return False
    if not edges:
        return n == 1
    unseen = {(u,v) for a,b in edges for u,v in ((a,b),(b,a))}
    faces = 0
    while unseen:
        start = next(iter(unseen))
        dart = start
        while dart in unseen:
            unseen.remove(dart)
            u,v = dart
            order = rotations[v]
            dart = (v,order[(order.index(u)-1)%len(order)])
        if dart != start:
            return False
        faces += 1
    return n-len(edges)+faces == 2


def legal_source(source):
    return (isinstance(source,dict) and set(source) == {"vertices","edges","rotations"}
            and plane_rotation(source["vertices"],source["edges"],source["rotations"]))


def cyclic_equal(first,second):
    if len(first) != len(second):
        return False
    return any(first == second[i:]+second[:i] for i in range(len(second))) if first else True


def three_connected(n,edges):
    if n < 4:
        return False
    return all(connected(n,edges,removed)
               for count in range(3) for removed in combinations(range(n),count))


def direct_augmentation(source,output):
    if not isinstance(output,dict) or set(output) != {"edges","rotations"}:
        return False
    n,edges,rotations = source["vertices"],output["edges"],output["rotations"]
    if not plane_rotation(n,edges,rotations):
        return False
    original = {tuple(edge) for edge in source["edges"]}
    if not original <= {tuple(edge) for edge in edges}:
        return False
    if any(len(order) != 3 for order in rotations) or not three_connected(n,edges):
        return False
    for v in range(n):
        restricted = [w for w in rotations[v] if w in source["rotations"][v]]
        if not cyclic_equal(restricted,source["rotations"][v]):
            return False
    return True


def completions(n,original):
    adjacency = [set() for _ in range(n)]
    for u,v in original:
        adjacency[u].add(v)
        adjacency[v].add(u)
    if n < 4 or n % 2 or any(len(row) > 3 for row in adjacency):
        return

    def extend(edges):
        candidates = [v for v in range(n) if len(adjacency[v]) < 3]
        if not candidates:
            yield sorted([list(edge) for edge in edges])
            return
        u = candidates[0]
        for v in candidates[1:]:
            if v not in adjacency[u]:
                adjacency[u].add(v)
                adjacency[v].add(u)
                edge = (min(u,v),max(u,v))
                yield from extend(edges|{edge})
                adjacency[u].remove(v)
                adjacency[v].remove(u)

    yield from extend(set(original))


def source_solutions(source,limit=3):
    if not legal_source(source):
        raise ValueError("Illegal connected plane graph")
    n = source["vertices"]
    outputs = []
    for edges in completions(n,{tuple(edge) for edge in source["edges"]}):
        if not three_connected(n,edges):
            continue
        adjacent = [set() for _ in range(n)]
        for u,v in edges:
            adjacent[u].add(v)
            adjacent[v].add(u)
        choices = []
        for v in range(n):
            a,b,c = sorted(adjacent[v])
            choices.append(([a,b,c],[a,c,b]))
        for rotations in product(*choices):
            output = {"edges":edges,"rotations":[list(order) for order in rotations]}
            if direct_augmentation(source,output):
                outputs.append(output)
                if len(outputs) >= limit:
                    return outputs
    return outputs or [{"status":"NO-SOLUTION"}]


def solve_source(source):
    return source_solutions(source,1)[0]


def valid_source(source,output):
    if not legal_source(source) or not isinstance(output,dict):
        return False
    if output == {"status":"NO-SOLUTION"}:
        return solve_source(source) == output
    return direct_augmentation(source,output)


def self_test():
    from generate_cases import EDGE_CASES,random_source
    from test_oracle import test_hand_cases
    path = Path(__file__).with_name("cases.json")
    root = Path(__file__).resolve().parents[3]
    subprocess.run([sys.executable,str(root/"research/validate_preparation.py"),str(path)],check=True,cwd=root)
    cases = json.loads(path.read_text())
    for source,expected in EDGE_CASES:
        assert ("edges" in solve_source(source)) == expected
    for case in cases:
        source = case["source"]
        if case["kind"] == "random":
            assert random_source(case["seed"]) == source
        answer = solve_source(source)
        assert ("edges" in answer) == ("edges" in case["expected"])
        assert valid_source(source,answer) and valid_source(source,case["expected"])
    test_hand_cases()
    print(f"Partial Prepare: {len(cases)} plane-graph source cases checked; added-vertex target oracle pending")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--self-test",action="store_true")
    group.add_argument("--candidate",type=Path)
    args = parser.parse_args()
    if args.self_test:
        self_test()
    else:
        raise SystemExit("Prepare blocked: added-vertex plane cubic augmentation needs a conclusive target oracle")
