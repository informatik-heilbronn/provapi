import unittest
import backend as fe


class TestComparisonBadCases(unittest.TestCase):
    def test_Comparison_WithoutArguments(self):
        with self.assertRaises(TypeError):
            self.assertEqual(1, fe.start_comparison(None, None, None, None))

    def test_Comparison_WithEmptyString(self):
        self.assertEqual(1, fe.start_comparison("", "", "", ""))

    def test_InvalidComparison(self):
        self.assertEqual(1, fe.start_comparison("L", "G", "L", "B"))
