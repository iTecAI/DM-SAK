import pygame
pygame.init()

def kwarg_defaults(kw,**kwargs):
    out = {}
    for k in kwargs.keys():
        try:
            out[k] = kw[k]
        except KeyError:
            out[k] = kwargs[k]
    return out

class GUI:
    def init(self,kwargs):
        pass

    def __init__(self,surface,pos,**kwargs):
        self.surface = surface
        self.pos = pos
        self.rect = surface.get_rect()
        self.children = []
        self.init(kwargs)
    
    def add_child(self,ui):
        self.children.append(ui)

    def _render(self):
        self.render()
        for i in self.children:
            i.render(self)

    def render(self):
        pass

    def _check(self,events=None):
        if not events:
            events = [e.type for e in pygame.event.get()]
        self.check(events)
        for i in self.children:
            i._check(events)
        
    def check(self,events):
        pass

class Container(GUI):
    def init(self,kwargs):
        kwargs = kwarg_defaults(kwargs, background=(255,255,255,255))