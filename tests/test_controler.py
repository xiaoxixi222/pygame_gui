import unittest, logging
from unittest.mock import MagicMock, patch
from pygame import Surface, Rect, MOUSEBUTTONDOWN, KEYDOWN, K_ESCAPE, Vector2
from pygame.event import Event
import sys, os

sys.path.append(
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
)
from pygame_gui import Controller, Control

logging.basicConfig(
    level=logging.DEBUG,
    filename="example.log",
    filemode="w",
    encoding="utf-8",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


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


class TestController(unittest.TestCase):
    def setUp(self):
        self.screen_mock = MagicMock(spec=Surface)
        self.controller = Controller(self.screen_mock)

    def test_add_control_happy_path(self):
        logging.info("test_add_control_happy_path:start")
        control = ControlMock("test_control", Vector2(0, 0), Vector2(100, 100))
        result = self.controller.add_control(control)
        self.assertTrue(result)
        self.assertEqual(control.id, 0)
        self.assertIn(control, self.controller.get_controls())
        logging.info("test_add_control_happy_path:end")

    def test_add_control_already_exists(self):
        logging.info("test_add_control_already_exists:start")
        control = ControlMock("test_control", Vector2(0, 0), Vector2(100, 100))
        self.controller.add_control(control)
        result = self.controller.add_control(control)
        self.assertFalse(result)
        self.assertIn(control, self.controller.get_controls())
        logging.info("test_add_control_already_exists:end")

    def test_remove_control_happy_path(self):
        logging.info("test_remove_control_happy_path:start")
        control = ControlMock("test_control", Vector2(0, 0), Vector2(100, 100))
        self.controller.add_control(control)
        result = self.controller.remove_control(control)
        self.assertTrue(result)
        self.assertNotIn(control, self.controller.get_controls())
        logging.info("test_remove_control_happy_path:end")

    def test_remove_control_not_found(self):
        logging.info("test_remove_control_not_found:start")
        control = ControlMock("test_control", Vector2(0, 0), Vector2(100, 100))
        result = self.controller.remove_control(control)
        self.assertFalse(result)
        self.assertNotIn(control, self.controller.get_controls())
        logging.info("test_remove_control_not_found:end")

    def test_update_mouse_focus(self):
        logging.info("test_update_mouse_focus:start")
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
        logging.info("test_update_mouse_focus:end")

    def test_update_mouse_outside(self):
        logging.info("test_update_mouse_outside:start")
        control = ControlMock("test_control", Vector2(10, 10), Vector2(20, 20))
        self.controller.add_control(control)

        mouse_event = Event(MOUSEBUTTONDOWN, pos=(40, 40))
        self.controller.update([mouse_event])
        self.assertIsNone(self.controller._Controller__focus_control)  # type: ignore
        logging.info("test_update_mouse_outside:end")

    def test_update_esc_key(self):
        logging.info("test_update_esc_key:start")
        control = ControlMock("test_control", Vector2(10, 10), Vector2(20, 20))
        self.controller.add_control(control)

        mouse_event = Event(MOUSEBUTTONDOWN, pos=(15, 15))
        self.controller.update([mouse_event])
        self.assertEqual(self.controller._Controller__focus_control, control)  # type: ignore

        esc_event = Event(KEYDOWN, key=K_ESCAPE)
        self.controller.update([esc_event])
        self.assertIsNone(self.controller._Controller__focus_control)  # type: ignore
        logging.info("test_update_esc_key:end")

    def test_update_disabled_control(self):
        logging.info("test_update_disabled_control:start")
        control = ControlMock(
            "test_control", Vector2(10, 10), Vector2(20, 20), enabled=False
        )
        self.controller.add_control(control)

        mouse_event = Event(MOUSEBUTTONDOWN, pos=(15, 15))
        self.controller.update([mouse_event])
        self.assertIsNone(self.controller._Controller__focus_control)  # type: ignore
        logging.info("test_update_disabled_control:end")

    def test_update_non_focusable_control(self):
        logging.info("test_update_non_focusable_control:start")
        control = ControlMock(
            "test_control", Vector2(10, 10), Vector2(20, 20), focusable=False
        )
        self.controller.add_control(control)

        mouse_event = Event(MOUSEBUTTONDOWN, pos=(15, 15))
        self.controller.update([mouse_event])
        self.assertIsNone(self.controller._Controller__focus_control)  # type: ignore
        logging.info("test_update_non_focusable_control:end")

    @patch("pygame_gui.control.control.Control.update")
    def test_update_calls_control_update(self, mock_update):
        logging.info("test_update_calls_control_update:start")
        control = ControlMock("test_control", Vector2(10, 10), Vector2(20, 20))
        self.controller.add_control(control)

        mouse_event = Event(MOUSEBUTTONDOWN, pos=(15, 15))
        self.controller.update([mouse_event])
        mock_update.assert_called_once_with([mouse_event], True)
        logging.info("test_update_calls_control_update:end")

    @patch("pygame_gui.control.control.Control.update")
    def test_update_no_focus_calls_control_update(self, mock_update):
        logging.info("test_update_no_focus_calls_control_update:start")
        control = ControlMock("test_control", Vector2(10, 10), Vector2(20, 20))
        self.controller.add_control(control)

        mouse_event = Event(MOUSEBUTTONDOWN, pos=(40, 40))
        self.controller.update([mouse_event])
        mock_update.assert_called_once_with([mouse_event], False)
        logging.info("test_update_no_focus_calls_control_update:end")

    def test_update_no_events(self):
        logging.info("test_update_no_events:start")
        control = ControlMock("test_control", Vector2(10, 10), Vector2(20, 20))
        self.controller.add_control(control)

        self.controller.update([])
        self.assertIsNone(self.controller._Controller__focus_control)  # type: ignore
        logging.info("test_update_no_events:end")


if __name__ == "__main__":
    unittest.main()
