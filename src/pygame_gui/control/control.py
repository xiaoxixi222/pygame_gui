from enum import Enum
import pygame
from pygame.locals import *  # type: ignore
from pygame import Rect, Surface, Vector2, Color
from typing import Any, Callable
import logging


class EventListenerSignals(Enum):
    SINGLE_KEY_UP = 1
    SINGLE_KEY_DOWN = 2
    SINGLE_KEY_PRESSED = 3
    COMBINATION_KEY = 4
    MOUSE_CLICK_UP = 5
    MOUSE_CLICK_DOWN = 6
    MOUSE_CLICK_PRESSED = 7
    ANY_EVENT = 9
    CUSTOM_EVENT = 10
    PARALLEL = 11
    ANY = 12
    NO_CHANGE = 13


EVENT_TYPE = tuple[EventListenerSignals, int | tuple[int,...] | tuple[tuple[EventListenerSignals, tuple|int], tuple[EventListenerSignals, tuple|int]]|None]
EVENT_ANSWER_TYPE = bool | list[pygame.event.Event] | EventListenerSignals


class EventListener:

    def __init__(self):
        self.event_listeners_id: dict[EVENT_TYPE, int] = {}
        self.event_listeners_result: list[EVENT_ANSWER_TYPE] = []
        self.__counter: int = 0
        self.event: list[pygame.event.Event] = []
        self.block_key: list[int] = []

    def add_event_listener(self, event_type: EVENT_TYPE):
        if event_type in self.event_listeners_id:
            logging.debug(
                f"event listener add event_type:{event_type}, id:{self.event_listeners_id[event_type]}"
            )
            return self.event_listeners_id[event_type]
        else:
            self.event_listeners_id[event_type] = self.__counter
            logging.debug(
                f"event listener add event_type:{event_type}, id:{self.event_listeners_id[event_type]}"
            )
            self.__counter += 1
            self.event_listeners_result.append(False)
            return self.event_listeners_id[event_type]

    def set_event_listener_result(self, event_listener_id: int, result: Any):
        if event_listener_id < 0 or event_listener_id >= self.__counter:
            logging.error(f"event listener id out of range: id:{event_listener_id}")
            raise ValueError("event listener id out of range")
        logging.debug(
            f"event listener set result: id:{event_listener_id}, result:{result}"
        )
        self.event_listeners_result[event_listener_id] = result

    def get_event_listener_result(self, event_listener_id: int):
        if event_listener_id < 0 or event_listener_id >= self.__counter:
            logging.error(f"event listener id out of range: id:{event_listener_id}")
            raise ValueError("event listener id out of range")
        logging.debug(
            f"event listener get result: id:{event_listener_id}, result:{self.event_listeners_result[event_listener_id]}"
        )
        return self.event_listeners_result[event_listener_id]

    def update_event_listener_result(self, event: list[pygame.event.Event]):
        self.__mouse_up: list[int] = []
        self.__mouse_down: list[int] = []
        self.__key_up: list[int] = []
        self.__key_down: list[int] = []
        self.event_type: dict[int, list[pygame.event.Event]] = {}
        self.event = event
        for e in event:
            if e.type not in self.event_type:
                self.event_type[e.type] = []
            self.event_type[e.type].append(e)
            if e.type == MOUSEBUTTONUP:
                self.__mouse_up.append(e.button)
            elif e.type == MOUSEBUTTONDOWN:
                self.__mouse_down.append(e.button)
            elif e.type == KEYUP:
                self.__key_up.append(e.key)
                if e.key in self.block_key:
                    self.block_key.remove(e.key)
            elif e.type == KEYDOWN:
                self.__key_down.append(e.key)
        logging.debug(
            f"event listener update event: {self.event}, mouse_up: {self.__mouse_up}, mouse_down: {self.__mouse_down}, key_up: {self.__key_up}, key_down: {self.__key_down}, event_type: {self.event_type}, block_key: {self.block_key}"
        )
        for event_type in self.event_listeners_id:
            ans = self.check_event_listener(event_type)
            if ans != EventListenerSignals.NO_CHANGE:
                self.event_listeners_result[self.event_listeners_id[event_type]] = ans

    def check_event_listener(self, event_type: EVENT_TYPE) -> EVENT_ANSWER_TYPE:
        answer: EVENT_ANSWER_TYPE = False
        if event_type[0] == EventListenerSignals.SINGLE_KEY_UP:
            if event_type[1] in self.__key_up and event_type[1] not in self.block_key:
                answer = True
                self.block_key.append(event_type[1])
        elif event_type[0] == EventListenerSignals.SINGLE_KEY_DOWN:
            if event_type[1] in self.__key_down and event_type[1] not in self.block_key:
                answer = True
                self.block_key.append(event_type[1])
        elif event_type[0] == EventListenerSignals.SINGLE_KEY_PRESSED:
            if pygame.key.get_pressed()[event_type[1]] and event_type[1] not in self.block_key:  # type: ignore
                answer = True
                self.block_key.append(event_type[1])  # type: ignore
        elif event_type[0] == EventListenerSignals.COMBINATION_KEY:
            if all(pygame.key.get_pressed()[key] for key in event_type[1]):  # type: ignore
                answer = True
                self.block_key.extend(event_type[1])  # type: ignore
        elif event_type[0] == EventListenerSignals.MOUSE_CLICK_UP:
            if event_type[1] in self.__mouse_up:
                answer = True
        elif event_type[0] == EventListenerSignals.MOUSE_CLICK_DOWN:
            if event_type[1] in self.__mouse_down:
                answer = True
        elif event_type[0] == EventListenerSignals.MOUSE_CLICK_PRESSED:
            if pygame.mouse.get_pressed()[event_type[1]]:  # type: ignore
                answer = True
        elif event_type[0] == EventListenerSignals.ANY_EVENT:
            if event_type[1] in self.event_type:
                answer = self.event_type[event_type[1]]
        elif event_type[0] == EventListenerSignals.CUSTOM_EVENT:
            answer = EventListenerSignals.NO_CHANGE
        elif event_type[0] == EventListenerSignals.PARALLEL:
            logging.debug(f"event listener check parallel event_type1:{event_type[1][0]}, event_type2:{event_type[1][1]}")  # type: ignore
            answer1: bool | list[Event] = self.check_event_listener(event_type[1][0])  # type: ignore
            answer2: bool | list[Event] = self.check_event_listener(event_type[1][1])  # type: ignore
            logging.debug(
                f"event listener check parallel answer1:{answer1}, answer2:{answer2}"
            )
            if answer1 is not False and answer2 is not False:
                answer = True
        elif event_type[0] == EventListenerSignals.ANY:
            logging.debug(f"event listener check any event_type1:{event_type[1][0]}, event_type2:{event_type[1][1]}")  # type: ignore
            answer1: bool | list[Event] = self.check_event_listener(event_type[1][0])  # type: ignore
            answer2: bool | list[Event] = self.check_event_listener(event_type[1][1])  # type: ignore
            logging.debug(
                f"event listener check any answer1:{answer1}, answer2:{answer2}"
            )
            if answer1 is not False or answer2 is not False:
                answer = True

        logging.debug(f"event listener check event_type:{event_type}, answer:{answer}")
        return answer


class ChangeChecker:
    def __init__(self):
        self.change: list[tuple[Any, Any, Callable[[Any, Any]]]] = (
            []
        )  # [(obj, attr, func)]
        self.old_values: dict[tuple[Any, Any, Callable[[Any, Any]]], Any] = (
            {}
        )  # {(obj, attr, func): old_value}

    def check(self):
        for obj, attr, func in self.change:
            old_value = self.old_values.get((obj, attr, func), None)
            new_value = getattr(obj, attr)
            if old_value != new_value:
                func(new_value, old_value)
                self.old_values[(obj, attr, func)] = new_value
                logging.debug(
                    f"change checker: check change: {obj}, {attr}, {func}, {new_value}, {old_value}, change: {self.change}, old_values: {self.old_values}"
                )

    def add_change(self, obj: Any, attr: str, func: Callable[[Any, Any], None]) -> None:
        if (obj, attr, func) in self.change:
            logging.warning(
                f"change checker: already has change: {obj}, {attr}, {func}, change: {self.change}, old_values: {self.old_values}"
            )
            return
        self.change.append((obj, attr, func))
        self.old_values[(obj, attr, func)] = getattr(obj, attr)
        logging.debug(
            f"change checker: add change: {obj}, {attr}, {func}, {getattr(obj, attr)}, change: {self.change}, old_values: {self.old_values}"
        )

    def remove_change(
        self, obj: Any, attr: str, func: Callable[[Any, Any], None]
    ) -> None:
        if (obj, attr, func) not in self.change:
            logging.warning(
                f"change checker: not in change: {obj}, {attr}, {func}, change: {self.change}, old_values: {self.old_values}"
            )
            return
        self.change.remove((obj, attr, func))
        self.old_values.pop((obj, attr, func), None)
        logging.debug(
            f"change checker: remove change: {obj}, {attr}, {func}, change: {self.change}, old_values: {self.old_values}"
        )


class Controller:
    """
    控制器类，用于管理和更新控制对象。
    """

    def __init__(self, screen: Surface) -> None:
        """
        初始化 Controller 类
        """
        self.__controls: list[Control] = []
        self.__focus_control: Control | None = None
        self.screen: Surface = screen
        self.change_checker = ChangeChecker()
        self.__id_counter: int = 0

    def update(self, events: list[pygame.event.Event]) -> None:
        """
        更新控制器中的所有控制对象。

        :param events: 包含 pygame 事件的列表。
        """
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                for control in self.__controls:
                    if (
                        control.enabled
                        and control.focusable
                        and control.rect.collidepoint(event.pos)
                    ):
                        self.__focus_control = control
                        logging.debug(
                            f"controller: mouse focus control: {self.__focus_control.name}{self.__focus_control.id}"
                        )
                        break
                else:
                    self.__focus_control = None
                    logging.debug("controller: mouse lost focus")
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.__focus_control = None
                    logging.debug("controller: esc lost focus")
        self.change_checker.check()
        for control in self.__controls:
            if control.enabled:
                control.update(events, self.__focus_control == control)

    def add_control(self, control: "Control") -> bool:
        """
        添加一个控制对象到控制器中。

        :param control: 要添加的控制对象。
        :return: 如果控制对象已存在返回 False，否则返回 True。
        """
        if control in self.__controls:
            logging.warning(
                f"controller: control already exists: {control.name}{control.id}"
            )
            return False
        self.__controls.append(control)
        logging.debug(
            f"controller: add control: {control.name} old_id: {control.id} new_id: {self.__id_counter}"
        )
        control.id = self.__id_counter
        self.__id_counter += 1
        return True

    def remove_control(self, control: "Control") -> bool:
        """
        从控制器中移除一个控制对象。

        :param control: 要移除的控制对象。
        :return: 如果控制对象不存在返回 False，否则返回 True。
        """
        if control not in self.__controls:
            logging.warning(
                f"controller: control not found: {control.name}{control.id}"
            )
            return False
        self.__controls.remove(control)
        logging.debug(f"controller: remove control: {control.name}{control.id}")
        return True

    def get_controls(self) -> list["Control"]:
        """
        获取控制器中所有控制对象的副本。

        :return: 控制对象列表的副本。
        """
        return self.__controls.copy()


class Control:
    """
    控制对象基类，具体的控制对象需要继承这个类并实现相应的功能。
    """

    def __init__(self, manager: Controller) -> None:
        """
        初始化 Control 类。

        :param manager: 管理该控制对象的控制器。
        """
        self.manager: Controller = manager
        self.visible: bool = True
        self.enabled: bool = True
        self.focusable: bool = True
        self.size: Vector2 = Vector2(100, 100)
        self.position: Vector2 = Vector2(0, 0)
        self.rect: pygame.Rect = Rect(self.position, self.size)
        self.manager.change_checker.add_change(
            self, "size", lambda new, old: self.update_rect()
        )
        self.manager.change_checker.add_change(
            self, "position", lambda new, old: self.update_rect()
        )
        self.id: int = id(self)
        self.name: str = "control"

    def update_rect(self) -> None:
        """
        更新控制对象的矩形。
        """
        self.rect = Rect(self.position, self.size)
        logging.debug(f"{self.name}{self.id}: update rect: {self.rect}")

    def update(self, events: list[pygame.event.Event], focus: bool) -> None:
        """
        更新控制对象。

        :param events: 包含 pygame 事件的列表。
        :param focus: 是否被选中。
        """
        ...
