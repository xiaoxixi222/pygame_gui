import unittest
from unittest.mock import MagicMock, patch
import pygame
from pygame.locals import (
    KEYDOWN,
    TEXTINPUT,
    MOUSEBUTTONDOWN,
    K_BACKSPACE,
    K_RIGHT,
    K_LEFT,
    K_LSHIFT
)
from pygame import Vector2
pygame.init()
import sys, os
sys.path.append(
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
)
from pygame_gui.control.entry import Entry
import logging
class get_pressed_mock:
    def __init__(self, key:dict[int, bool]):
        self.key = key
    def __getitem__(self, key:int):
        return self.key.get(key, False)
class TestEntry(unittest.TestCase):
    def setUp(self):
        self.manager = MagicMock()
        self.font = pygame.font.Font(None, 20)
        self.entry = Entry(self.manager, self.font)

    def test_init(self):
        logging.info("test_init:start")
        self.assertEqual(self.entry.name, "entry")
        self.assertEqual(self.entry.text, "")
        self.assertEqual(self.entry.font, self.font)
        self.assertEqual(self.entry.background_color, pygame.Color(255, 255, 255))
        self.assertEqual(self.entry.text_color, pygame.Color(0, 0, 0))
        self.assertEqual(self.entry.course_color, pygame.Color(0, 0, 0))
        self.assertEqual(self.entry.course, 0)
        self.assertFalse(self.entry.chosen)
        self.assertEqual(self.entry.chosen_color, pygame.Color(0, 0, 255))
        self.assertEqual(self.entry.chosen_font_color, pygame.Color(255, 255, 255))
        self.assertIsNone(self.entry.chosen_start)
        self.assertIsNone(self.entry.chosen_end)
        self.assertEqual(self.entry._Entry__offset, 0) # type: ignore
        self.assertFalse(self.entry._Entry__old_focus) # type: ignore
        self.assertEqual(self.entry.text_surface, [])
        self.assertEqual(self.entry.text_long, [0])
        logging.info("test_init:end")

    @patch("pygame.key.get_pressed")
    def test_course_change_with_shift(self, mock_get_pressed):
        logging.info("test_course_change_with_shift:start")
        mock_get_pressed.return_value = get_pressed_mock({K_LSHIFT: True})
        self.entry.course_change(2, 1)
        self.assertTrue(self.entry.chosen)
        self.assertEqual(self.entry.chosen_start, 1)
        self.assertEqual(self.entry.chosen_end, 2)

        self.entry.chosen = True
        self.entry.chosen_start = 1
        self.entry.chosen_end = 2
        self.entry.course_change(3, 2)
        self.assertTrue(self.entry.chosen)
        self.assertEqual(self.entry.chosen_start, 1)
        self.assertEqual(self.entry.chosen_end, 3)
        logging.info("test_course_change_with_shift:end")

    @patch("pygame.key.get_pressed")
    def test_course_change_without_shift(self, mock_get_pressed):
        logging.info("test_course_change_without_shift:start")
        mock_get_pressed.return_value = get_pressed_mock({})
        self.entry.course_change(2, 1)
        self.assertFalse(self.entry.chosen)
        self.assertIsNone(self.entry.chosen_start)
        self.assertIsNone(self.entry.chosen_end)
        logging.info("test_course_change_without_shift:end")

    def test_focus_change_when_focused(self):
        logging.info("test_focus_change_when_focused:start")
        self.entry.focus_change(True)
        self.assertFalse(self.entry.chosen)
        self.assertEqual(self.entry.course, len(self.entry.text))
        logging.info("test_focus_change_when_focused:end")

    def test_focus_change_when_not_focused(self):
        logging.info("test_focus_change_when_not_focused:start")
        self.entry.focus_change(False)
        self.assertEqual(self.entry._Entry__old_focus, False) # type: ignore
        logging.info("test_focus_change_when_not_focused:end")
    @patch("pygame_gui.control.entry.Entry.new_font")
    def test_text_change(self, mock_new_font):
        logging.info("test_text_change:start")
        self.entry.text = "old"
        self.entry.text_change("new", "old")
        mock_new_font.assert_called_once()
        logging.info("test_text_change:end")

    def test_update_with_backspace_events(self):
        logging.info("test_update_with_backspace_events:start")
        event = pygame.event.Event(KEYDOWN, key=K_BACKSPACE)
        self.entry.text = "abc"
        self.entry._Entry__old_focus = True # type: ignore
        self.entry.course = 1
        self.entry.update([event], True)
        self.assertEqual(self.entry.text, "bc")
        self.assertEqual(self.entry.course, 0)
        self.entry.update([event], True)
        self.assertEqual(self.entry.text, "bc")
        self.assertEqual(self.entry.course, 0)
        logging.info("test_update_with_backspace_events:end")

    def test_update_with_backspace_events_when_chosen(self):
        logging.info("test_update_with_backspace_events_when_chosen:start")
        event = pygame.event.Event(KEYDOWN, key=K_BACKSPACE)
        self.entry.text = "1234567890"
        self.entry.course = 5
        self.entry.chosen = True
        self.entry.chosen_start = 1
        self.entry.chosen_end = 5
        self.entry._Entry__old_focus = True # type: ignore
        self.entry.update([event], True)
        self.assertEqual(self.entry.text, "167890")
        self.assertEqual(self.entry.course, 1)
        self.assertFalse(self.entry.chosen)
        self.assertIsNone(self.entry.chosen_start)
        self.assertIsNone(self.entry.chosen_end)
        self.entry.text = "1234567890"
        self.entry.course = 1
        self.entry.chosen = True
        self.entry.chosen_start = 5
        self.entry.chosen_end = 1
        self.entry.update([event], True)
        self.assertEqual(self.entry.text, "167890")
        self.assertEqual(self.entry.course, 1)
        self.assertFalse(self.entry.chosen)
        self.assertIsNone(self.entry.chosen_start)
        self.assertIsNone(self.entry.chosen_end)
        logging.info("test_update_with_backspace_events_when_chosen:end")

    def test_update_with_right_events(self):
        logging.info("test_update_with_right_events:start")
        event = pygame.event.Event(KEYDOWN, key=K_RIGHT)
        self.entry.text = "ab"
        self.entry.course = 1
        self.entry._Entry__old_focus = True # type: ignore
        self.entry.update([event], True)
        self.assertEqual(self.entry.course, 2)
        self.entry.update([event], True)
        self.assertEqual(self.entry.course, 2)
        logging.info("test_update_with_right_events:end")

    def test_update_with_left_events(self):
        logging.info("test_update_with_left_events:start")
        event = pygame.event.Event(KEYDOWN, key=K_LEFT)
        self.entry.text = "abc"
        self.entry.course = 1
        self.entry._Entry__old_focus = True # type: ignore
        self.entry.update([event], True)
        self.assertEqual(self.entry.course, 0)
        self.entry.update([event], True)
        self.assertEqual(self.entry.course, 0)
        logging.info("test_update_with_left_events:end")

    def test_update_with_textinput_event(self):
        logging.info("test_update_with_textinput_event:start")
        event = pygame.event.Event(TEXTINPUT, text="x")
        self.entry.text = "abc"
        self.entry.course = 1
        self.entry._Entry__old_focus = True # type: ignore
        self.entry.update([event], True)
        self.assertEqual(self.entry.text, "axbc")
        self.assertEqual(self.entry.course, 2)
        logging.info("test_update_with_textinput_event:end")

    def test_update_with_mousebuttondown_event(self):
        logging.info("test_update_with_mousebuttondown_event:start")
        event = pygame.event.Event(MOUSEBUTTONDOWN, pos=(20, 10))
        self.entry.position = Vector2(0, 0)
        self.entry.size = Vector2(100, 100)
        self.entry.text = "abcd"
        self.entry.text_long = [0, 10, 20, 30]
        self.entry.update([event], True)
        self.assertEqual(self.entry.course, 1)

        event = pygame.event.Event(MOUSEBUTTONDOWN, pos=(100, 10))
        self.entry.update([event], True)
        self.assertEqual(self.entry.course, 4)

        event = pygame.event.Event(MOUSEBUTTONDOWN, pos=(-10, 10))
        self.entry.update([event], True)
        self.assertEqual(self.entry.course, 0)
        logging.info("test_update_with_mousebuttondown_event:end")

    def test_new_font(self):
        logging.info("test_new_font:start")
        self.entry.text = "abc"
        self.entry.new_font()
        self.assertEqual(len(self.entry.text_surface), 3)
        self.assertEqual(len(self.entry.text_long), 4)
        logging.info("test_new_font:end")


if __name__ == "__main__":
    unittest.main()
