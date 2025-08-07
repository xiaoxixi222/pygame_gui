import unittest
from unittest.mock import MagicMock, patch, call
import pygame
from pygame.locals import MOUSEBUTTONDOWN, KEYDOWN, K_ESCAPE
from pygame import Rect, Vector2, K_SPACE, Surface
from pygame.event import Event
from pygame_gui import Controller, Control, ChangeChecker
import logging
from . import logging_tool


@logging_tool.logging_tool
class TestControl(unittest.TestCase):

    def setUp(self):
        self.mock_screen = MagicMock(spec=Surface)
        self.mock_controller = Controller(self.mock_screen)
        self.mock_controller.change_checker = MagicMock(spec=ChangeChecker)
        self.control = Control(self.mock_controller)

    def test_init(self):
        self.assertEqual(self.control.manager, self.mock_controller)
        self.assertTrue(self.control.visible)
        self.assertTrue(self.control.enabled)
        self.assertTrue(self.control.focusable)
        self.assertEqual(self.control.size, Vector2(100, 100))
        self.assertEqual(self.control.position, Vector2(0, 0))
        self.assertEqual(self.control.rect, Rect(Vector2(0, 0), Vector2(100, 100)))
        self.assertEqual(self.mock_controller.change_checker.add_change.call_count, 2)  # type: ignore

    def test_update_rect(self):
        original_rect = self.control.rect
        self.control.size = Vector2(200, 200)
        self.control.update_rect()
        self.assertNotEqual(self.control.rect, original_rect)
        self.assertEqual(
            self.control.rect, Rect(self.control.position, self.control.size)
        )


if __name__ == "__main__":
    unittest.main()
