from fallout.vault import Vault, VaultException
from fallout.wasteland import Wasteland


def main():
    print("----------------- R1 -----------------")
    v1 = Vault("Vault1")

    medic = v1.add_role("Medic", 1, 8, 3)    
    print(medic.name)                                       # Medic
    print([medic.food, medic.health, medic.maintenance])    # [1, 8, 3]
    print(len(medic))                                       # 0

    mechanic = v1.add_role("Mechanic", 3, 2, 9)             
    print(mechanic.name)                                            # Mechanic
    print([mechanic.food, mechanic.health, mechanic.maintenance])   # [3, 2, 9]
    print(len(mechanic))                                            # 0

    dw1 = v1.add_dweller("Citizen1", 35, "Medic", "Mechanic")
    print(dw1.name)                                 # Citizen1
    print([dw1.food, dw1.health, dw1.maintenance])  # [4, 10, 12]
    print(len(dw1))                                 # 2
    print([len(medic), len(mechanic)])              # [1, 1]

    print(v1.get_resource("Mechanic").name)         # Mechanic
    print(v1.get_resource("Medic").name)            # Medic
    print(v1.get_resource("Citizen1").name)         # Citizen1

    try:
        v1.add_dweller("Citizen0", 11, "Medic")
        print("[Error] Insufficient vitality not detected")
    except VaultException:
        print("Correctly detected: insufficient vitality")  # Correctly detected: insufficient vitality

    print("----------------- R2 -----------------")
    v1.add_dweller("Citizen2", 20, "Mechanic")
    dept1 = v1.add_department("Dept1", ["Citizen1", "Citizen2"], lambda x: sum(x))
    print(dept1.name)                                       # Dept1
    print([dept1.food, dept1.health, dept1.maintenance])    # [7, 12, 21]
    print(len(dept1))                                       # 2

    print(v1.get_most_productive_dweller("Dept1"))          # ('Citizen1', 26)

    print(v1.get_resource("Dept1").name)                    # Dept1

    print("----------------- R3 -----------------")
    wl = Wasteland()
    v2, v3 = Vault("Vault2"), Vault("Vault3")
    v4, v5 = Vault("Vault4"), Vault("Vault5")    
    wl.add_vaults([v1, v2, v3, v4, v5])

    wl.connect_vaults("Vault1", "Vault2", 3)
    wl.connect_vaults("Vault1", "Vault3", 2)
    wl.connect_vaults("Vault2", "Vault4", 1)
    wl.connect_vaults("Vault3", "Vault4", 4)

    print(wl.get_connected("Vault1"))   # {'Vault2', 'Vault3'}
    print(wl.get_connected("Vault2"))   # {'Vault4', 'Vault1'}
    print(wl.get_connected("Vault3"))   # {'Vault4', 'Vault1'}
    print(wl.get_connected("Vault4"))   # {'Vault2', 'Vault3'}
    print(wl.get_connected("Vault5"))   # set()

    print(wl.get_distance("Vault1", "Vault2"))  # 3
    print(wl.get_distance("Vault1", "Vault3"))  # 2
    print(wl.get_distance("Vault2", "Vault4"))  # 1
    print(wl.get_distance("Vault3", "Vault4"))  # 4
    print(wl.get_distance("Vault1", "Vault4"))  # None
    print(wl.get_distance("Vault4", "Vault5"))  # None

    print("----------------- R4 -----------------") 
    print(wl.find_path("Vault4", "Vault3"))  # (['Vault4', 'Vault3'], 4) o (['Vault4', 'Vault2', 'Vault1', 'Vault3'], 6)
    print(wl.find_path("Vault2", "Vault3"))  # (['Vault2', 'Vault1', 'Vault3'], 5) o (['Vault2', 'Vault4', 'Vault3'], 5)
    print(wl.find_path("Vault3", "Vault5"))  # None


if __name__ == "__main__":
    main()
