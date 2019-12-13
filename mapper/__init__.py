import pygame,os,time,json
pygame.init()

#init constants
FONTS = { #font dict
    'primary':pygame.font.Font(os.path.join('assets','fonts','primary.ttf'),16),
    'secondary':pygame.font.Font(os.path.join('assets','fonts','secondary.ttf'),16)
}

class STATE: #global statekeeper
    def __init__(self):
        self.current_tile = None

state_inst = STATE()

class Surface(pygame.Surface): #editable class
    pass

class Button: #button w/ text
    def __init__(self,rect,text,clickf,color=(222, 222, 222)):
        global FONTS
        self.is_clicked = False
        self.surface = pygame.Surface(rect.size)
        self.surface.fill(color)
        txtr = FONTS['primary'].render(text,True,(0,0,0))
        tx = int((rect.w - txtr.get_width())/2)
        ty = int((rect.h - txtr.get_height())/2)
        self.surface.blit(txtr,(tx,ty))
        self.click = clickf
        self.rect = rect
    def check(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and not self.is_clicked:
            self.click()
            self.is_clicked = True
        if not (self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]):
            self.is_clicked = False

class imgButton(Button): #button w/ image
    def __init__(self,rect,path,clickf,color=(222, 222, 222)):
        global FONTS
        self.is_clicked = False
        self.surface = pygame.Surface(rect.size)
        self.surface.fill(color)
        img = pygame.transform.scale(pygame.image.load(path),rect.size)
        self.surface.blit(img,rect.topleft)
        self.click = clickf
        self.rect = rect

def tile_click_factory(tile): #make a tilebar click function
    def f():
        global state_inst
        state_inst.current_tile = tile
    
    return f

def load_sprites_folder(path,sz=[16,16]): #load sprites from sheets
    sprites = []
    c = 0
    for i in os.listdir(path):
        if not '1' in i:
            sheet = pygame.image.load(os.path.join(path,i))
            for x in range(int(sheet.get_width()/sz[0])):
                for y in range(int(sheet.get_height()/sz[1])):
                    s = Surface(sz,pygame.SRCALPHA)
                    s.blit(sheet,[0,0],area=pygame.Rect(x*16,y*16,16,16))
                    has_color = False
                    for nx in range(s.get_width()):
                        for ny in range(s.get_height()):
                            if s.get_at((nx,ny))[:3] != (0,0,0):
                                has_color = True
                    if has_color:
                        setattr(s,'tilenum',c)
                        setattr(s,'click_func',tile_click_factory(s))
                        sprites.append(s)
                    c += 1
    return sprites


class tiles: #data storage about tilebar
    def __init__(self,mx):
        self.tilepos = 0
        self.mx = mx
    def inc(self):
        self.tilepos += 4
        if self.tilepos > self.mx:
            self.tilepos = self.mx
    def dec(self):
        self.tilepos -= 4
        if self.tilepos < 0:
            self.tilepos = 0

def constrain(val,mini,maxi): #constrains vals between mini and maxi, inclusive
    if val < mini:
        return mini
    if val > maxi:
        return maxi
    return val

class Tile: #tile storage class, has json and dict funcs
    def __init__(self,rotation,tile,pos):
        self.tile = pygame.transform.rotate(tile,rotation)
        self.id = tile.tilenum
        self.rot = rotation
        self.pos = pos
    def jsonize(self):
        return json.dumps({
            'tile':self.id,
            'rotation':self.rot,
            'position':self.pos
        })
    def getdict(self):
        return {
            'tile':self.id,
            'rotation':self.rot,
            'position':self.pos,
            'rendered':self.tile,
            'object':self
        }


#main function
def main(size=[1920,1080]):
    SPRITES = []
    SPRITES.extend(load_sprites_folder(os.path.join('assets','tiles','DawnLike','Objects')))
    SPRITES.extend(load_sprites_folder(os.path.join('assets','tiles','DawnLike','Items')))
    splus = 116
    tls = tiles(len(SPRITES)-splus)
    print('Loaded sprites:',len(SPRITES))

    #prepare GUI
    screen = pygame.display.set_mode(size,pygame.FULLSCREEN)
    screen.convert_alpha()
    scsurf = pygame.Surface(size,pygame.SRCALPHA)
    up_button = Button(pygame.Rect(0,0,146,30),'UP',tls.dec)
    down_button = Button(pygame.Rect(0,1050,146,30),'DOWN',tls.inc)
    #delete_button = imgButton(pygame.Rect(170,1034,32,32))
    tileMap = {}
    current_rotation = 0
    relative_tile_pos = [0,0]
    relative_pos = [0,0]

    current_select_rect = None
    select_action = None
    select_origin = None

    #place selection detector rects
    selection_det_rects = []
    for x in range(55):
        for y in range(32):
            selection_det_rects.append(pygame.Rect(x*32+160,y*32,32,32))
    
    running = True
    while running:
        #fill screen
        scsurf.fill([255,255,255,255])

        #get mouse pos translations
        mp = pygame.mouse.get_pos()
        scr_cur_tile_pos = [constrain(round((mp[0]-16)/32)*32,160,1920),constrain(round((mp[1]-16)/32)*32,0,992)]
        relative_tile_pos = [int(scr_cur_tile_pos[0]/32) + relative_pos[0],int(scr_cur_tile_pos[1]/32) + relative_pos[1]]

        #draw map
        for p in list(tileMap.keys()):
            for layer in tileMap[p]:
                bp = [(layer['position'][0]-relative_pos[0])*32,(layer['position'][1]-relative_pos[1])*32]
                scsurf.blit(pygame.transform.scale(layer['rendered'],[32,32]),bp)


        #menus
        scsurf.fill([232, 232, 232],rect=pygame.Rect(0,0,146,1080))
        scsurf.fill([171, 171, 171],rect=pygame.Rect(146,0,14,1080))
        scsurf.fill([171, 171, 171],rect=pygame.Rect(160,1024,1760,56))
        scsurf.blit(up_button.surface,up_button.rect.topleft)
        scsurf.blit(down_button.surface,down_button.rect.topleft)
        up_button.check()
        down_button.check()

        #load tilebar
        while True:
            try:
                sprslice = SPRITES[tls.tilepos:tls.tilepos+splus]
                break
            except IndexError:
                splus -= 1
        scount = 1
        x = 2
        y = 34
        for tile in sprslice:
            scsurf.blit(pygame.transform.scale(tile,[32,32]),[x,y])
            if pygame.Rect(x,y,32,32).collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                tile.click_func()
            x += 34
            if scount > 3:
                scount = 0
                y += 34
                x = 2
            scount += 1

        #map grid
        for x in range(55):
            scsurf.fill([224, 224, 224, 100],rect= pygame.Rect(x*32+160,0,1,1024))
            for y in range(32):
                scsurf.fill([224, 224, 224, 100],rect= pygame.Rect(160,y*32,1760,1))

        #cursor
        if state_inst.current_tile:
            scsurf.blit(pygame.transform.scale(state_inst.current_tile,[32,32]),scr_cur_tile_pos)

        #draw selection box
        if select_action != None:
            sc = pygame.mouse.get_pos()
            sc = [constrain(sc[0],160,1920),constrain(sc[1],0,1024)]
            current_select_rect.w = sc[0] - select_origin[0]
            current_select_rect.h = sc[1] - select_origin[1]

            if current_select_rect.w < 0:
                current_select_rect = pygame.Rect(sc[0],select_origin[1],abs(current_select_rect.w),current_select_rect.h)
            if current_select_rect.h < 0:
                current_select_rect = pygame.Rect(current_select_rect.topleft[0],sc[1],current_select_rect.w,abs(current_select_rect.h))

            sel_surf = pygame.Surface(current_select_rect.size,pygame.SRCALPHA)
            sel_surf.fill((128, 183, 255, 100))
            scsurf.blit(sel_surf,current_select_rect.topleft)
            

        screen.blit(scsurf,[0,0])

        pygame.display.flip()
        

        #run the event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] <= 146:
                    if event.button == 4:
                        tls.dec()
                    if event.button == 5:
                        tls.inc()
                if event.button == 1 and event.pos[0]>160 and event.pos[1]<1024 and state_inst.current_tile:
                    current_select_rect = pygame.Rect(event.pos,(0,0))
                    select_action = 1
                    select_origin = event.pos
                if event.button == 3 and event.pos[0]>160 and event.pos[1]<1024:
                    current_select_rect = pygame.Rect(event.pos,(0,0))
                    select_action = 2
                    select_origin = event.pos
            if event.type == pygame.MOUSEBUTTONUP:
                if select_action:

                    for rect in current_select_rect.collidelistall(selection_det_rects):
                        crect = selection_det_rects[rect]
                        crx = crect.topleft[0]
                        cry = crect.topleft[1]
                        relpos = [int(crx/32) + relative_pos[0],int(cry/32) + relative_pos[1]]
                        if select_action == 1:
                            tile_temp = Tile(current_rotation,state_inst.current_tile,relpos).getdict()
                            if tuple(relpos) in tileMap.keys():
                                tileMap[tuple(relpos)].append(tile_temp)
                            else:
                                tileMap[tuple(relpos)] = [tile_temp]
                        if select_action == 2:
                            if tuple(relpos) in tileMap.keys():
                                if len(tileMap[tuple(relpos)]) > 0:
                                    tileMap[tuple(relpos)].pop()
                                if len(tileMap[tuple(relpos)]) == 0:
                                    del tileMap[tuple(relpos)]

                    select_action = None
                    current_select_rect = None
                    select_origin = None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    relative_pos[1] -= 1
                if event.key == pygame.K_DOWN:
                    relative_pos[1] += 1
                if event.key == pygame.K_LEFT:
                    relative_pos[0] -= 1
                if event.key == pygame.K_RIGHT:
                    relative_pos[0] += 1