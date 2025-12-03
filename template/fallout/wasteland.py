from fallout.vault import Vault
from typing import List, Optional, Tuple, Set


class Wasteland:
    def __init__(self) -> None:
        pass

    # R3
    def add_vaults(self, vaults: List[Vault]) -> None:
        pass
    
    def connect_vaults(self, vault_name_1: str, vault_name_2: str, distance: int) -> None:       
        pass

    def get_connected(self, vault_name: str) -> Set[str]:
        pass

    def get_distance(self, vault_name_1: str, vault_name_2: str) -> Optional[int]:
        pass

    # R4
    def find_path(self, vault_start_name: str, vault_end_name: str) -> Optional[Tuple[List[str], int]]:
        pass
        