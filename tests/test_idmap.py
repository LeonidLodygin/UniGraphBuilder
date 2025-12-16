from unigraph.idmap import IDMap


def test_idmap_basic_behavior():
    idmap = IDMap()
    a = idmap.get("key1")
    b = idmap.get("key2")
    c = idmap.get("key1")
    assert a == c
    assert a != b
    assert idmap._counter == 2


def test_idmap_many_keys():
    idmap = IDMap()
    keys = [f"key{i}" for i in range(1000)]
    ids = [idmap.get(k) for k in keys]
    assert len(set(ids)) == 1000
    assert idmap._counter == 1000


def test_idmap_get_and_reuse():
    idmap = IDMap()
    id1 = idmap.get("key1")
    id2 = idmap.get("key2")
    id3 = idmap.get("key1")
    assert id1 == id3
    assert id1 != id2
    assert id2 == id1 + 1
