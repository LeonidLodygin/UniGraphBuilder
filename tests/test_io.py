from pathlib import Path

from unigraph.edges import EdgeStore
from unigraph.idmap import IDMap
from unigraph.io.writer import write_graph, write_nodes, write_stats


def test_writer_functions(tmp_path: Path):
    idmap = IDMap()
    edges = EdgeStore()

    s = idmap.get("protein:P1")
    d = idmap.get("kegg:hsa00010")
    edges.add(s, d, "belongs_to")

    graph_path = tmp_path / "graph.g"
    nodes_path = tmp_path / "nodes.tsv"
    stats_path = tmp_path / "stats.txt"

    write_graph(graph_path, edges)
    write_nodes(nodes_path, idmap)
    write_stats(stats_path, idmap, edges)

    assert graph_path.exists()
    assert nodes_path.exists()
    assert stats_path.exists()

    graph_content = graph_path.read_text()
    assert f"{s} {d} belongs_to" in graph_content


def test_write_graph(tmp_path):
    edges = EdgeStore()
    edges.add(1, 2, "rel1")
    edges.add(2, 3, "rel2")

    graph_file = tmp_path / "graph.g"
    write_graph(graph_file, edges)
    content = graph_file.read_text().strip().split("\n")

    assert content == ["1 2 rel1", "2 3 rel2"]


def test_write_nodes(tmp_path):
    idmap = IDMap()
    idmap.get("a")
    idmap.get("b")

    nodes_file = tmp_path / "nodes.tsv"
    write_nodes(nodes_file, idmap)
    content = nodes_file.read_text().strip().split("\n")

    expected = [
        f"{idx}\t{key}" for key, idx in sorted(idmap._map.items(), key=lambda x: x[1])
    ]
    assert content == expected


def test_write_stats(tmp_path):
    idmap = IDMap()
    idmap.get("a")
    idmap.get("b")
    edges = EdgeStore()
    edges.add(0, 1, "rel1")
    edges.add(1, 0, "rel1")
    edges.add(1, 0, "rel2")

    stats_file = tmp_path / "stats.txt"
    write_stats(stats_file, idmap, edges)
    content = stats_file.read_text()

    assert "total_nodes: 2" in content
    assert "total_edges: 3" in content
    assert "rel1: 2" in content
    assert "rel2: 1" in content
