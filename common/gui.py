import pygame
pygame.init()

def kwarg_defaults(obj, kw,**kwargs):
    for k in kwargs.keys():
        try:
            setattr(obj,k,kw[k])
        except KeyError:
            setattr(obj,k,kwargs[k])
    
DEFAULT_STYLE = dict(
    background_color=(255,255,255)
)

def _nothing_():
    pass

def pr():
    print('click')

class BaseElement:
    def __init__(self,rect,style=DEFAULT_STYLE):
        self.pos = rect.topleft
        self.size = rect.size
        self.surface = pygame.Surface(self.size,pygame.SRCALPHA)
        self.children = []
        self.style = style
    
    def add_child(self,child):
        self.children.append(child)
    
    def render(self):
        self.surface.fill(self.style['background_color'])
        for child in self.children:
            self.surface.blit(child.render(),child.pos)
        return self.surface

    def check(self,events):
        for child in self.children:
            child.check(events)

class Button(BaseElement):
    def __init__(self,rect,style=DEFAULT_STYLE,click=_nothing_,content=pygame.Surface((0,0))):
        super().__init__(rect,style=style)
        self.click = click
        self.content = content
        self.rect = self.surface.get_rect()
        self.rect.size = [x+10 for x in content.get_size()]
        self.content_surface = pygame.Surface(self.rect.size,pygame.SRCALPHA)
        self.surface = pygame.Surface(self.rect.size,pygame.SRCALPHA)
        self.content_surface.fill(self.style['background_color'])
        self.content_surface.blit(content,(5,5))
        self.clicked = False
    
    def render(self):
        self.surface.fill(self.style['background_color'])
        self.surface.blit(self.content_surface,(0,0))

        return self.surface
    
    def check(self,events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
                self.clicked = True
                self.click()
            if event.type == pygame.MOUSEBUTTONUP:
                self.clicked = False
    




scrn = pygame.display.set_mode((200,200))
scrn.fill((255,255,255))
ele = Button(pygame.Rect(50,50,100,100),click=pr,content=pygame.Surface((100,100)))
scrn.blit(ele.render(),ele.pos)
pygame.display.flip()
while True:
    ele.check(pygame.event.get())
