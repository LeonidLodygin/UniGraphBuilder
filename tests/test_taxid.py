from unigraph.edges import EdgeStore
from unigraph.idmap import IDMap
from unigraph.parsers.entry import parse_entry

BLOCK_WITH_TAXID = """
AC   P12345;
OX   NCBI_TaxID=9606;
//
"""


def test_parse_entry_taxid_filter_accept():
    idmap = IDMap()
    edges = EdgeStore()
    filter_set = {"9606"}
    parse_entry(BLOCK_WITH_TAXID, idmap, edges, filter_set)
    assert "protein:P12345" in idmap._map


def test_parse_entry_taxid_filter_reject():
    idmap = IDMap()
    edges = EdgeStore()
    filter_set = {"1000"}
    parse_entry(BLOCK_WITH_TAXID, idmap, edges, filter_set)
    assert len(idmap._map) == 0
