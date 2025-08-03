import pygame
from pygame.locals import *  # type: ignore
from pygame import Rect, Surface, Vector2, Color
from typing import Any, Callable
import logging
class ChangeChecker:
    def __init__(self):
        self.change:list[tuple[Any, Any, Callable[[Any, Any]]]] = []# [(obj, attr, func)]
        self.old_values:dict[tuple[Any, Any, Callable[[Any, Any]]], Any] = {}# {(obj, attr, func): old_value}
    def check(self):
        for obj, attr, func in self.change:
            old_value = self.old_values.get((obj, attr, func), None)
            new_value = getattr(obj, attr)
            if old_value!= new_value:
                func(old_value, new_value)
                self.old_values[(obj, attr, func)] = new_value
                logging.debug(f"check change: {obj}, {attr}, {func}, {old_value}, {new_value}, change: {self.change}, old_values: {self.old_values}")
    def add_change(self, obj: Any, attr: str, func: Callable[[Any, Any], None]) -> None:
        self.change.append((obj, attr, func))
        self.old_values[(obj, attr, func)] = getattr(obj, attr)
        logging.debug(f"add change: {obj}, {attr}, {func}, {getattr(obj, attr)}, change: {self.change}, old_values: {self.old_values}")
    def remove_change(self, obj: Any, attr: str, func: Callable[[Any, Any], None]) -> None:
        self.change.remove((obj, attr, func))
        self.old_values.pop((obj, attr, func), None)
        logging.debug(f"remove change: {obj}, {attr}, {func}, change: {self.change}, old_values: {self.old_values}")
class Controller:
    """
    控制器类，用于管理和更新控制对象。
    """

    def __init__(self,screen:Surface) -> None:
        """
        初始化 Controller 类
        """
        self.__controls: list[Control] = []
        self.__focus_control: Control | None = None
        self.screen: Surface=screen
        self.change_checker = ChangeChecker()

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
                        logging.debug(f"mouse focus control: {self.__focus_control}")
                        break
                else:
                    self.__focus_control = None
                    logging.debug("mouse lost focus")
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.__focus_control = None
                    logging.debug("esc lost focus")
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
            return False
        self.__controls.append(control)
        return True

    def remove_control(self, control: "Control") -> bool:
        """
        从控制器中移除一个控制对象。

        :param control: 要移除的控制对象。
        :return: 如果控制对象不存在返回 False，否则返回 True。
        """
        if control not in self.__controls:
            return False
        self.__controls.remove(control)
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
        self.manager.change_checker.add_change(self, "size", lambda new, old: self.update_rect())

    def update_rect(self) -> None:
        """
        更新控制对象的矩形。
        """
        self.rect = Rect(self.position, self.size)
        logging.debug(f"update rect: {self.rect}")

    def update(self, events: list[pygame.event.Event], focus: bool) -> None:
        """
        更新控制对象。

        :param events: 包含 pygame 事件的列表。
        :param focus: 是否被选中。
        """
        ...
