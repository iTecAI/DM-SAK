import pygame
from common import Node
from common import gui
import os

pygame.init()

style_menus = dict(
    background_color=(222, 222, 222),
    hover_color=(210,210,210),
    padding=10
)

font = pygame.font.Font(os.path.join('assets','fonts','primary.ttf'),30)

class STATE:
    def __init__(self):
        self.zoom = 1
        self.zoom_min = 0.1
        self.zoom_max = 10

def cap(val,mini,maxi):
    if val < mini:
        val = mini
    if val > maxi:
        val = maxi
    return val

state = STATE()

def zoom_in():
    global state
    state.zoom = cap(state.zoom+0.1,state.zoom_min,state.zoom_max)

def zoom_out():
    global state
    state.zoom = cap(state.zoom-0.1,state.zoom_min,state.zoom_max)

def main():
    global style_menus, font, state
    screen = pygame.display.set_mode((1920,1080),pygame.SCALED)
    toolbar = gui.BaseElement(pygame.Rect(0,0,1920,50),style=style_menus)
    new_map_button = gui.HoverButton(pygame.Rect(0,0,100,50),style=style_menus,content=font.render('New Map',True,(0,0,0)))
    new_camp_button = gui.HoverButton(pygame.Rect(new_map_button.available().right,0,100,50),style=style_menus,content=font.render('New Campaign',True,(0,0,0)))
    toolbar.add_child(new_map_button)
    toolbar.add_child(new_camp_button)

    zoom_out_btn = gui.HoverButton(pygame.Rect(1850,1010,50,50),style=style_menus,click=zoom_out,content=font.render('-',True,(0,0,0)))
    zoom_in_btn = gui.HoverButton(pygame.Rect(1850,zoom_out_btn.available().above-60,50,50),style=style_menus,click=zoom_in,content=font.render('+',True,(0,0,0)))
    
    while True:
        screen.fill((255,255,255))
        events = pygame.event.get()
        toolbar.check(events)
        zoom_in_btn.check(events)
        zoom_out_btn.check(events)
        screen.blit(toolbar.render(),toolbar.pos)
        screen.blit(zoom_in_btn.render(),zoom_in_btn.pos)
        screen.blit(zoom_out_btn.render(),zoom_out_btn.pos)
        
        pygame.display.flip()
        if new_map_button.clicked():
            print('New Map')
        if new_camp_button.clicked():
            print('New Campaign')
        