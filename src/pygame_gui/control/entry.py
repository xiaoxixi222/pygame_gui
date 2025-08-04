import logging
from .control import Control , Controller
import pygame
from pygame.locals import KEYDOWN, TEXTINPUT, MOUSEBUTTONDOWN, K_BACKSPACE, K_RIGHT, K_LEFT, SRCALPHA, K_LSHIFT, K_RSHIFT
from pygame import Rect, Surface, Vector2, Color

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
        self.name: str = "entry"
        self.text: str = ""
        self.font: pygame.font.Font | None = font
        self.background_color: pygame.Color = Color(255,255,255)
        self.text_color: pygame.Color = Color(0,0,0)
        self.course_color: pygame.Color = Color(0, 0, 0)
        self.course: int = 0#0a1a2a3
        self.chosen: bool = False
        self.chosen_color: pygame.Color = Color(0,0,255)
        self.chosen_font_color: pygame.Color = Color(255,255,255)
        self.chosen_start: int|None = None
        self.chosen_end: int|None = None
        self.__offset: int = 0
        self.__old_focus: bool = False
        self.text_surface: list[Surface] = []
        self.text_long:list[int] = []
        self.update_rect()
        self.manager.change_checker.add_change(self, "text", self.text_change)
        self.manager.change_checker.add_change(self, "font", lambda new, old: self.new_font())
        self.manager.change_checker.add_change(self, "course", self.course_change)
    def course_change(self,new:int, old:int) -> None:
        if pygame.key.get_pressed()[K_LSHIFT] or pygame.key.get_pressed()[K_RSHIFT]:
            if self.chosen:
                self.chosen_end = new
            else:
                self.chosen = True
                self.chosen_start = old
                self.chosen_end = new
        else:
            self.chosen = False
            self.chosen_start = None
            self.chosen_end = None
        logging.debug(f"{self.name}{self.id}: course_change: {new}, {old}, shift: l {pygame.key.get_pressed()[K_LSHIFT]} r {pygame.key.get_pressed()[K_RSHIFT]}, chosen: {self.chosen}, chosen_start: {self.chosen_start}, chosen_end: {self.chosen_end}")
    def focus_change(self,new:bool) -> None:
        if new:
            self.chosen = False
            self.course = len(self.text)
        self.__old_focus = new
    def text_change(self,new:str, old:str) -> None:
        self.new_font()

    def update(self, events: list[pygame.event.Event], focus: bool) -> None:
        """
        更新 Entry 控件。

        :param events: 包含 pygame 事件的列表。
        :param focus: 是否被选中。
        """
        super().update(events, focus)
        if focus!= self.__old_focus:
            self.focus_change(focus)
        if focus:
            for event in events:
                if event.type == KEYDOWN:
                    if event.key == K_BACKSPACE:
                        if self.chosen:
                            c_s:int = min((self.chosen_start,self.chosen_end)) # type: ignore
                            c_e:int = max((self.chosen_start,self.chosen_end)) # type: ignore
                            self.text = self.text[:c_s] + self.text[c_e:]
                            self.course = c_s
                            logging.debug(f"{self.name}{self.id}: backspace: {self.text}, course: {self.course}, chosen_start: {self.chosen_start}, chosen_end: {self.chosen_end}")
                            self.chosen = False
                            self.chosen_start = None
                            self.chosen_end = None
                        elif self.course > 0:
                            self.text = self.text[:self.course-1] + self.text[self.course:]
                            self.course -= 1
                            logging.debug(f"{self.name}{self.id}: backspace: {self.text}, course: {self.course}")
                    elif event.key == K_RIGHT:
                        self.course = min(self.course + 1, len(self.text))
                        logging.debug(f"{self.name}{self.id}: right, course: {self.course}")
                    elif event.key == K_LEFT:
                        self.course = max(self.course - 1, 0)
                        logging.debug(f"{self.name}{self.id}: left, course: {self.course}")
                if event.type == TEXTINPUT:
                    logging.debug(f"{self.name}{self.id}: textinput: {event.text}")
                    self.text = self.text[:self.course] + event.text + self.text[self.course:]
                    self.course += len(event.text)
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
                    logging.debug(f"{self.name}{self.id}: mousebuttondown: {pos}, course: {self.course}")
            self.manager.screen.fill(self.background_color, self.rect)
            if self.font:
                text_surface = Surface(self.size*0.8, SRCALPHA)
                if self.chosen:
                    c_s:int = min((self.chosen_start,self.chosen_end)) # type: ignore
                    c_e:int = max((self.chosen_start,self.chosen_end)) # type: ignore
                    text_surface.fill(self.chosen_color, (self.text_long[c_s], 0, self.text_long[c_e]-self.text_long[c_s], self.size[1]*0.8))
                    logging.debug(f"{self.name}{self.id}: chosen: {c_s}, {c_e}, {self.text_long[c_s]}, {self.text_long[c_e]}")
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
                for i in range(0, len(self.text_surface)):
                    text_surface.blit(self.text_surface[i], (Vector2(self.text_long[i], 0)))
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
        logging.debug(f"{self.name}{self.id}: text_surface: {self.text_surface}, text_long: {self.text_long}")