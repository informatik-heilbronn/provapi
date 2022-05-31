import unittest
import ocr as td


class TestOCRBadCases(unittest.TestCase):
    def test_kein_bauschein(self):
        file_path = None
        with self.assertRaises(TypeError):
            td.get_bauschein_from_file(file_path)

    def test_bauschein_unleserlich(self):
        td.set_blur("./UnitTests/Bauschein.png")
        self.assertEqual("L", td.codes[0])
        self.assertEqual("B", td.codes[1])
        td.codes = ()
        td.set_blur("./UnitTests/Bauscheinschlecht.PNG")
        self.assertEqual((), td.codes)

