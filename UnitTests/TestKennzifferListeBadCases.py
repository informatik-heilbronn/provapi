import unittest
import keys


class TestKennzifferListeBadCases(unittest.TestCase):
    def test_kennziffer_hinzufuegen_tank_isNone(self):
        with self.assertRaises(Exception):
            keys.add_tank_key(None)

    def test_kennziffer_loeschen_tank_isNone(self):
        with self.assertRaises(Exception):
            keys.remove_tank_key(None)

    def test_kennziffer_hinzufuegen_leitung_isNone(self):
        with self.assertRaises(Exception):
            keys.add_leitung_key(None)

    def test_kennziffer_loeschen_leitung_isNone(self):
        with self.assertRaises(Exception):
            keys.remove_leitung_key(None)

    def test_kennziffer_hinzufuegen_tank_no_string(self):
        with self.assertRaises(Exception):
            no_string = [0, 1, 2]
            keys.add_tank_key(no_string)

    def test_kennziffer_loeschen_tank_no_string(self):
        with self.assertRaises(Exception):
            no_string = [0, 1, 2]
            keys.remove_tank_key(no_string)

    def test_kennziffer_hinzufuegen_leitung_no_string(self):
        with self.assertRaises(Exception):
            no_string = [0, 1, 2]
            keys.add_leitung_key(no_string)

    def test_kennziffer_loeschen_leitung_no_string(self):
        with self.assertRaises(Exception):
            no_string = [0, 1, 2]
            keys.remove_leitung_key(no_string)

    def test_kennziffer_hinzufuegen_tank_empty(self):
        with self.assertRaises(Exception):
            keys.add_tank_key("")

    def test_kennziffer_loeschen_tank_empty(self):
        with self.assertRaises(Exception):
            keys.remove_tank_key("")

    def test_kennziffer_hinzufuegen_leitung_empty(self):
        with self.assertRaises(Exception):
            keys.add_leitung_key("")

    def test_kennziffer_loeschen_leitung_empty(self):
        with self.assertRaises(Exception):
            keys.remove_leitung_key("")

    def test_kennziffer_loeschen_tank_key_not_found(self):
        with self.assertRaises(Exception):
            keys.remove_tank_key("invalid key")

    def test_kennziffer_loeschen_leitung_key_not_found(self):
        with self.assertRaises(Exception):
            keys.remove_leitung_key("invalid key")

    def test_kennziffer_hinzufuegen_tank_only_whitespace(self):
        with self.assertRaises(Exception):
            keys.add_tank_key("   ")

    def test_kennziffer_loeschen_tank_only_whitespace(self):
        with self.assertRaises(Exception):
            keys.remove_tank_key("   ")

    def test_kennziffer_hinzufuegen_leitung_only_whitespace(self):
        with self.assertRaises(Exception):
            keys.add_leitung_key("   ")

    def test_kennziffer_loeschen_leitung_only_whitespace(self):
        with self.assertRaises(Exception):
            keys.remove_leitung_key("   ")
