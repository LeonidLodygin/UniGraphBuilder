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

def test_parse_entry_basic():
    idmap = IDMap()
    edges = EdgeStore()
    organism_filter = set()

    parse_entry(SAMPLE_BLOCK, idmap, edges, organism_filter)

    pid = idmap.get("protein:P12345")
    assert pid is not None
    assert len(edges.edges) > 0
    assert len(edges.stats) > 0
    
def test_parse_entry_empty_block():
    idmap = IDMap()
    edges = EdgeStore()
    filter_set = set()
    parse_entry("", idmap, edges, filter_set)
    assert len(idmap._map) == 0
    assert len(edges.edges) == 0   

def test_parse_entry_taxid_filter():
    idmap = IDMap()
    edges = EdgeStore()
    block = """
    AC   P12345;
    OX   NCBI_TaxID=9999;
    """
    parse_entry(block, idmap, edges, {"9606"})
    assert len(idmap._map) == 0
    assert len(edges.edges) == 0

def test_parse_entry_full_block():
    idmap = IDMap()
    edges = EdgeStore()
    block = """
    AC   P12345;
    OX   NCBI_TaxID=9606;
    DR   KEGG; hsa00010;
    DR   STRING; 12345;
    DR   GO; GO:0008150;
    DR   InterPro; IPR000001;
    PubMed=12345678;
    DR   GeneID; 6789;
    DR   HOGENOM; HOG000001;
    """
    parse_entry(block, idmap, edges, set())

    protein_key = "protein:P12345"
    assert protein_key in idmap._map

    rels = [e.rel for e in edges.edges]
    for rel in ["belongs_to", "belongs_to_r", "interacts_with", "participate_in", "participate_in_r", "has", "has_r", "refers_to", "refers_to_r", "codes_for", "codes_for_r", "Is_homologous_to", "Is_homologous_to_r"]:
        assert rel in rels    
        
def test_read_dat_blocks(tmp_path):
    from unigraph.io.reader import read_dat_blocks

    content = """AC   P1;
OX   NCBI_TaxID=1;
//
AC   P2;
OX   NCBI_TaxID=2;
//
"""

    file_path = tmp_path / "test.dat"
    file_path.write_text(content)

    blocks = list(read_dat_blocks(file_path))
    assert len(blocks) == 2
    assert blocks[0].startswith("AC   P1;")
    assert blocks[1].startswith("AC   P2;")    

def test_parse_refs_add_edges():
    from unigraph.parsers.refs import parse_refs

    idmap = IDMap()
    edges = EdgeStore()

    block = """
    DR   KEGG; hsa00010;
    DR   STRING; 12345;
    DR   GO; GO:0008150;
    DR   InterPro; IPR000001;
    PubMed=12345678;
    DR   GeneID; 6789;
    DR   HOGENOM; HOG000001;
    """

    protein_key = "protein:P00001"
    idmap.get(protein_key)

    parse_refs(block, protein_key, idmap, edges)

    assert any(e.rel == "belongs_to" for e in edges.edges)
    assert any(e.rel == "interacts_with" for e in edges.edges)
    assert any(e.rel == "participate_in" for e in edges.edges)
    assert any(e.rel == "has" for e in edges.edges)
    assert any(e.rel == "refers_to" for e in edges.edges)
    assert any(e.rel == "codes_for" for e in edges.edges)
    assert any(e.rel == "Is_homologous_to" for e in edges.edges)    