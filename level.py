
import pygame
from tile import Tile
from player import Player
from settings import *
from support import *
from random import choice
from debug import debug
from weapon import Weapon
from ui import UI

class Level:
    def __init__(self):
        # get the display surface
        self.display_surface = pygame.display.get_surface()
        # sprite group setup
        self.visible_sprites = YsortCamerGroup()
        self.obstacles_sprites = pygame.sprite.Group()

        # attack sprites * weapons
        self.current_attack = None
        # sprite setup
        self.create_map()

        # user interface UI
        self.ui = UI()

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('map/map_Grass.csv'),
            'object': import_csv_layout('map/map_LargeObjects.csv'),
        }
        graphics = {
            'grass': import_folder('graphics/grass'),
            'objects': import_folder('graphics/objects')
        }
        #intresting +
        #print(graphics)
        for style,layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x= col_index * TILESIZE
                        y= row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x,y),[self.obstacles_sprites],'invisible')
                        if style == 'grass':
                            random_grass_image = choice(graphics['grass'])
                            Tile((x,y),[ self.visible_sprites,self.obstacles_sprites],'grass', random_grass_image)
                            
                        if style == 'object':
                            surf = graphics['objects'][int(col)]
                            Tile((x,y),[ self.visible_sprites,self.obstacles_sprites],'object',surf)
        #for row_index, row in enumerate(WORLD_MAP):
        #    for col_index, col in enumerate(row):
        #        x= col_index * TILESIZE
        #        y= row_index * TILESIZE
        #        if col == 'x':
        #            Tile((x,y),[self.visible_sprites, self.obstacles_sprites])
        #        if col == 'p':
        #            self.player = Player((x,y),[self.visible_sprites], self.obstacles_sprites)
        self.player = Player(
            (2000,1430),
            [self.visible_sprites], 
            self.obstacles_sprites, 
            self.create_attack, 
            self.destroy_attack,
            self.create_magic,) 
            #print(row_index)
            #print(row)

    def create_attack(self):
        self.current_attack = Weapon(self.player,[self.visible_sprites ])
    def create_magic(self,style,strength,cost):
        print(style)
        print(strength)
        print(cost)

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def run(self):
        # update and draw the game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        #debug(self.player.direction)
        debug(self.player.status)
        self.ui.display(self.player)

class YsortCamerGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset =pygame.math.Vector2()

        # creating the floor map
        self.floor_surf = pygame.image.load('graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))

    def custom_draw(self,player):

        # get offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        #for sprite in self.sprites():
        for sprite in  sorted(self.sprites(),key = lambda sprite:  sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_pos)