import pygame,os
pygame.init()

#init constants
FONTS = {
    'primary':pygame.font.Font(os.path.join('assets','fonts','primary.ttf'),16),
    'secondary':pygame.font.Font(os.path.join('assets','fonts','secondary.ttf'),16)
}

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

def load_sprites_folder(path,sz=[16,16]):
    sprites = []
    for i in os.listdir(path):
        if not '1' in i:
            sheet = pygame.image.load(os.path.join(path,i))
            for x in range(int(sheet.get_width()/sz[0])):
                for y in range(int(sheet.get_height()/sz[1])):
                    s = pygame.Surface(sz)
                    s.blit(sheet,[0,0],area=pygame.Rect(x*16,y*16,16,16))
                    sprites.append(s)
    return sprites


#main function
def main():
    SPRITES = []
    SPRITES.extend(load_sprites_folder(os.path.join('assets','tiles','DawnLike','Objects')))
    SPRITES.extend(load_sprites_folder(os.path.join('assets','tiles','DawnLike','Items')))
    print(SPRITES)