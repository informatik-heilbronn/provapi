import unittest
import login


class TestAdminLoginGoodCases(unittest.TestCase):
    def test_login(self):
        self.assertTrue(login.check_userinfo("admin", "123"))
