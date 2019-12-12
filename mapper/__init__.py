import pygame,os
pygame.init()

#init constants
FONTS = {
    'primary':pygame.font.Font(os.path.join('assets','fonts','primary.ttf'),16),
    'secondary':pygame.font.Font(os.path.join('assets','fonts','secondary.ttf'),16)
}

class STATE:
    def __init__(self):
        self.current_tile = None

state_inst = STATE()

class Surface(pygame.Surface):
    pass

class Button:
    def __init__(self,rect,text,clickf,color=(222, 222, 222)):
        global FONTS
        self.surface = pygame.Surface(rect.size)
        self.surface.fill(color)
        txtr = FONTS['primary'].render(text,True,(0,0,0))
        tx = int((rect.w - txtr.width)/2)
        ty = int((rect.h - txtr.height)/2)
        self.surface.blit(txtr,(tx,ty))
        self.click = clickf
        self.rect = rect
    def check(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            self.click()

def tile_click_factory(tile):
    def f():
        global state_inst
        state_inst.current_tile = tile
    
    return f

def load_sprites_folder(path,sz=[16,16]):
    sprites = []
    c = 0
    for i in os.listdir(path):
        if not '1' in i:
            sheet = pygame.image.load(os.path.join(path,i))
            for x in range(int(sheet.get_width()/sz[0])):
                for y in range(int(sheet.get_height()/sz[1])):
                    s = Surface(sz)
                    s.blit(sheet,[0,0],area=pygame.Rect(x*16,y*16,16,16))
                    has_color = False
                    for nx in range(s.get_width()):
                        for ny in range(s.get_height()):
                            if s.get_at((nx,ny)) != (0,0,0):
                                has_color = True
                    if has_color:
                        setattr(s,'tilenum',c)
                        setattr(s,'click_func',tile_click_factory(s))
                        sprites.append(s)
                    c += 1
    return sprites


class tiles:
    def __init__(self,mx):
        self.tilepos = 0
        self.mx = mx
    def inc(self):
        self.tilepos += 10
        if self.tilepos > self.mx:
            self.tilepos = mx
    def dec(self):
        self.tilepos -= 10
        if self.tilepos < 0:
            self.tilepos = 0

#main function
def main(size=[1600,800]):
    SPRITES = []
    SPRITES.extend(load_sprites_folder(os.path.join('assets','tiles','DawnLike','Objects')))
    SPRITES.extend(load_sprites_folder(os.path.join('assets','tiles','DawnLike','Items')))
    tls = tiles(len(SPRITES))
    print('Loaded sprites:',len(SPRITES))

    #prepare GUI
    screen = pygame.display.set_mode(size,pygame.RESIZABLE)
    scsurf = pygame.Surface(size)
    running = True
    while running:
        scsurf.fill([0,0,0])
        #load tilebar
        splus = 352
        while True:
            try:
                sprslice = SPRITES[tls.tilepos:tls.tilepos+splus]
                break
            except IndexError:
                splus -= 1
        scount = 1
        x = 2
        y = 2
        for tile in sprslice:
            scsurf.blit(tile,[x,y])
            x += 18
            if scount > 7:
                scount = 0
                y += 18
                x = 2
            scount += 1
        screen.blit(scsurf,[0,0])
        pygame.display.flip()
        pygame.event.pump()




