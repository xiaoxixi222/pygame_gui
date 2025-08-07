import unittest
from unittest.mock import Mock, patch
from enum import Enum, auto
import pygame
from pygame_gui import (
    EventListener,
    EventListenerSignals,
    EVENT_TYPE,
    EVENT_ANSWER_TYPE,
)
import logging


class TestEventListener(unittest.TestCase):
    def setUp(self):
        self.event_listener = EventListener()
        pygame.init()
        pygame.key.set_mods(0)

    def test_add_event_listener(self):
        logging.info("test_add_event_listener:start")
        key_up_event = (EventListenerSignals.SINGLE_KEY_UP, pygame.K_a)
        id = self.event_listener.add_event_listener(key_up_event)
        self.assertIn(key_up_event, self.event_listener.event_listeners_id)
        self.assertEqual(self.event_listener.event_listeners_id[key_up_event], id)

        mouse_click_event = (EventListenerSignals.MOUSE_CLICK_DOWN, 1)
        mouse_id = self.event_listener.add_event_listener(mouse_click_event)
        self.assertIn(mouse_click_event, self.event_listener.event_listeners_id)
        self.assertEqual(
            self.event_listener.event_listeners_id[mouse_click_event], mouse_id
        )
        logging.info("test_add_event_listener:end")

    def test_set_event_listener_result(self):
        logging.info("test_set_event_listener_result:start")
        key_up_event = (EventListenerSignals.SINGLE_KEY_UP, pygame.K_a)
        id = self.event_listener.add_event_listener(key_up_event)
        self.event_listener.set_event_listener_result(id, True)
        self.assertEqual(self.event_listener.get_event_listener_result(id), True)
        with self.assertRaises(ValueError):
            self.event_listener.set_event_listener_result(-1, True)
        with self.assertRaises(ValueError):
            self.event_listener.set_event_listener_result(id + 1, True)
        logging.info("test_set_event_listener_result:end")

    def test_get_event_listener_result(self):
        logging.info("test_get_event_listener_result:start")
        key_up_event = (EventListenerSignals.SINGLE_KEY_UP, pygame.K_a)
        id = self.event_listener.add_event_listener(key_up_event)
        with self.assertRaises(ValueError):
            self.event_listener.get_event_listener_result(-1)
        with self.assertRaises(ValueError):
            self.event_listener.get_event_listener_result(id + 1)
        logging.info("test_get_event_listener_result:end")

    def test_update_event_listener_result_key_up(self):
        logging.info("test_update_event_listener_result_key_up:start")
        key_up_event = (EventListenerSignals.SINGLE_KEY_UP, pygame.K_a)
        id = self.event_listener.add_event_listener(key_up_event)
        event = [pygame.event.Event(pygame.KEYUP, key=pygame.K_a)]
        self.event_listener.update_event_listener_result(event)
        self.assertTrue(self.event_listener.get_event_listener_result(id))
        logging.info("test_update_event_listener_result_key_up:end")

    def test_update_event_listener_result_key_down(self):
        logging.info("test_update_event_listener_result_key_down:start")
        key_down_event = (EventListenerSignals.SINGLE_KEY_DOWN, pygame.K_a)
        id = self.event_listener.add_event_listener(key_down_event)
        event = [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_a)]
        self.event_listener.update_event_listener_result(event)
        self.assertTrue(self.event_listener.get_event_listener_result(id))
        logging.info("test_update_event_listener_result_key_down:end")

    def test_update_event_listener_result_key_pressed(self):
        logging.info("test_update_event_listener_result_key_pressed:start")
        key_pressed_event = (EventListenerSignals.SINGLE_KEY_PRESSED, pygame.K_a)
        id = self.event_listener.add_event_listener(key_pressed_event)
        with patch("pygame.key.get_pressed", return_value=[False] * 256):
            event = [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_a)]
            self.event_listener.update_event_listener_result(event)
            self.assertFalse(self.event_listener.get_event_listener_result(id))

        with patch(
            "pygame.key.get_pressed",
            return_value=[True if i == pygame.K_a else False for i in range(256)],
        ):
            event = []
            self.event_listener.update_event_listener_result(event)
            self.assertTrue(self.event_listener.get_event_listener_result(id))
        logging.info("test_update_event_listener_result_key_pressed:end")

    def test_update_event_listener_result_combination_key(self):
        logging.info("test_update_event_listener_result_combination_key:start")
        combination_key_event = (
            EventListenerSignals.COMBINATION_KEY,
            (pygame.K_a, pygame.K_b),
        )
        id = self.event_listener.add_event_listener(combination_key_event)
        with patch(
            "pygame.key.get_pressed",
            return_value=[
                True if i in (pygame.K_a, pygame.K_b) else False for i in range(256)
            ],
        ):
            event = []
            self.event_listener.update_event_listener_result(event)
            self.assertTrue(self.event_listener.get_event_listener_result(id))
        logging.info("test_update_event_listener_result_combination_key:end")

    def test_update_event_listener_result_mouse_click_up(self):
        logging.info("test_update_event_listener_result_mouse_click_up:start")
        mouse_click_up_event = (EventListenerSignals.MOUSE_CLICK_UP, 1)
        id = self.event_listener.add_event_listener(mouse_click_up_event)
        event = [pygame.event.Event(pygame.MOUSEBUTTONUP, button=1)]
        self.event_listener.update_event_listener_result(event)
        self.assertTrue(self.event_listener.get_event_listener_result(id))
        logging.info("test_update_event_listener_result_mouse_click_up:end")

    def test_update_event_listener_result_mouse_click_down(self):
        logging.info("test_update_event_listener_result_mouse_click_down:start")
        mouse_click_down_event = (EventListenerSignals.MOUSE_CLICK_DOWN, 1)
        id = self.event_listener.add_event_listener(mouse_click_down_event)
        event = [pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1)]
        self.event_listener.update_event_listener_result(event)
        self.assertTrue(self.event_listener.get_event_listener_result(id))
        logging.info("test_update_event_listener_result_mouse_click_down:end")

    def test_update_event_listener_result_mouse_click_pressed(self):
        logging.info("test_update_event_listener_result_mouse_click_pressed:start")
        mouse_click_pressed_event = (EventListenerSignals.MOUSE_CLICK_PRESSED, 0)
        id = self.event_listener.add_event_listener(mouse_click_pressed_event)
        with patch(
            "pygame.mouse.get_pressed", return_value=[False, False, False, False, False]
        ):
            event = [pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=0)]
            self.event_listener.update_event_listener_result(event)
            self.assertFalse(self.event_listener.get_event_listener_result(id))

        with patch(
            "pygame.mouse.get_pressed", return_value=[True, False, False, False, False]
        ):
            event = []
            self.event_listener.update_event_listener_result(event)
            self.assertTrue(self.event_listener.get_event_listener_result(id))
        logging.info("test_update_event_listener_result_mouse_click_pressed:end")

    def test_update_event_listener_result_any_event(self):
        logging.info("test_update_event_listener_result_any_event:start")
        any_event = (EventListenerSignals.ANY_EVENT, pygame.KEYDOWN)
        id = self.event_listener.add_event_listener(any_event)
        event = [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_a)]
        self.event_listener.update_event_listener_result(event)
        self.assertEqual(self.event_listener.get_event_listener_result(id), event)
        logging.info("test_update_event_listener_result_any_event:end")

    def test_update_event_listener_result_custom_event(self):
        logging.info("test_update_event_listener_result_custom_event:start")
        custom_event = (EventListenerSignals.CUSTOM_EVENT, None)
        id = self.event_listener.add_event_listener(custom_event)
        event = [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_a)]
        self.event_listener.update_event_listener_result(event)
        self.assertEqual(self.event_listener.get_event_listener_result(id), False)
        self.event_listener.set_event_listener_result(id, True)
        self.event_listener.update_event_listener_result(event)
        self.assertEqual(self.event_listener.get_event_listener_result(id), True)
        logging.info("test_update_event_listener_result_custom_event:end")

    def test_update_event_listener_result_parallel(self):
        logging.info("test_update_event_listener_result_parallel:start")
        parallel_event = (
            EventListenerSignals.PARALLEL,
            (
                (EventListenerSignals.SINGLE_KEY_DOWN, pygame.K_a),
                (EventListenerSignals.SINGLE_KEY_DOWN, pygame.K_b),
            ),
        )
        id = self.event_listener.add_event_listener(parallel_event)
        event_a = [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_a)]
        self.event_listener.update_event_listener_result(event_a)
        self.assertFalse(self.event_listener.get_event_listener_result(id))
        event_b = [
            pygame.event.Event(pygame.KEYUP, key=pygame.K_a),
            pygame.event.Event(pygame.KEYDOWN, key=pygame.K_b),
            pygame.event.Event(pygame.KEYDOWN, key=pygame.K_a),
        ]
        self.event_listener.update_event_listener_result(event_b)
        self.assertTrue(self.event_listener.get_event_listener_result(id))
        logging.info("test_update_event_listener_result_parallel:end")

    def test_update_event_listener_result_any(self):
        logging.info("test_update_event_listener_result_any:start")
        any_event = (
            EventListenerSignals.ANY,
            (
                (EventListenerSignals.SINGLE_KEY_DOWN, pygame.K_a),
                (EventListenerSignals.SINGLE_KEY_DOWN, pygame.K_b),
            ),
        )
        id = self.event_listener.add_event_listener(any_event)
        event_a = [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_a)]
        self.event_listener.update_event_listener_result(event_a)
        self.assertTrue(self.event_listener.get_event_listener_result(id))
        self.event_listener = EventListener()
        id = self.event_listener.add_event_listener(any_event)
        event_b = [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_b)]
        self.event_listener.update_event_listener_result(event_b)
        self.assertTrue(self.event_listener.get_event_listener_result(id))
        self.event_listener = EventListener()
        id = self.event_listener.add_event_listener(any_event)
        event_c = [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_c)]
        self.event_listener.update_event_listener_result(event_c)
        self.assertFalse(self.event_listener.get_event_listener_result(id))
        logging.info("test_update_event_listener_result_any:end")

    def test_update_event_listener_result_block_key(self):
        logging.info("test_update_event_listener_result_block_key:start")
        block_key_event1 = (EventListenerSignals.SINGLE_KEY_DOWN, pygame.K_a)
        block_key_event2 = (EventListenerSignals.SINGLE_KEY_DOWN, pygame.K_b)
        self.event_listener.add_event_listener(block_key_event1)
        self.event_listener.add_event_listener(block_key_event2)
        event_a = [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_a)]
        self.event_listener.update_event_listener_result(event_a)
        self.assertEqual(self.event_listener.block_key, [pygame.K_a])
        event_b = [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_b)]
        self.event_listener.update_event_listener_result(event_b)
        self.assertEqual(self.event_listener.block_key, [pygame.K_a, pygame.K_b])
        event_c = [pygame.event.Event(pygame.KEYUP, key=pygame.K_a)]
        self.event_listener.update_event_listener_result(event_c)
        self.assertEqual(self.event_listener.block_key, [pygame.K_b])
        logging.info("test_update_event_listener_result_block_key:end")

    def tearDown(self):
        pygame.quit()


if __name__ == "__main__":
    unittest.main()
