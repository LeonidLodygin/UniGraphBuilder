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
    # Accession numbers in UniProt flat file format are stored in lines
    # starting with "AC". Multiple accessions may be listed on the same line
    # and separated by semicolons, for example:
    #   AC   P12345; Q8N158;
    # This regex extracts the full accession list without the trailing semicolon.
    m = re.search(r"AC\s+([\w;]+)", block)
    if not m:
        return
    protein = m.group(1).split(";")[0]
    protein_key = f"protein:{protein}"

    # Taxonomic identifier of the organism is specified in UniProt flat file
    # in lines starting with "OX". The NCBI taxonomy ID is provided in the form:
    #   OX   NCBI_TaxID=9606;
    # This regex extracts the numeric NCBI Taxonomy ID of the organism.
    m = re.search(r"OX\s+NCBI_TaxID=(\d+)", block)
    if not m:
        return
    taxid = m.group(1)

    if organism_filter and taxid not in organism_filter:
        return

    idmap.get(protein_key)
    parse_refs(block, protein_key, idmap, edges)
