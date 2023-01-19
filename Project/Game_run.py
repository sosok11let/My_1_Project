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

    
def you_lost():
    size = width, height = 600, 600
    screen = pygame.display.set_mode(size)
    image_menu = load_image("Fon_gl.png")
    ship_top = screen.get_height() - image_menu.get_height()
    ship_left = screen.get_width() / 2 - image_menu.get_width() / 2
    running2 = True
    pygame.mouse.set_visible(True)
    start = Button(screen, 300, 65)
    exit_game = Button(screen, 170, 70)
    font = pygame.font.Font('data/font_super_game.ttf', 30)
    gameover.play()

    while running2:
        global f
        pygame.time.delay(20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running2 = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                botton_sound.play()
        screen.blit(image_menu, (ship_left, ship_top))
        start.draw(145, 200, "Играть снова", star_game, 50)
        exit_game.draw(200, 350, "Выход", show_menu, 50)
        text = font.render(f'Score:{score}', False, (255, 0, 0))
        if score > int(f):
            open('txt_files/record.txt', 'w').write(str(score))
        screen.blit(text, (210, 120))
        print_text("GAME OVER", 185, 80, (255, 0, 0))
        pygame.display.update()
    pygame.quit()
    
    
def star_game():
    global score

    pygame.init()
    size = width, height = 1200, 800
    screen = pygame.display.set_mode(size)

    image = load_image('fon.png')
    image2 = load_image('platforma_11.png')
    image3 = load_image('platforma_2.png')
    image4 = load_image('platforma_3.png')
    ship_top = screen.get_height() - image.get_height()
    ship_left = screen.get_width() / 2 - image.get_width() / 2

    image_jump = pygame.image.load('Animation_super_player/player_left_jump.png')
    image_stay = pygame.image.load('Animation_super_player/player_left_4.png')

    image_jump_right = pygame.image.load('Animation_super_player/player_right_jump.png')
    image_stay_right = pygame.image.load('Animation_super_player/player_right_4.png')

    flagbullets = True
    platf = []
    pl1 = Platforms()
    pl2 = Platforms_2()
    pl3 = Platforms_3()
    platf.append(pl1)
    platf.append(pl2)
    platf.append(pl3)
    up = False
    player = Player(55, 55)

    left = False
    right = False

    flagshot = False

    ak47 = pygame.image.load("data/glock.png")
    ak47_2 = ak47.get_rect(center=screen.get_rect().center)

    def blit_point_to_mouse(target_surf, char_surf, x, y):
        mx, my = pygame.mouse.get_pos()
        dir = (mx - x, my - y)
        length = math.hypot(*dir)
        if length == 0.0:
            dir = (0, -1)
        else:
            dir = (dir[0] / length, dir[1] / length)
        angle = math.degrees(math.atan2(-dir[1], dir[0]))
        rotated_surface = pygame.transform.rotate(char_surf, angle)
        rotated_surface_location = rotated_surface.get_rect(center=(player.rect.x + 25, player.rect.y + 35))
        target_surf.blit(rotated_surface, rotated_surface_location)

    pygame.mouse.set_visible(False)

    running = True

    randomspeedufo = [3, 4, 5, 6, 7, 8]
    for i in range(6):
        randomspeedufo_choise = random.choice(randomspeedufo)
        mob = Mobs(screen, randomspeedufo_choise)
        randomspeedufo.remove(randomspeedufo_choise)

    bullets = []
    pos = (250, 250)
    pygame.mixer.music.play(-1)

    leftorright = False

    font = pygame.font.Font('data/font_super_game.ttf', 30)

    hp = 3
    hp_max = 5
    hp_x = 990
    hp_player = pygame.image.load('data/heart.png')
    score = 0

    bullets_count = 10

    def print_hp(hp, hp_x):
        if hp < hp_max:
            for i in range(hp):
                screen.blit(hp_player, (hp_x, 630))
                hp_x += 70

    while running:
        pygame.time.delay(17)
        ax, ay, bb, ss = player.rect
        pos = ax + 20, ay + 30
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if score > int(f):
                    open('txt_files/record.txt', 'w').write(str(score))
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    left = True
                if event.key == pygame.K_d:
                    right = True
                if event.key == pygame.K_SPACE:
                    up = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    left = False
                if event.key == pygame.K_d:
                    right = False
                if event.key == pygame.K_SPACE:
                    up = False
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and flagshot:
                    bull = Bullet(*pos)
                    bullets.append(bull)
                    player_sprites.add(bull)
                    shot.play()
                    bullets_count -= 1
                elif not flagshot:
                    flagshot = True
                for i in bullets:
            plathits = pygame.sprite.spritecollideany(i, plat_sprites)
            if plathits:
                bullets.remove(i)
                flagbullets = True
            else:
                flagbullets = False

        for bullet in bullets[:]:
            bullet.update()
            if not screen.get_rect().collidepoint(bullet.pos):
                bullets.remove(bullet)
                player_sprites.remove(bullet)
                flagbullets = True
            else:
                flagbullets = False

        screen.blit(image, (ship_left, ship_top))

        for bullet in bullets:
            bullet.draw(screen)

        playerhits = pygame.sprite.spritecollide(player, mobs_sprites, False)
        for i in bullets:
            bullethits = pygame.sprite.spritecollideany(i, mobs_sprites)

            if bullethits:
                bullets.remove(i)
                mobs_sprites.remove(bullethits)
                score += 1
                bullets_count += 2

        if bullets_count <= 0 and flagbullets:
            pygame.mixer.music.stop()
            mobs_sprites.remove(mobs_sprites)
            you_lost()

        text_bullets = font.render(f'Bullets:{bullets_count}', False, (0, 0, 0))
        screen.blit(text_bullets, (1000, 700))

        text = font.render(f'Score:{score}', False, (0, 0, 0))
        screen.blit(text, (50, 700))

        screen.blit(image2, (95, 325))
        screen.blit(image3, (900, 270))
        screen.blit(image4, (450, 500))

        player.update(left, right, up, platf)
        player.collide(306, 145, platf)

        randomspeedufo = [3, 4, 5, 6, 7, 8]
        if len(mobs_sprites) <= 3:
            for i in range(6):
                randomspeedufo_choise = random.choice(randomspeedufo)
                mob = Mobs(screen, randomspeedufo_choise)
                randomspeedufo.remove(randomspeedufo_choise)

        mobs_sprites.update()
        mobs_sprites.draw(screen)

        if left:
            if up:
                screen.blit(image_jump, (player.rect.x, player.rect.y))
            else:
                screen.blit(image_stay, (player.rect.x, player.rect.y))
            leftorright = True
        if right:
            if up:
                screen.blit(image_jump_right, (player.rect.x, player.rect.y))
            else:
                screen.blit(image_stay_right, (player.rect.x, player.rect.y))
            leftorright = False
        if up:
            if leftorright:
                screen.blit(image_jump, (player.rect.x, player.rect.y))
            else:
                screen.blit(image_jump_right, (player.rect.x, player.rect.y))
        else:
            if leftorright:
                screen.blit(image_stay, (player.rect.x, player.rect.y))
            else:
                screen.blit(image_stay_right, (player.rect.x, player.rect.y))

        cursor = load_image('cursor.png').convert_alpha()
        for i in mobs_sprites:
            x, y = pygame.mouse.get_pos()
            ax, ay, bx, by = i.rect
            for i in range(ax, ax + 80):
                for k in range(ay, ay + 62):
                    if x == i and y == k:
                        cursor = load_image('cursorred.png').convert_alpha()
                        xxx, yyy = pygame.mouse.get_pos()
                        screen.blit(cursor, (xxx - 16, yyy - 16))

        if playerhits:
            player.rect.left = 600
            player.rect.top = 400
            hp -= 1

        if player.rect.top >= 1000:
            player.rect.left = 600
            player.rect.top = 400
            hp -= 1

        if hp <= 0:
            pygame.mixer.music.stop()
            mobs_sprites.remove(mobs_sprites)
            you_lost()

        print_hp(hp, hp_x)

        if pygame.mouse.get_focused():
            x, y = pygame.mouse.get_pos()
            screen.blit(cursor, (x - 16, y - 16))

        blit_point_to_mouse(screen, ak47, *ak47_2.center)

        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    try:
        show_menu()
    except pygame.error:
        pass

