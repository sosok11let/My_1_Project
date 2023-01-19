import pygame
import sys
import os
import random
import math

pygame.init()
size = width, height = 1200, 800
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image

def print_text(massage, x, y, color=(0, 0, 0), font_type='data/font_super_game.ttf', font_size=30):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(massage, True, color)
    screen.blit(text, (x, y))

    
player_sprites = pygame.sprite.Group()
plat_sprites = pygame.sprite.Group()
mobs_sprites = pygame.sprite.Group()
bullet_sprites = pygame.sprite.Group()
platf = []


class Platforms(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(plat_sprites)

        self.screen = screen
        self.image = pygame.Surface((306, 120))
        self.image.fill("red")
        self.rect = self.image.get_rect(center=(250, 390))


platfff = Platforms()


class Platforms_2(pygame.sprite.Sprite):
    image = load_image('platforma_2.png')

    def __init__(self):
        super().__init__(plat_sprites)
        self.screen = screen
        self.image = pygame.Surface((385, 225))
        self.image.fill("red")
        self.rect = self.image.get_rect(center=(640, 625))


platfff2 = Platforms_2()


class Platforms_3(pygame.sprite.Sprite):
    image = load_image('platforma_3.png')

    def __init__(self):
        super().__init__(plat_sprites)
        self.image = pygame.Surface((250, 130))
        self.image.fill("red")
        self.rect = self.image.get_rect(center=(1025, 349))


platfff3 = Platforms_3()

platf.append(platfff)
platf.append(platfff2)
platf.append(platfff3)
