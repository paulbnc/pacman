import pygame
import numpy as np

from utils import (pacman_color, 
                   pacman_speed, 
                   pacman_size, 
                   width, height, 
                   freq_pieces,
                   shape_piece_map,
                   piece_size,
                   piece_color)

class Pacman:
    def __init__(self, x, y):

        self.size = pacman_size
        self.x = x
        self.y = y
        self.color = pacman_color
        self.speed = pacman_speed

        self.skin_left = pygame.image.load("./static/chill_guy_turned_left.png").convert_alpha()
        self.skin_left = pygame.transform.scale(self.skin_left, (self.size, self.size))

        self.skin_right = pygame.image.load("./static/chill_guy_turned_right.png").convert_alpha()
        self.skin_right = pygame.transform.scale(self.skin_right, (self.size, self.size))

        self.skin_down = pygame.image.load("./static/chill_guy_turned_down.png").convert_alpha()
        self.skin_down = pygame.transform.scale(self.skin_down, (self.size, self.size))

        self.skin_up = pygame.image.load("./static/chill_guy_turned_up.png").convert_alpha()
        self.skin_up = pygame.transform.scale(self.skin_up, (self.size, self.size))

        self.last_action = None

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
            self.last_action = 'left'
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
            self.last_action = 'right'
        if keys[pygame.K_UP]:
            self.y -= self.speed
            self.last_action = 'up'
        if keys[pygame.K_DOWN]:
            self.y += self.speed
            self.last_action = 'down'
        if self.y>height-self.size:
            self.y = height-self.size
        if self.y<0:
            self.y = 0
        if self.x>width-self.size:
            self.x = width-self.size
        if self.x<0:
            self.x = 0

    def draw(self, screen):
        if self.last_action == 'left' or self.last_action is None:
            screen.blit(self.skin_left, (self.x, self.y))
        if self.last_action == 'right':
            screen.blit(self.skin_right, (self.x, self.y))
        if self.last_action == 'up':
            screen.blit(self.skin_up, (self.x, self.y))
        if self.last_action == 'down':
            screen.blit(self.skin_down, (self.x, self.y))


class Piecesmap:
    def __init__(self):
        self.map = np.random.choice([0, 1], size=(shape_piece_map[1], shape_piece_map[0]), p=[1-freq_pieces, freq_pieces])
        self.color = piece_color
        self.size = piece_size
        self.piece_img = pygame.image.load("./static/coin.png").convert_alpha()
        self.piece_img = pygame.transform.scale(self.piece_img, (piece_size, piece_size))
        self.cpt_pieces = 0

    def handle_input(self, pacman_x, pacman_y):
        self.cpt_pieces = 0
        for ligne in range(len(self.map)):
            for col in range(len(self.map[ligne])):
                if self.map[ligne][col] == 1:
                    piece_x = col * piece_size
                    piece_y = ligne * piece_size
                    if (pacman_x < piece_x + piece_size and 
                        pacman_x + pacman_size > piece_x and
                        pacman_y < piece_y + piece_size and 
                        pacman_y + pacman_size > piece_y):
                        self.map[ligne][col] = 0
                        self.cpt_pieces += 1

    def draw(self, screen):
        for ligne in range(len(self.map)):
            for col in range(len(self.map[ligne])):
                if self.map[ligne][col] == 1:
                    screen.blit(self.piece_img, (col * piece_size, ligne * piece_size))

    def victory(self):
        return not np.any(self.map)