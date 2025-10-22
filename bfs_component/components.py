"""Simple BFS traversal helper"""
from collections import deque
from typing import Dict, List, Set


def bfs_traverse(graph: Dict[object, List[object]], start) -> List[object]:
    """Return nodes in BFS order starting from start.

    graph: adjacency-list mapping
    start: starting node
    """
    visited: Set[object] = set()
    order: List[object] = []
    q = deque([start])
    visited.add(start)
    while q:
        node = q.popleft()
        order.append(node)
        for nb in graph.get(node, []):
            if nb not in visited:
                visited.add(nb)
                q.append(nb)
    return order
