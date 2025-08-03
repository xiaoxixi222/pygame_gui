from .control import Control , Controller
import pygame
from pygame.locals import *
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
        self.text: str = ""
        self.font: pygame.font.Font | None = font
        self.background_color: pygame.Color = Color(255,255,255)
        self.text_color: pygame.Color = Color(0,0,0)
        self.course_color: pygame.Color = Color(0, 0, 0)
        self.course: int = 0#0a1a2a3
        self.chosen: bool = False
        self.chosen_color: pygame.Color = Color(0,0,255)
        self.chosen_font_color: pygame.Color = Color(255,255,255)
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