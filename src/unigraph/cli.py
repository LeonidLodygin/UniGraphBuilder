import argparse
from pathlib import Path

from unigraph.config import Config
from unigraph.edges import EdgeStore
from unigraph.idmap import IDMap
from unigraph.io.reader import read_dat_blocks
from unigraph.io.writer import write_graph, write_nodes, write_stats
from unigraph.parsers.entry import parse_entry


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Parse UniProt .dat files to graph format"
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=Path("data"),
        help="Directory with .dat files (default: data)",
    )
    parser.add_argument(
        "--output-graph",
        type=Path,
        default=Path("output/graph.g"),
        help="Output graph edges file (default: graph.g)",
    )
    parser.add_argument(
        "--output-nodes",
        type=Path,
        default=Path("output/nodes.tsv"),
        help="Output nodes file (default: nodes.tsv)",
    )
    parser.add_argument(
        "--output-stats",
        type=Path,
        default=Path("output/stats.txt"),
        help="Output stats file (default: stats.txt)",
    )
    parser.add_argument(
        "--taxid",
        action="append",
        default=None,
        help="NCBI TaxID to filter by. Can specify multiple times.",
    )
    args = parser.parse_args()

    organism_filter = set(args.taxid) if args.taxid else set()
    cfg = Config(
        input_dir=args.input_dir,
        output_graph=args.output_graph,
        output_nodes=args.output_nodes,
        output_stats=args.output_stats,
        organism_filter=organism_filter,
    )
    idmap = IDMap()
    edges = EdgeStore()
    for path in cfg.input_dir.glob("*.dat"):
        for block in read_dat_blocks(path):
            parse_entry(block, idmap, edges, cfg.organism_filter)

    write_graph(cfg.output_graph, edges)
    write_nodes(cfg.output_nodes, idmap)
    write_stats(cfg.output_stats, idmap, edges)

    print("Done.")
