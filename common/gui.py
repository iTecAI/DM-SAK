import pygame
pygame.init()

def kwarg_defaults(obj, kw,**kwargs):
    for k in kwargs.keys():
        try:
            setattr(obj,k,kw[k])
        except KeyError:
            setattr(obj,k,kwargs[k])
    
DEFAULT_STYLE = dict(
    background_color=(255,255,255),
    hover_color=(127,127,127),
    padding=5
)

def _nothing_():
    pass

def pr():
    print('click')

class BaseElement:
    def __init__(self,rect,style=DEFAULT_STYLE):
        global DEFAULT_STYLE
        self.pos = rect.topleft
        self.size = rect.size
        self.surface = pygame.Surface(self.size,pygame.SRCALPHA)
        self.children = []
        self.style = style
        for k in DEFAULT_STYLE.keys():
            if not k in self.style.keys():
                self.style[k] = DEFAULT_STYLE[k]
    
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
    
    def available(self):
        obj = self
        class Available:
            above=obj.pos[1]
            below=obj.pos[1]+self.size[1]
            left=obj.pos[0]
            right=obj.pos[0]+self.size[0]

        return Available

class Frame(BaseElement):
    def __init__(self,rect,style=DEFAULT_STYLE,select=False,select_function=_nothing_):
        super().__init__(rect,style)
        self.select = True
        self.selecting = False
        self.selecting_rect = None
        self.sfunc = select_function

class ContentBox(BaseElement):
    def __init__(self,rect,style=DEFAULT_STYLE,content=pygame.Surface((0,0))):
        super().__init__(rect,style=style)
        self.content = content
        self.rect = pygame.Rect(self.pos,self.surface.get_rect().size)
        size = content.get_size()
        
        if size[0]+2*self.style['padding'] > self.rect.size[0]:
            self.rect.w = size[0]+2*self.style['padding']
        if size[1]+2*self.style['padding'] > self.rect.size[1]:
            self.rect.h = size[1]+2*self.style['padding']
        self.size = self.rect.size

        self.surface = pygame.Surface(self.rect.size,pygame.SRCALPHA)
        self.surface.fill(self.style['background_color'])
        self.content_surface_pos = [(self.rect.w/2) - content.get_width()/2,(self.rect.h/2) - content.get_height()/2]
        self.surface.blit(content,self.content_surface_pos)

    
    def render(self):
        self.surface.fill(self.style['background_color'])
        self.surface.blit(self.content,self.content_surface_pos)

        return self.surface
    
    def check(self,events):
        pass

class Button(ContentBox):
    def __init__(self,rect,style=DEFAULT_STYLE,click=_nothing_,content=pygame.Surface((0,0))):
        super().__init__(rect,style=style,content=content)
        self.click = click
        self._clicked = False
    
    def check(self,events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
                self._clicked = True
                self.click()
            if event.type == pygame.MOUSEBUTTONUP:
                self._clicked = False
    
    def clicked(self):
        if self._clicked:
            self._clicked = False
            return True
        return False

class HoverButton(Button):
    def __init__(self,rect,style=DEFAULT_STYLE,click=_nothing_,content=pygame.Surface((0,0))):
        super().__init__(rect,style=style,content=content,click=click)
        self.hovered = False

    def render(self):
        if self.hovered:
            self.surface.fill(self.style['hover_color'])
        else:
            self.surface.fill(self.style['background_color'])
        self.surface.blit(self.content,self.content_surface_pos)

        return self.surface
    
    def check(self,events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
                self._clicked = True
                self.click()
            if event.type == pygame.MOUSEBUTTONUP:
                self._clicked = False
            if event.type == pygame.MOUSEMOTION:
                if self.rect.collidepoint(event.pos):
                    self.hovered = True
                else:
                    self.hovered = False