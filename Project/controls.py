import pygame
import sys

clock = pygame
def events(player):
    """all events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                player.right = True
            if event.key == pygame.K_a:
                player.left = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                player.right = False
            if event.key == pygame.K_a:
                player.left = False
        if player.jump == False:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump = True
                else:
                    player.jump = False
