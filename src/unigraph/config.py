from pathlib import Path


class Config:
    def __init__(
        self,
        input_dir: Path,
        output_graph: Path,
        output_nodes: Path,
        output_stats: Path,
        organism_filter: set[str] | None = None,
    ):
        self.input_dir = Path(input_dir)
        self.output_graph = Path(output_graph)
        self.output_nodes = Path(output_nodes)
        self.output_stats = Path(output_stats)
        self.organism_filter = organism_filter or set()
