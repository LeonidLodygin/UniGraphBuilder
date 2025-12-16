from pathlib import Path
from typing import Iterable


def read_dat_blocks(path: Path) -> Iterable[str]:
    block: list[str] = []
    with path.open() as f:
        for line in f:
            if line.startswith("//"):
                yield "".join(block)
                block.clear()
            else:
                block.append(line)
