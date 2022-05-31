import unittest
import keys


class TestKennzifferListeGoodCases(unittest.TestCase):
    def test_kennziffer_hinzufuegen_tank(self):
        self.assertNotIn("test", keys.get_tank_keys())
        keys.add_tank_key("test")
        self.assertIn("test", keys.get_tank_keys())
        keys.remove_tank_key("test")

    def test_kennziffer_loeschen_tank(self):
        keys.add_tank_key("test")
        self.assertIn("test", keys.get_tank_keys())
        keys.remove_tank_key("test")
        self.assertNotIn("test", keys.get_tank_keys())

    def test_kennziffer_hinzufuegen_leitung(self):
        self.assertNotIn("test", keys.get_leitung_keys())
        keys.add_leitung_key("test")
        self.assertIn("test", keys.get_leitung_keys())
        keys.remove_leitung_key("test")

    def test_kennziffer_loeschen_leitung(self):
        keys.add_leitung_key("test")
        self.assertIn("test", keys.get_leitung_keys())
        keys.remove_leitung_key("test")
        self.assertNotIn("test", keys.get_leitung_keys())

    def test_kennziffer_hinzufuegen_tank_int(self):
        self.assertNotIn("123", keys.get_tank_keys())
        keys.add_tank_key(123)
        self.assertIn("123", keys.get_tank_keys())
        keys.remove_tank_key(123)

    def test_kennziffer_loeschen_tank_int(self):
        keys.add_tank_key(123)
        self.assertIn("123", keys.get_tank_keys())
        keys.remove_tank_key(123)
        self.assertNotIn("123", keys.get_tank_keys())

    def test_kennziffer_hinzufuegen_leitung_int(self):
        self.assertNotIn("123", keys.get_leitung_keys())
        keys.add_leitung_key(123)
        self.assertIn("123", keys.get_leitung_keys())
        keys.remove_leitung_key(123)

    def test_kennziffer_loeschen_leitung_int(self):
        keys.add_leitung_key(123)
        self.assertIn("123", keys.get_leitung_keys())
        keys.remove_leitung_key(123)
        self.assertNotIn("123", keys.get_leitung_keys())

    def test_kennziffer_hinzufuegen_tank_float(self):
        self.assertNotIn("123123", keys.get_tank_keys())
        keys.add_tank_key(123.123)
        self.assertIn("123123", keys.get_tank_keys())
        keys.remove_tank_key(123.123)

    def test_kennziffer_loeschen_tank_float(self):
        keys.add_tank_key(123.123)
        self.assertIn("123123", keys.get_tank_keys())
        keys.remove_tank_key(123.123)
        self.assertNotIn("123123", keys.get_tank_keys())

    def test_kennziffer_hinzufuegen_leitung_float(self):
        self.assertNotIn("123123", keys.get_leitung_keys())
        keys.add_leitung_key(123.123)
        self.assertIn("123123", keys.get_leitung_keys())
        keys.remove_leitung_key(123.123)

    def test_kennziffer_loeschen_leitung_float(self):
        keys.add_leitung_key(123.123)
        self.assertIn("123123", keys.get_leitung_keys())
        keys.remove_leitung_key(123.123)
        self.assertNotIn("123123", keys.get_leitung_keys())

