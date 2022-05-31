import unittest
import dmcr
import keys

pattern_list = keys.get_leitung_keys() + keys.get_tank_keys()


class TestDMCBadCases(unittest.TestCase):
    def test_readDMC_WithoutFilePath(self):
        file_path = None
        with self.assertRaises(TypeError):
            dmcr.get_dmc_from_file(file_path)

    def test_readDMC_DMCNotReadable(self):
        x = dmcr.get_dmc_from_file("./UnitTests/DMC_NotReadable.png")
        self.assertEqual("C", x[0])

