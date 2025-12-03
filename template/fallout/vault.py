from abc import ABC, abstractmethod
from typing import List, Callable, Tuple


class VaultException(Exception):
    pass


class VaultResource(ABC):
    @property
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def food(self) -> int:
        pass

    @property
    @abstractmethod
    def health(self) -> int:
        pass

    @property
    @abstractmethod
    def maintenance(self) -> int:
        pass
    
    def __len__(self) -> int:
        pass


class Vault:
    def __init__(self, name) -> None:
        pass

    # R1
    def add_role(self, name: str, food: int, health: int, maintenance: int) -> VaultResource:
        pass

    def add_dweller(self, name: str, vitality: int, *roles: str) -> VaultResource:
        pass

    def get_resource(self, name: str) -> VaultResource:
        pass

    # R2
    def add_department(self, name: str, dwellers: List[str], func: Callable[[List[int]], int] = None) -> VaultResource:
        pass

    def get_most_productive_dweller(self, dept_name) -> Tuple[str, int]:
        pass
