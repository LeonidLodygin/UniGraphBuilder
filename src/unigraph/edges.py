from collections import defaultdict


class Edge:
    def __init__(self, src: int, dst: int, rel: str) -> None:
        self.src = src
        self.dst = dst
        self.rel = rel

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Edge):
            return NotImplemented
        return self.src == other.src and self.dst == other.dst and self.rel == other.rel

    def __repr__(self) -> str:
        return f"Edge(src={self.src}, dst={self.dst}, rel={self.rel!r})"


class EdgeStore:
    def __init__(self) -> None:
        self.edges: list[Edge] = []
        self.stats: dict[str, int] = defaultdict(int)

    def add(self, src: int, dst: int, rel: str) -> None:
        self.edges.append(Edge(src, dst, rel))
        self.stats[rel] += 1
