import unittest
from unittest.mock import MagicMock, patch, call
import pygame
from pygame.locals import MOUSEBUTTONDOWN, KEYDOWN, K_ESCAPE
from pygame import Rect, Vector2, K_SPACE, Surface
from pygame.event import Event
import sys, os

sys.path.append(
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
)
from pygame_gui import Controller, Control, ChangeChecker
import logging


class TestControl(unittest.TestCase):

    def setUp(self):
        self.mock_screen = MagicMock(spec=Surface)
        self.mock_controller = Controller(self.mock_screen)
        self.mock_controller.change_checker = MagicMock(spec=ChangeChecker)
        self.control = Control(self.mock_controller)

    def test_init(self):
        logging.info(f"TestControl.test_init:start")
        self.assertEqual(self.control.manager, self.mock_controller)
        self.assertTrue(self.control.visible)
        self.assertTrue(self.control.enabled)
        self.assertTrue(self.control.focusable)
        self.assertEqual(self.control.size, Vector2(100, 100))
        self.assertEqual(self.control.position, Vector2(0, 0))
        self.assertEqual(self.control.rect, Rect(Vector2(0, 0), Vector2(100, 100)))
        self.assertEqual(self.mock_controller.change_checker.add_change.call_count, 2)  # type: ignore
        logging.info(f"TestControl.test_init:end")

    def test_update_rect(self):
        logging.info(f"TestControl.test_update_rect:start")
        original_rect = self.control.rect
        self.control.size = Vector2(200, 200)
        self.control.update_rect()
        self.assertNotEqual(self.control.rect, original_rect)
        self.assertEqual(
            self.control.rect, Rect(self.control.position, self.control.size)
        )
        logging.info(f"TestControl.test_update_rect:end")


if __name__ == "__main__":
    unittest.main()
