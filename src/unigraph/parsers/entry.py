import re

from unigraph.edges import EdgeStore
from unigraph.idmap import IDMap
from unigraph.parsers.refs import parse_refs


def parse_entry(
    block: str,
    idmap: IDMap,
    edges: EdgeStore,
    organism_filter: set[str] | None = None,
) -> None:
    m = re.search(r"AC\s+([\w;]+)", block)
    if not m:
        return
    protein = m.group(1).split(";")[0]
    protein_key = f"protein:{protein}"

    m = re.search(r"OX\s+NCBI_TaxID=(\d+)", block)
    if not m:
        return
    taxid = m.group(1)

    if organism_filter and taxid not in organism_filter:
        return

    idmap.get(protein_key)
    parse_refs(block, protein_key, idmap, edges)
