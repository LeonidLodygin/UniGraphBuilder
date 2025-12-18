from pathlib import Path

from unigraph.edges import EdgeStore
from unigraph.idmap import IDMap


def write_graph(path: Path, edges: EdgeStore) -> None:
    with path.open("w") as f:
        for e in edges.edges:
            f.write(f"{e.src} {e.dst} {e.rel}\n")


def write_nodes(path: Path, idmap: IDMap) -> None:
    with path.open("w") as f:
        for key, idx in sorted(idmap.items(), key=lambda x: x[1]):
            f.write(f"{idx}\t{key}\n")


def write_stats(path: Path, idmap: IDMap, edges: EdgeStore) -> None:
    with path.open("w") as f:
        f.write(f"total_nodes: {idmap._counter}\n")
        f.write(f"total_edges: {len(edges.edges)}\n\n")
        f.write("edge_type_counts:\n")
        for rel, count in sorted(edges.stats.items()):
            f.write(f"  {rel}: {count}\n")
