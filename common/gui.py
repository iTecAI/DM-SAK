import pygame
pygame.init()

def kwarg_defaults(obj, kw,**kwargs):
    for k in kwargs.keys():
        try:
            setattr(obj,k,kw[k])
        except KeyError:
            setattr(obj,k,kwargs[k])
    

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

    def _render(self,obj):
        for i in self.children:
            i.render(self,obj)

    def render(self,obj):
        self._render(obj)

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
        kwarg_defaults(self, kwargs, background=(255,255,255), border=(0,0,0))

    def render(self):
        print('rendered')
        print(self.border)
        x,y = self.pos
        print(x,y)
        self.surface.fill(self.background,rect=self.rect)
        self.surface.fill(self.border,rect=pygame.Rect(x,y,self.rect.width,1))
        self.surface.fill(self.border,rect=pygame.Rect(x,y,1,self.rect.height))
        self.surface.fill(self.border,rect=pygame.Rect(x+self.rect.width,y,self.rect.width,self.rect.height))
        self.surface.fill(self.border,rect=pygame.Rect(x,y+self.rect.height,self.rect.width,self.rect.height))


scrn = pygame.display.set_mode([500,500])
gui = GUI(scrn,(0,0))
gui.add_child(Container(scrn,(100,100)))
gui.render(gui)
pygame.display.flip()
while True:
    pass