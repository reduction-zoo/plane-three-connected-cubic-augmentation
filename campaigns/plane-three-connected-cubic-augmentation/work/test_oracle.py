from check import legal_source,solve_source,valid_source


def test_hand_cases():
    complete = {"vertices":4,"edges":[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],
                "rotations":[[1,2,3],[0,3,2],[0,1,3],[0,2,1]]}
    assert legal_source(complete)
    assert valid_source(complete,{"edges":complete["edges"],"rotations":complete["rotations"]})
    odd = {"vertices":3,"edges":[[0,1],[1,2]],"rotations":[[1],[0,2],[1]]}
    assert solve_source(odd) == {"status":"NO-SOLUTION"}
    assert not legal_source({"vertices":2,"edges":[[0,1]],"rotations":[[],[]]})


if __name__ == "__main__":
    test_hand_cases()
