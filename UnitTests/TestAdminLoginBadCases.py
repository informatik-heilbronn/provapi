import unittest
import login


class TestAdminLoginBadCases(unittest.TestCase):
    def test_bad_username(self):
        self.assertFalse(login.check_userinfo("admun", "123"))

    def test_bad_password(self):
        self.assertFalse(login.check_userinfo("admin", "124"))

    def test_empty_username(self):
        self.assertFalse(login.check_userinfo("", "123"))

    def test_empty_password(self):
        self.assertFalse(login.check_userinfo("admin", ""))

    def test_both_empty(self):
        self.assertFalse(login.check_userinfo("", ""))

    def test_username_isNone(self):
        self.assertFalse(login.check_userinfo(None, "123"))

    def test_password_isNone(self):
        self.assertFalse(login.check_userinfo("admin", None))

    def test_both_isNone(self):
        self.assertFalse(login.check_userinfo(None, None))
