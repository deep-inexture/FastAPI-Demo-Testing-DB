from typing import Protocol


class DBInterface(Protocol):
    def read_all(self):
        ...
