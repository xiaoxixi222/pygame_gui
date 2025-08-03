import sys,os
#sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'src'))
print(sys.path)
import pygame_gui
import pygame
pygame.init()
screen=pygame.display.set_mode((800,600))
c=pygame_gui.Controller(screen)
entry = pygame_gui.entry.Entry(c,pygame.font.Font(r"C:\Windows\Fonts\HarmonyOS_Sans_SC_Bold.ttf", 20))
entry.size=pygame.Vector2(200,30)
entry.text = "Hello, world!"
entry.new_font()
entry.update_rect()
c.add_control(entry)
while True:
    events=pygame.event.get()
    for event in events:
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill((0,0,255))
    c.update(events)
    pygame.display.update()