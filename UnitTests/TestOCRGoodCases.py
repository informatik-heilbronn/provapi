import unittest
import ocr as td


class TestOCRGoodCases(unittest.TestCase):
    def test_richtiger_code(self):
        codes = td.get_bauschein_from_file("./UnitTests/Bauschein.png")
        self.assertEqual("B", codes[1])
        self.assertEqual("L", codes[0])

    def test_reset_globals(self):
        td.get_bauschein_from_file("./UnitTests/Bauschein.png")
        self.assertEqual((), td.codes)
        self.assertIsNone(td.img)
        self.assertFalse(td.match)

