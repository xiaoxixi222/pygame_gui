import unittest, logging
from unittest.mock import MagicMock, patch
from pygame import Surface, Rect, MOUSEBUTTONDOWN, KEYDOWN, K_ESCAPE, Vector2
from pygame.event import Event
from pygame_gui import Controller, Control
from . import logging_tool


class ControlMock(Control):
    def __init__(self, name, position, size, enabled=True, focusable=True):
        super().__init__(MagicMock())
        self.name = name
        self.position = position
        self.size = size
        self.enabled = enabled
        self.focusable = focusable
        self.update_rect()

    def update(self, events, focus):
        super().update(events, focus)
        self.focus = focus


@logging_tool.logging_tool
class TestController(unittest.TestCase):
    def setUp(self):
        self.screen_mock = MagicMock(spec=Surface)
        self.controller = Controller(self.screen_mock)

    def test_add_control_happy_path(self):
        control = ControlMock("test_control", Vector2(0, 0), Vector2(100, 100))
        result = self.controller.add_control(control)
        self.assertTrue(result)
        self.assertEqual(control.id, 0)
        self.assertIn(control, self.controller.get_controls())

    def test_add_control_already_exists(self):
        control = ControlMock("test_control", Vector2(0, 0), Vector2(100, 100))
        self.controller.add_control(control)
        result = self.controller.add_control(control)
        self.assertFalse(result)
        self.assertIn(control, self.controller.get_controls())

    def test_remove_control_happy_path(self):
        control = ControlMock("test_control", Vector2(0, 0), Vector2(100, 100))
        self.controller.add_control(control)
        result = self.controller.remove_control(control)
        self.assertTrue(result)
        self.assertNotIn(control, self.controller.get_controls())

    def test_remove_control_not_found(self):
        control = ControlMock("test_control", Vector2(0, 0), Vector2(100, 100))
        result = self.controller.remove_control(control)
        self.assertFalse(result)
        self.assertNotIn(control, self.controller.get_controls())

    def test_update_mouse_focus(self):
        control1 = ControlMock("test_control1", Vector2(10, 10), Vector2(20, 20))
        control2 = ControlMock("test_control2", Vector2(30, 30), Vector2(20, 20))
        self.controller.add_control(control1)
        self.controller.add_control(control2)

        mouse_event = Event(MOUSEBUTTONDOWN, pos=(15, 15))
        self.controller.update([mouse_event])
        self.assertEqual(self.controller._Controller__focus_control, control1)  # type: ignore

        mouse_event = Event(MOUSEBUTTONDOWN, pos=(45, 45))
        self.controller.update([mouse_event])
        self.assertEqual(self.controller._Controller__focus_control, control2)  # type: ignore

    def test_update_mouse_outside(self):
        control = ControlMock("test_control", Vector2(10, 10), Vector2(20, 20))
        self.controller.add_control(control)

        mouse_event = Event(MOUSEBUTTONDOWN, pos=(40, 40))
        self.controller.update([mouse_event])
        self.assertIsNone(self.controller._Controller__focus_control)  # type: ignore

    def test_update_esc_key(self):
        control = ControlMock("test_control", Vector2(10, 10), Vector2(20, 20))
        self.controller.add_control(control)

        mouse_event = Event(MOUSEBUTTONDOWN, pos=(15, 15))
        self.controller.update([mouse_event])
        self.assertEqual(self.controller._Controller__focus_control, control)  # type: ignore

        esc_event = Event(KEYDOWN, key=K_ESCAPE)
        self.controller.update([esc_event])
        self.assertIsNone(self.controller._Controller__focus_control)  # type: ignore

    def test_update_disabled_control(self):
        control = ControlMock(
            "test_control", Vector2(10, 10), Vector2(20, 20), enabled=False
        )
        self.controller.add_control(control)

        mouse_event = Event(MOUSEBUTTONDOWN, pos=(15, 15))
        self.controller.update([mouse_event])
        self.assertIsNone(self.controller._Controller__focus_control)  # type: ignore

    def test_update_non_focusable_control(self):
        control = ControlMock(
            "test_control", Vector2(10, 10), Vector2(20, 20), focusable=False
        )
        self.controller.add_control(control)

        mouse_event = Event(MOUSEBUTTONDOWN, pos=(15, 15))
        self.controller.update([mouse_event])
        self.assertIsNone(self.controller._Controller__focus_control)  # type: ignore

    @patch("pygame_gui.control.control.Control.update")
    def test_update_calls_control_update(self, mock_update):
        control = ControlMock("test_control", Vector2(10, 10), Vector2(20, 20))
        self.controller.add_control(control)

        mouse_event = Event(MOUSEBUTTONDOWN, pos=(15, 15))
        self.controller.update([mouse_event])
        mock_update.assert_called_once_with([mouse_event], True)

    @patch("pygame_gui.control.control.Control.update")
    def test_update_no_focus_calls_control_update(self, mock_update):
        control = ControlMock("test_control", Vector2(10, 10), Vector2(20, 20))
        self.controller.add_control(control)

        mouse_event = Event(MOUSEBUTTONDOWN, pos=(40, 40))
        self.controller.update([mouse_event])
        mock_update.assert_called_once_with([mouse_event], False)

    def test_update_no_events(self):
        control = ControlMock("test_control", Vector2(10, 10), Vector2(20, 20))
        self.controller.add_control(control)

        self.controller.update([])
        self.assertIsNone(self.controller._Controller__focus_control)  # type: ignore


if __name__ == "__main__":
    unittest.main()
