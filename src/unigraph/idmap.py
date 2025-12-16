class IDMap:
    def __init__(self) -> None:
        self._map: dict[str, int] = {}
        self._counter = 0

    def get(self, key: str) -> int:
        if key not in self._map:
            self._map[key] = self._counter
            self._counter += 1
        return self._map[key]

    def size(self) -> int:
        return self._counter

    def items(self):
        return self._map.items()
