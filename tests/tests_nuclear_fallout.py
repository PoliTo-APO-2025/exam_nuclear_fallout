import unittest
import inspect
from fallout.vault import Vault, VaultException, VaultResource
from fallout.wasteland import Wasteland


class TestR0(unittest.TestCase):
    def test_abstract(self):
        self.assertTrue(inspect.isabstract(VaultResource))


class TestR1(unittest.TestCase):
    def setUp(self):
        self._v1 = Vault("v1")

    def test_add_role_stats(self):
        r1 = self._v1.add_role("r1", 3, 7, 0)
        self.assertEqual("r1", r1.name)
        self.assertEqual([3, 7, 0], [r1.food, r1.health, r1.maintenance])

    def test_add_dweller_stats(self):
        self._v1.add_role("r1", 3, 7, 0)
        self._v1.add_role("r2", 2, 4, 1)
        d1 = self._v1.add_dweller("d1", 20, "r1", "r2")
        self.assertEqual("d1", d1.name)
        self.assertEqual([5, 11, 1], [d1.food, d1.health, d1.maintenance])

    def test_add_dweller_len(self):
        self._v1.add_role("r1", 3, 7, 0)
        self._v1.add_role("r2", 2, 4, 1)
        self._v1.add_role("r3", 0, 0, 1)
        d1 = self._v1.add_dweller("d1", 20, "r1", "r2", "r3")
        self.assertEqual(3, len(d1))

    def test_add_role_len(self):
        r1 = self._v1.add_role("r1", 3, 7, 0)
        r2 = self._v1.add_role("r2", 2, 4, 1)
        r3 = self._v1.add_role("r3", 0, 0, 1)
        roles = [r1, r2, r3]
        self.assertEqual([0, 0, 0], [len(r) for r in roles])
        self._v1.add_dweller("d1", 20, "r1", "r2")
        self.assertEqual([1, 1, 0], [len(r) for r in roles])
        self._v1.add_dweller("d2", 20, "r2", "r3")
        self.assertEqual([1, 2, 1], [len(r) for r in roles])

    def test_get_resource(self):
        self._v1.add_role("r1", 3, 7, 0)
        self._v1.add_role("r3", 0, 0, 1)
        self._v1.add_role("r2", 2, 4, 1)
        self._v1.add_dweller("d2", 20, "r1", "r2")
        self._v1.add_dweller("d1", 20, "r1")
        res = [self._v1.get_resource(r) for r in ["r1", "r2", "r3", "d1", "d2"]]
        self.assertEqual(["r1", "r2", "r3", "d1", "d2"], [r.name for r in res])
        
    def test_add_dweller_exception(self):
        self._v1.add_role("r1", 3, 7, 0)
        self._v1.add_role("r2", 2, 4, 1)
        self._v1.add_dweller("d1", 20, "r1", "r2")
        self.assertRaises(VaultException, self._v1.add_dweller, "d2", 15, "r1", "r2")


class TestR2(unittest.TestCase):
    def setUp(self):
        self._v1 = Vault("v1")
        self._v1.add_role("r1", 3, 7, 0)
        self._v1.add_role("r2", 2, 4, 1)
        self._v1.add_role("r3", 0, 0, 1)
        self._v1.add_dweller("d1", 20, "r1", "r2")
        self._v1.add_dweller("d2", 10, "r2", "r3")
        self._v1.add_dweller("d3", 25, "r1", "r2")
    
    def test_get_resource_dept(self):
        self._v1.add_department("dpt1", ["d1", "d2"], lambda x: sum(x))
        self._v1.add_department("dpt2", ["d1", "d3"], lambda x: sum(x)/len(x))
        self.assertEqual("dpt1", self._v1.get_resource("dpt1").name)
        self.assertEqual("dpt2", self._v1.get_resource("dpt2").name)

    def test_add_department_length(self):
        dpt1 = self._v1.add_department("dpt1", ["d1", "d3"], lambda x: sum(x))
        dpt2 = self._v1.add_department("dpt2", ["d1", "d3", "d2"], lambda x: sum(x)/len(x))
        self.assertEqual(2, len(dpt1))
        self.assertEqual(3, len(dpt2))
    
    def test_add_department_stats(self):
        dpt1 = self._v1.add_department("dpt1", ["d1", "d2"], lambda x: sum(x))
        dpt2 = self._v1.add_department("dpt2", ["d1", "d2", "d3"], lambda x: sum(x)/len(x))
        self.assertEqual([7, 15, 3], [dpt1.food, dpt1.health, dpt1.maintenance])
        self.assertEqual([4, 9, 1], [dpt2.food, dpt2.health, dpt2.maintenance])

    def test_get_most_productive_dweller(self):
        self._v1.add_department("dpt1", ["d1", "d2", "d3"], lambda x: sum(x))
        self._v1.add_department("dpt2", ["d2", "d3"], lambda x: sum(x))
        self.assertIn(self._v1.get_most_productive_dweller("dpt1"), {('d1', 17), ('d3', 17)})
        self.assertEqual(('d3', 17), self._v1.get_most_productive_dweller("dpt2"))


class TestR3(unittest.TestCase):
    def setUp(self):
        self._wl = Wasteland()
        self._wl.add_vaults([
                Vault("v1"), Vault("v2"),
                Vault("v3"), Vault("v4"),
                Vault("v5"), Vault("v6")
        ])
        self._wl.connect_vaults("v1", "v2", 3)
        self._wl.connect_vaults("v1", "v4", 2)
        self._wl.connect_vaults("v2", "v3", 1)
        self._wl.connect_vaults("v4", "v3", 4)
        self._wl.connect_vaults("v3", "v5", 5)
    
    def test_get_connected(self):
        self.assertEqual({"v2", "v4"}, self._wl.get_connected("v1"))
        self.assertEqual({"v1", "v3"}, self._wl.get_connected("v2")) 
        self.assertEqual({"v2", "v4", "v5"}, self._wl.get_connected("v3")) 
        self.assertEqual({"v1", "v3"}, self._wl.get_connected("v4")) 
        self.assertEqual({"v3"}, self._wl.get_connected("v5"))

    def test_get_distance(self):
        self.assertEqual(3, self._wl.get_distance("v1", "v2"))
        self.assertEqual(2, self._wl.get_distance("v1", "v4"))
        self.assertEqual(1, self._wl.get_distance("v2", "v3"))
        self.assertEqual(4, self._wl.get_distance("v4", "v3"))
        self.assertEqual(5, self._wl.get_distance("v3", "v5"))

    def test_edge_cases(self):
        self.assertIsNotNone(self._wl.get_distance("v1", "v2"))
        self.assertIsNotNone(self._wl.get_connected("v1"))
        self.assertEqual(set(), self._wl.get_connected("v6"))
        self.assertIsNone(self._wl.get_distance("v1", "v3"))
        self.assertIsNone(self._wl.get_distance("v4", "v6"))    


class TestR4(unittest.TestCase):
    def setUp(self):
        self._wl = Wasteland()
        self._wl.add_vaults([
                Vault("v1"), Vault("v2"),
                Vault("v3"), Vault("v4"),
                Vault("v5"), Vault("v6")
        ])
    
    def test_find_path(self):
        self._wl.connect_vaults("v1", "v2", 2)
        self._wl.connect_vaults("v1", "v3", 3)
        self._wl.connect_vaults("v2", "v4", 4)
        self._wl.connect_vaults("v3", "v5", 1)
        self.assertEqual(['v1', 'v3', 'v5'], self._wl.find_path("v1", "v5")[0])

    def test_find_distance(self):
        self._wl.connect_vaults("v1", "v2", 2)
        self._wl.connect_vaults("v1", "v3", 3)
        self._wl.connect_vaults("v2", "v4", 4)
        self._wl.connect_vaults("v3", "v5", 1)
        self.assertEqual(4, self._wl.find_path("v1", "v5")[1])

    def test_missing_path(self):
        self._wl.connect_vaults("v1", "v2", 5)
        self.assertIsNotNone(self._wl.find_path("v1", "v2"))
        self.assertIsNone(self._wl.find_path("v1", "v3"))

    def test_find_path_full(self):
        self._wl.connect_vaults("v1", "v2", 3)
        self._wl.connect_vaults("v1", "v4", 2)
        self._wl.connect_vaults("v2", "v3", 1)
        self._wl.connect_vaults("v4", "v3", 4)
        self._wl.connect_vaults("v3", "v5", 5)
        path = self._wl.find_path("v1", "v5")
        path = (tuple(path[0]), path[1])
        self.assertIn(path, {(('v1', 'v2', 'v3', 'v5'), 9), (('v1', 'v4', 'v3', 'v5'), 11)})
