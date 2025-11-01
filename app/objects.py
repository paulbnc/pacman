import pygame
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
        self.rect = pygame.Rect(x, y, self.size, self.size)
        self.color = pacman_color
        self.speed = pacman_speed

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
        if self.rect.y>height-self.size:
            self.rect.y = height-self.size
        if self.rect.y<0:
            self.rect.y = 0
        if self.rect.x>width-self.size:
            self.rect.x = width-self.size
        if self.rect.x<0:
            self.rect.x = 0

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


class Piecesmap:
    def __init__(self):
        import numpy as np
        self.map = np.random.choice([0, 1], size=(shape_piece_map[0], shape_piece_map[1]), p=[1-freq_pieces, freq_pieces])
        self.color = piece_color
        self.size = piece_size

    def handle_input(self, pacman_x, pacman_y):
        for ligne in range(len(self.map)):
            for col in range(len(self.map[ligne])):
                if self.map[ligne][col] == 1:
                    piece_x = col * piece_size
                    piece_y = ligne * piece_size
                    
                    # Détection de collision rectangulaire
                    if (pacman_x < piece_x + piece_size and 
                        pacman_x + pacman_size > piece_x and
                        pacman_y < piece_y + piece_size and 
                        pacman_y + pacman_size > piece_y):
                        self.map[ligne][col] = 0

    def draw(self, screen):
        for ligne in range(len(self.map)):
            for col in range(len(self.map[ligne])):
                if self.map[ligne][col] == 1:
                    pygame.draw.rect(screen, self.color, pygame.Rect(col*piece_size, ligne*piece_size, self.size, self.size))