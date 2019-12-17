import pygame
from common import Node
from common import gui
import os

pygame.init()

style_menus = dict(
    background_color=(222, 222, 222),
    hover_color=(210,210,210),
    padding=5
)

font = pygame.font.Font(os.path.join('assets','fonts','primary.ttf'),30)


def main():
    global style_menus, font
    screen = pygame.display.set_mode((1920,1080),pygame.SCALED)
    toolbar = gui.BaseElement(pygame.Rect(0,0,1920,50),style=style_menus)
    new_map_button = gui.HoverButton(pygame.Rect(0,0,100,50),style=style_menus,content=font.render('New Map',True,(0,0,0)))
    new_camp_button = gui.HoverButton(pygame.Rect(new_map_button.available().right,0,100,50),style=style_menus,content=font.render('New Campaign',True,(0,0,0)))
    toolbar.add_child(new_map_button)
    toolbar.add_child(new_camp_button)
    while True:
        screen.fill((255,255,255))
        toolbar.check(pygame.event.get())
        screen.blit(toolbar.render(),toolbar.pos)
        pygame.display.flip()
        if new_map_button.clicked():
            print('New Map')
        if new_camp_button.clicked():
            print('New Campaign')