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
        self.skin = pygame.image.load("./static/chill_guy.png").convert_alpha()
        self.skin = pygame.transform.scale(self.skin, (self.size, self.size))

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed
        if self.y>height-self.size:
            self.y = height-self.size
        if self.y<0:
            self.y = 0
        if self.x>width-self.size:
            self.x = width-self.size
        if self.x<0:
            self.x = 0

    def draw(self, screen):
        screen.blit(self.skin, (self.x, self.y))


class Piecesmap:
    def __init__(self):
        self.map = np.random.choice([0, 1], size=(shape_piece_map[1], shape_piece_map[0]), p=[1-freq_pieces, freq_pieces])
        self.color = piece_color
        self.size = piece_size
        self.piece_img = pygame.image.load("./static/piece.png").convert_alpha()
        self.piece_img = pygame.transform.scale(self.piece_img, (piece_size, piece_size))

    def handle_input(self, pacman_x, pacman_y):
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

    def draw(self, screen):
        for ligne in range(len(self.map)):
            for col in range(len(self.map[ligne])):
                if self.map[ligne][col] == 1:
                    screen.blit(self.piece_img, (col * piece_size, ligne * piece_size))

    def victory(self):
        return not np.any(self.map)