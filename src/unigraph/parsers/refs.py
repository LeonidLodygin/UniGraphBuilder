import re

from unigraph.edges import EdgeStore
from unigraph.idmap import IDMap

# Regular expressions for parsing UniProt cross-references.
# Based on the official UniProt .dat format documentation:
# https://ftp.uniprot.org/pub/databases/uniprot/knowledgebase/complete/docs/userman.htm
#
# Example line:
# DR   KEGG; hsa:10458; -.
REF_PARSERS = [
    (r"DR\s+KEGG;\s+([^;]+);", "kegg", "belongs_to", "belongs_to_r"),
    (r"DR\s+STRING;\s+([^;]+);", "string", "interacts_with", "interacts_with"),
    (r"DR\s+GO;\s+(GO:\d+);", "go", "participate_in", "participate_in_r"),
    (r"DR\s+InterPro;\s+(IPR\d+);", "interpro", "has", "has_r"),
    (r"PubMed=(\d+)", "pubmed", "refers_to", "refers_to_r"),
    (r"DR\s+GeneID;\s+(\d+);", "gene", "codes_for_r", "codes_for"),
    (r"DR\s+HOGENOM;\s+([^;]+);", "hogenom", "Is_homologous_to", "Is_homologous_to_r"),
]


def parse_refs(
    block: str,
    protein_key: str,
    idmap: IDMap,
    edges: EdgeStore,
) -> None:
    for pattern, prefix, rel_fwd, rel_rev in REF_PARSERS:
        for value in re.findall(pattern, block):
            key = f"{prefix}:{value}"
            src = idmap.get(protein_key)
            dst = idmap.get(key)
            edges.add(src, dst, rel_fwd)
            edges.add(dst, src, rel_rev)
