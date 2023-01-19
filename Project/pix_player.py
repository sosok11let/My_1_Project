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


flag = False

speed_move = 7
GRAVITY = 0.20
PLAY_JUMP = 10


class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((40, 60))
        self.image.fill((113, 182, 185))
        self.xvel = 0
        self.yvel = 0
        self.ongravity = False
        self.startX = x
        self.startY = y
        self.rect = self.image.get_rect(center=(600, 250))
        self.speedy = 15
        self.image.set_colorkey("red")
        self.bivalie = set()

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, left, right, up, platf):
        if up:
            if self.ongravity:
                self.yvel = -PLAY_JUMP

        if left:
            self.xvel = -speed_move

        if right:
            self.xvel = speed_move

        if not(left or right):
            self.xvel = 0

        if not self.ongravity:
            self.yvel += GRAVITY

        self.ongravity = False
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platf)
        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platf)


        if self.rect.left < -50:
            self.rect.left = 1200

        if self.rect.left > 1250:
            self.rect.right = 0

        self.timer = pygame.time.get_ticks() // 250
        if self.timer not in self.bivalie:
            self.bivalie.add(self.timer)
            if self.rect.left == platfff.rect.right:
                self.rect.left += 50

            if self.rect.right == platfff.rect.left:
                self.rect.right -= 50

            if self.rect.right == platfff3.rect.left:
                self.rect.right -= 50

            if self.rect.left == platfff3.rect.right:
                self.rect.left += 50

            if self.rect.right == platfff2.rect.left:
                self.rect.right -= 50

            if self.rect.left == platfff2.rect.right:
                self.rect.left += 50

    def collide(self, xvel, yvel, platf):
        for pl in platf:
            if pygame.sprite.collide_rect(self, pl):
                if xvel > 0:
                    self.rect.right = pl.rect.left
                if xvel < 0:
                    self.rect.left = pl.rect.right
                if yvel > 0:
                    self.rect.bottom = pl.rect.top
                    self.ongravity = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = pl.rect.bottom
                    self.yvel = 0


class Mobs(pygame.sprite.Sprite):
    image = load_image("poletnorm.png")

    def __init__(self, screen, randomspeedufo):
        super().__init__(mobs_sprites)
        self.screen = screen
        self.image = Mobs.image
        self.screen_rect = screen.get_rect()
        self.rightTF = random.choice([True, False])
        if self.rightTF:
            self.leftTF = False
            self.rect = self.image.get_rect(center=(-50, random.randrange(-40, 50)))
        else:
            self.leftTF = True
            self.rect = self.image.get_rect(center=(1250, random.randrange(-40, 50)))
        self.vx = randomspeedufo

        self.yvel = 0

        self.rightonly = random.randrange(100, 150)
        self.leftonly = random.randrange(1000, 1100)
        self.right_pora_nalevo = random.randrange(1000, 1150)
        self.left_pora_napravo = random.randrange(50, 200)

        self.leftorright = False
        self.opusch = False

    def rendering(self):
        mobs_sprites.draw(self.screen)

    def update(self):
        if self.rightTF:
            if not self.leftorright:
                if self.rect.right < width + 150:
                    self.rect.right += self.vx
                if self.rect.right < self.rightonly and not self.opusch:
                    self.rect.top += self.vx * 0.6
                else:
                    self.opusch = True
                if self.rect.right >= self.right_pora_nalevo:
                    self.leftorright = True
            elif self.leftorright:
                if self.rect.left >= self.left_pora_napravo:
                    self.rect.left -= self.vx
                else:
                    self.leftorright = False

        if not self.rightTF:
            if not self.leftorright:
                if self.rect.left >= self.left_pora_napravo:
                    self.rect.left -= self.vx
                if self.rect.left > self.leftonly and not self.opusch:
                    self.rect.top += self.vx * 0.6
                else:
                    self.opusch = True
                if self.rect.left <= self.left_pora_napravo:
                    self.leftorright = True
            elif self.leftorright:
                if self.rect.right <= self.right_pora_nalevo:
                    self.rect.right += self.vx
                else:
                    self.leftorright = False

    def ret(self):
        return self.rect
