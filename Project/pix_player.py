import pygame
import sys
import os

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


player_sprites = pygame.sprite.Group()
plat_sprites = pygame.sprite.Group()
plat_sprites2 = pygame.sprite.Group()

'''plat_W = 30
plat_H = 30

class Fon(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(player_sprites)
        self.img = Surface((plat_W, plat_H))'''



class Player(pygame.sprite.Sprite):
    image = load_image("demo_pix_player.png")

    def __init__(self, screen):
        super().__init__(player_sprites)
        self.screen = screen
        self.image = Player.image
        self.screen_rect = screen.get_rect()
        self.rect = self.image.get_rect(center=(50, 400))
        self.right = False
        self.left = False
        self.jump = False

        self.vx = 7
        self.jump_count = 10

        self.yvel = 0
        self.gravity = 0.35
        self.ongravity = False

    def rendering(self):
        player_sprites.draw(self.screen)

    def update_player(self):
        """player movement"""
        if self.right and self.rect.right < width + 25:
            self.rect.right += self.vx
        if self.left and self.rect.left > 0 - 10:
            self.rect.left -= self.vx

        if self.jump:
            if self.ongravity:
                self.yvel = -self.jump_count

        if not self.ongravity:
            self.yvel += self.gravity

        self.ongravity = False
        self.rect.top += self.yvel
