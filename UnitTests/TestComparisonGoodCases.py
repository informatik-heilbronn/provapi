import unittest
import backend as fe

class TestComparisonGoodCases(unittest.TestCase):
    def test_GoodComparison(self):
        self.assertEqual(3, fe.start_comparison("L", "B", "L", "B"))

    def test_BadComparison(self):
        self.assertEqual(2, fe.start_comparison("L", "B", "L", "A"))

    def test_Logfile(self):
        with open("comparison.log") as logfile:
            for i, l in enumerate(logfile):
                i += 1
        fe.start_comparison("L", "B", "L", "B")
        with open("comparison.log") as logfile:
            for j, l in enumerate(logfile):
                j += 1
        self.assertEqual(i+1, j)
