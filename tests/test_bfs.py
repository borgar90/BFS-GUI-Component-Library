from bfs_component import bfs_traverse


def test_bfs_simple():
    g = {
        "A": ["B", "C"],
        "B": ["D"],
        "C": ["E"],
    }
    assert bfs_traverse(g, "A") == ["A", "B", "C", "D", "E"]
