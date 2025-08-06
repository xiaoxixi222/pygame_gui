import unittest
from unittest.mock import Mock, MagicMock
from pygame_gui import ChangeChecker
import logging


class TestChangeChecker(unittest.TestCase):

    def setUp(self):
        logging.disable(logging.DEBUG)
        self.change_checker = ChangeChecker()

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def test_check_no_changes(self):
        logging.info("test_check_no_changes:start")
        obj = Mock()
        obj.attr = 10
        func_mock = MagicMock()
        self.change_checker.add_change(obj, "attr", func_mock)
        self.change_checker.check()
        func_mock.assert_not_called()
        logging.info("test_check_no_changes:end")

    def test_check_with_changes(self):
        logging.info("test_check_with_changes:start")
        obj = Mock()
        obj.attr = 10
        func_mock = MagicMock()
        self.change_checker.add_change(obj, "attr", func_mock)
        obj.attr = 20
        self.change_checker.check()
        func_mock.assert_called_once_with(20, 10)
        logging.info("test_check_with_changes:end")

    def test_add_change(self):
        logging.info("test_add_change:start")
        obj = Mock()
        obj.attr = 10
        func_mock = MagicMock()
        self.change_checker.add_change(obj, "attr", func_mock)
        self.assertIn((obj, "attr", func_mock), self.change_checker.change)
        self.assertIn((obj, "attr", func_mock), self.change_checker.old_values.keys())
        self.assertEqual(self.change_checker.old_values[(obj, "attr", func_mock)], 10)
        logging.info("test_add_change:end")

    def test_remove_change(self):
        logging.info("test_remove_change:start")
        obj = Mock()
        obj.attr = 10
        func_mock = MagicMock()
        self.change_checker.add_change(obj, "attr", func_mock)
        self.change_checker.remove_change(obj, "attr", func_mock)
        self.assertNotIn((obj, "attr", func_mock), self.change_checker.change)
        self.assertNotIn((obj, "attr", func_mock), self.change_checker.old_values)
        logging.info("test_remove_change:end")

    def test_add_duplicate_change(self):
        logging.info("test_add_duplicate_change:start")
        obj = Mock()
        obj.attr = 10
        func_mock = MagicMock()
        self.change_checker.add_change(obj, "attr", func_mock)
        self.change_checker.add_change(obj, "attr", func_mock)
        self.assertEqual(len(self.change_checker.change), 1)
        self.assertEqual(len(self.change_checker.old_values), 1)
        logging.info("test_add_duplicate_change:end")

    def test_remove_nonexistent_change(self):
        logging.info("test_remove_nonexistent_change:start")
        obj = Mock()
        obj.attr = 10
        func_mock = MagicMock()
        self.change_checker.remove_change(obj, "attr", func_mock)
        self.assertEqual(len(self.change_checker.change), 0)
        self.assertEqual(len(self.change_checker.old_values), 0)
        logging.info("test_remove_nonexistent_change:end")


if __name__ == "__main__":
    unittest.main()
