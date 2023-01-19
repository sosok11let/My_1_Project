import pygame
import sys
import os
import random
import math
from pix_player import Player, Platforms, Platforms_2, Platforms_3, Mobs, Bullet, print_text
from pix_player import player_sprites, mobs_sprites, plat_sprites
from button_game import Button

botton_sound = pygame.mixer.Sound('data/click.mp3')

shot = pygame.mixer.Sound('data/shot.mp3')

gameover = pygame.mixer.Sound('data/GameOver.mp3')

pygame.mixer.music.load('data/music_gameplay.mp3')

botton_sound.set_volume(0.3)
shot.set_volume(0.07)
gameover.set_volume(0.2)
pygame.mixer.music.set_volume(0.1)

f = open('txt_files/record.txt', 'r').read()
if f:
    f = 0


def load_image(name, colorkey=(0, 0, 0)):
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


def show_menu():
    global f
    size = width, height = 1200, 800
    screen = pygame.display.set_mode(size)
    image_menu = load_image("Fon_gl.png")
    image_play = load_image('gl.png')
    image_glock = load_image('glock_gl.png')
    ship_top = screen.get_height() - image_menu.get_height()
    ship_left = screen.get_width() / 2 - image_menu.get_width() / 2
    running2 = True
    pygame.mouse.set_visible(True)
    start = Button(screen, 170, 65)
    exit_game = Button(screen, 170, 70)
    fon_ino = pygame.sprite.Group()
    
    class Mobs(pygame.sprite.Sprite):
        image = pygame.image.load('data/poletnorm.png')

        def __init__(self, screen):
            super().__init__(fon_ino)
            self.screen = screen
            self.image = Mobs.image
            self.rect = self.image.get_rect(center=(200, 550))
            self.bival = set()
            self.flag = False

        def rendering(self):
            fon_ino.draw(self.screen)

        def update(self):
            if not self.flag:
                if self.rect.top <= 600:
                    self.rect.top += 3
                if self.rect.top == 600:
                    self.flag = True

            else:
                self.rect.top -= 3
                if self.rect.top <= 400:
                    self.flag = False

    fon_mob = Mobs(screen)

    while running2:
        pygame.time.delay(20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running2 = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                botton_sound.play()
        screen.blit(image_menu, (ship_left, ship_top))
        screen.blit(image_play, (1100, 600))
        screen.blit(image_glock, (1090, 650))
        fon_mob.update()
        fon_ino.draw(screen)
        f = open('txt_files/record.txt', 'r').read()
        print_text(f'Record: {f}', 155, 30, (255, 255, 100))
        print_text('D - Идти вправо', 780, 560, (255, 255, 130))
        print_text('A - Идти влево', 780, 590, (255, 255, 130))
        print_text('Spase - Прыжок', 780, 620, (255, 255, 130))
        print_text('ЛКМ - Выстрел', 780, 650, (255, 255, 130))
        start.draw(500, 200, "Играть", star_game, 50)
        exit_game.draw(500, 600, "Выход", quit, 50)
        pygame.display.update()
    pygame.quit()
