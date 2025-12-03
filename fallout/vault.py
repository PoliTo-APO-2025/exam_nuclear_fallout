from abc import ABC, abstractmethod
from typing import List, Callable, Tuple
from dataclasses import dataclass


class VaultException(Exception):
    pass


class VaultResource(ABC):
    def __init__(self, name):
        self._name = name

    @property
    def name(self) -> str:
        return self._name

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


class Role(VaultResource):
    def __init__(self, name, food, health, maintenance):
        super().__init__(name)
        self._food = food
        self._health = health
        self._maintenance = maintenance
        self._dwellers = []

    def add_dweller(self, dweller):
        self._dwellers.append(dweller)

    @property
    def dwellers(self):
        return self._dwellers

    @property
    def food(self) -> int:
        return self._food

    @property
    def health(self) -> int:
        return self._health

    @property
    def maintenance(self) -> int:
        return self._maintenance

    def __len__(self):
        return len(self._dwellers)
    

class Dweller(VaultResource):
    def __init__(self, name, vitality, *roles):
        super().__init__(name)
        self._vitality = vitality        
        self._roles = roles
        if vitality < self.food + self.health + self.maintenance:
            raise VaultException("Insufficient vitality")
    
    @property
    def roles(self):
        return self._roles

    @property
    def vitality(self):
        return self._vitality

    @property
    def food(self) -> int:
        return sum([r.food for r in self._roles])
    
    @property
    def health(self) -> int:
        return sum([r.health for r in self._roles])

    @property
    def maintenance(self) -> int:
        return sum([r.maintenance for r in self._roles])
    
    def __len__(self):
        return len(self._roles)
    

class Department(VaultResource):

    def __init__(self, name, dwellers, func):
        super().__init__(name)
        self._dwellers = dwellers
        self._func = func

    @property
    def dwellers(self):
        return self._dwellers

    @property
    def food(self) -> int:
        return round(self._func([r.food for r in self._dwellers]))
    
    @property
    def health(self) -> int:
        return round(self._func([r.health for r in self._dwellers]))

    @property
    def maintenance(self) -> int:
        return round(self._func([r.maintenance for r in self._dwellers]))
    
    def __len__(self):
        return len(self._dwellers)


class Vault:
    def __init__(self, name) -> None:
        self._resources = {}
        self._name = name
        self._connected = {}

    @dataclass
    class VaultConnection:
        vault: "Vault"
        distance: int
    
    @property
    def name(self):
        return self._name
    
    def connect(self, vault, distance):
        self._connected[vault.name] = Vault.VaultConnection(vault, distance)

    @property
    def connected(self):
        return self._connected

    # R1
    def add_role(self, name: str, food: int, health: int, maintenance: int) -> VaultResource:
        role = Role(name, food, health, maintenance)
        self._resources[name] = role
        return role

    def add_dweller(self, name: str, vitality: int, *roles: str) -> VaultResource:
        roles = [self._resources[r] for r in roles]
        dweller = Dweller(name, vitality, *roles)
        self._resources[name] = dweller
        for r in roles:
            r.add_dweller(dweller)
        return dweller

    def get_resource(self, name: str) -> VaultResource:
        return self._resources[name]

    # R2
    def add_department(self, name: str, dwellers: List[str], func: Callable[[List[int]], int] = None) -> VaultResource:
        dept = Department(name, [self._resources[d] for d in dwellers], func)
        self._resources[name] = dept
        return dept

    def get_most_productive_dweller(self, dept_name) -> Tuple[str, int]:
        dept = self._resources[dept_name]
        return max(map(lambda d: (d.name, d.health + d.maintenance + d.food), dept.dwellers), key=lambda t: t[1])
