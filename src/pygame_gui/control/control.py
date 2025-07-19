import pygame
from pygame.locals import *  # type: ignore
from pygame import Rect, Surface, Vector2, Color


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
                        break
                else:
                    self.__focus_control = None
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.__focus_control = None
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

    def update_rect(self) -> None:
        """
        更新控制对象的矩形。
        """
        self.rect = Rect(self.position, self.size)

    def update(self, events: list[pygame.event.Event], focus: bool) -> None:
        """
        更新控制对象。

        :param events: 包含 pygame 事件的列表。
        :param focus: 是否被选中。
        """
        ...


class Entry(Control):
    """
    输入框控件。
    """

    def __init__(
        self, manager: Controller, font: pygame.font.Font | None = None
    ) -> None:
        """
        初始化 Entry 类。

        :param manager: 管理该控件的控制器。
        :param font: 字体。
        """
        super().__init__(manager)
        self.text: str = ""
        self.font: pygame.font.Font | None = font
        self.background_color: pygame.Color = Color(255,255,255)
        self.text_color: pygame.Color = Color(0,0,0)
        self.course_color: pygame.Color = Color(0, 0, 0)
        self.course: int = 0#0a1a2a3
        self.__old_focus: bool = False
        self.__offset: int = 0
        self.text_surface: list[Surface] = []
        self.text_long:list[int] = []
        self.update_rect()

    def update(self, events: list[pygame.event.Event], focus: bool) -> None:
        """
        更新 Entry 控件。

        :param events: 包含 pygame 事件的列表。
        :param focus: 是否被选中。
        """
        if focus and not self.__old_focus:
            self.course = len(self.text)
        self.__old_focus = focus
        if focus:
            for event in events:
                if event.type == KEYDOWN:
                    if event.key == K_BACKSPACE:
                        if self.course > 0:
                            self.text = self.text[:self.course-1] + self.text[self.course:]
                            self.course -= 1
                            self.new_font()
                    elif event.key == K_RIGHT:
                        self.course = min(self.course + 1, len(self.text))
                    elif event.key == K_LEFT:
                        self.course = max(self.course - 1, 0)
                if event.type == TEXTINPUT:
                    self.text = self.text[:self.course] + event.text + self.text[self.course:]
                    self.course += len(event.text)
                    self.new_font()
                if event.type == MOUSEBUTTONDOWN:
                    pos: Vector2 = Vector2(event.pos[0] - self.position[0]-self.size[0]*0.1, event.pos[1] - self.position[1]-self.size[1]*0.1)
                    for i in range(0, len(self.text_long)-1):
                        if self.text_long[i]<=pos[0]<self.text_long[i+1]:
                            self.course = i
                            break
                    else:
                        if pos[0]>self.text_long[-1]:
                            self.course = len(self.text)
                        if pos[0]<0:
                            self.course = 0
            self.manager.screen.fill(self.background_color, self.rect)
            if self.font:
                text_surface = Surface(self.size*0.8, SRCALPHA)
                for i in range(0, len(self.text_surface)+1):
                    if i!=len(self.text_surface):
                        text_surface.blit(self.text_surface[i], (Vector2(self.text_long[i], 0)))
                    if i==self.course:
                        pygame.draw.line(text_surface, self.course_color, Vector2(self.text_long[i], 0), Vector2(self.text_long[i], self.size[1]*0.8), 1)
                self.manager.screen.blit(text_surface, (self.position + self.size*0.1))
        else:
            self.manager.screen.fill(self.background_color, self.rect)
            if self.font:
                text_surface = Surface(self.size*0.8, SRCALPHA)
                for i in range(0, len(self.text_surface)+1):
                    if i!=len(self.text_surface):
                        text_surface.blit(self.text_surface[i], (Vector2(self.text_long[i], 0)))
                    if i==self.course:
                        pygame.draw.line(text_surface, self.course_color, Vector2(self.text_long[i], 0), Vector2(self.text_long[i], self.size[1]*0.8), 1)
                self.manager.screen.blit(text_surface, (self.position + self.size*0.1))
    def new_font(self):
        self.text_surface = []
        self.text_long = [0]
        long = 0
        if self.font:
            for i in range(0, len(self.text)):
                self.text_surface.append(self.font.render(self.text[i], True, self.text_color))
                long += self.text_surface[i].get_width()
                self.text_long.append(long)