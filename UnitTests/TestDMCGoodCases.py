import unittest
import keys
import dmcr as dmc

pattern_list = keys.get_leitung_keys() + keys.get_tank_keys()


class TestDMCGoodCases(unittest.TestCase):
    def test_readDMC_Code(self):
        x = dmc.get_dmc_from_file("./UnitTests/DMC_LeitungB.png")
        self.assertEqual("B", x)

