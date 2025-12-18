# UniGraphBuilder

UniGraphBuilder is a Python-based tool to parse [UniProt](https://www.uniprot.org/) .dat files and convert biological data into graph format for downstream analysis. It extracts proteins, their relationships, and annotations, producing graph edges, nodes, and summary statistics.

## Features

- Parses UniProt .dat files and extracts relationships between proteins and entities like KEGG, STRING, GO, InterPro, PubMed, GeneID, and HOGENOM

- Filters data by organism taxonomic IDs (NCBI TaxIDs)

- Outputs graph edges, node lists, and statistics in easy-to-use text formats

- Modular, extensible codebase with CLI support

## Why use UniGraphBuilder?

UniGraphBuilder helps researchers transform complex UniProt datasets into graph representations for network analysis, visualization, and integration with other omics data. It automates parsing and linking biological entities efficiently.

## Requirements

- [Python 3.10 or higher](https://wiki.python.org/moin/BeginnersGuide/Download)

- Poetry(recommended for managing dependencies and virtual environments)

## Installation

Clone this repository and install dependencies via Poetry:

```shell
poetry install
```

Alternatively, you can manually create a virtual environment and install dependencies from pyproject.toml.

## Usage

The main entry point is the CLI script:

```shell
poetry run unigraph --input-dir data --output-graph output/graph.g --output-nodes output/nodes.tsv --output-stats output/stats.txt
```

Arguments:

- --input-dir: Directory containing .dat UniProt files (default: data)

- --output-graph: Output file path for graph edges (default: output/graph.g)

- --output-nodes: Output file path for node list (default: output/nodes.tsv)

- --output-stats: Output file path for parsing statistics (default: output/stats.txt)

- --taxid: NCBI Taxonomic ID to filter entries by organism (can specify multiple times)

Example with organism filter:

```shell
poetry run unigraph --taxid 9606 --taxid 10090
```

This command processes only proteins from organisms with TaxIDs 9606 (human) and 10090 (mouse).

## Usage example

### Input data

UniGraphBuilder works with **UniProt `.dat` files** in the official *UniProt flat file format*.
These files can be downloaded from the UniProt website:

- https://www.uniprot.org/help/downloads

For example, you can download the reviewed protein dataset:

- `uniprot_sprot.dat.gz`

After downloading, the file must be decompressed. 
.dat file contains multiple UniProt records separated by //.

### Example scenario

Suppose we want to build a biological graph for human proteins
(Homo sapiens, NCBI TaxID = 9606) and include relationships to external
databases such as GO, KEGG, STRING, GeneID, and PubMed.

### Step 1: Prepare input files

Place UniProt .dat files into 'data' directory.

### Step 2: Run the tool

```shell
poetry run unigraph
```

### Output files

After execution, the output directory contains:

- nodes.tsv (Mapping of entity identifiers to numeric node IDs)
- stats.txt (Summary statistics: nodes, edges per relation type)
- graph.g

## How it works

UniGraphBuilder reads .dat files from the input directory, parses them entry-by-entry, extracts protein IDs and cross-references, creates nodes and edges representing biological relationships, and saves the results in simple, tab-separated files.

## Development

Code is organized in modules for parsing, graph data management, and I/O.

Tests are included and can be run with pytest:

```shell
poetry run pytest
```

## License

Apache-2.0