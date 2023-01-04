import pygame
import sys
import os
from pix_player import Player
import controls


if __name__ == '__main__':
    pygame.init()
    size = width, height = 1200, 800
    screen = pygame.display.set_mode(size)

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

    image = load_image('fon.png')
    ship_top = screen.get_height() - image.get_height()
    ship_left = screen.get_width()/2 - image.get_width()/2


    fon_sprites = pygame.sprite.Group()

    player = Player(screen)
    running = True
    clock = pygame.time.Clock()
    while running:
        screen.blit(image, (ship_left, ship_top))
        pygame.time.delay(30)
        controls.events(player)
        player.update_player()
        player.rendering()
        pygame.display.flip()
    pygame.quit()
