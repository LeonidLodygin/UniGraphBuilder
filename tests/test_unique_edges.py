from unigraph.parsers.entry import parse_entry
from unigraph.idmap import IDMap
from unigraph.edges import EdgeStore

SAMPLE_BLOCK = """
AC   P12345;
OX   NCBI_TaxID=9606;
DR   KEGG; hsa00010;
DR   STRING; 12345;
DR   GO; GO:0008150;
DR   InterPro; IPR000001;
PubMed=1234567;
DR   GeneID; 1234;
DR   HOGENOM; HOG00001;
//
"""

def test_number_of_unique_nodes_after_parse():
    idmap = IDMap()
    edges = EdgeStore()
    organism_filter = set()

    parse_entry(SAMPLE_BLOCK, idmap, edges, organism_filter)

    expected_keys = {
        "protein:P12345",
        "kegg:hsa00010",
        "string:12345",
        "go:GO:0008150",
        "interpro:IPR000001",
        "pubmed:1234567",
        "gene:1234",
        "hogenom:HOG00001",
    }

    for key in expected_keys:
        assert key in idmap._map

    assert len(idmap._map) == len(expected_keys)