from fallout.vault import Vault
from typing import List, Optional, Tuple, Set


class Wasteland:
    def __init__(self) -> None:
        self._vaults = {}

    # R3
    def add_vaults(self, vaults: List[Vault]) -> None:
        for v in vaults:
            self._vaults[v.name] = v
    
    def connect_vaults(self, vault_name_1: str, vault_name_2: str, distance: int) -> None:       
        self._vaults[vault_name_1].connect(self._vaults[vault_name_2], distance)
        self._vaults[vault_name_2].connect(self._vaults[vault_name_1], distance)

    def get_connected(self, vault_name: str) -> Set[str]:
        return set(self._vaults[vault_name].connected.keys())

    def get_distance(self, vault_name_1: str, vault_name_2: str) -> Optional[int]:
        v1 = self._vaults[vault_name_1]
        return v1.connected[vault_name_2].distance if vault_name_2 in v1.connected else None

    # R4
    def find_path(self, vault_start_name: str, vault_end_name: str) -> Optional[Tuple[List[str], int]]:
        visited = {vault_start_name}
        paths = [([self._vaults[vault_start_name]], 0)]
        while paths:
            path, dist = paths.pop(0)
            if path[-1].name == vault_end_name:
                return [v.name for v in path], dist
            for conn in path[-1].connected.values():
                if conn.vault.name not in visited:        
                    paths.append((path + [conn.vault], dist + conn.distance))
                    visited.add(conn.vault.name)
        return None       
        