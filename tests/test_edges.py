from unigraph.edges import EdgeStore, Edge

def test_edges_add_and_stats():
    edges = EdgeStore()
    edges.add(1, 2, "rel1")
    edges.add(2, 3, "rel2")
    assert len(edges.edges) == 2
    assert edges.stats["rel1"] == 1
    assert edges.stats["rel2"] == 1
    assert edges.edges[0] == Edge(1, 2, "rel1")

def test_edgestore_stats_count():
    edges = EdgeStore()
    edges.add(1, 2, "rel1")
    edges.add(2, 3, "rel2")
    edges.add(3, 4, "rel1")
    assert edges.stats["rel1"] == 2
    assert edges.stats["rel2"] == 1
    assert len(edges.edges) == 3    