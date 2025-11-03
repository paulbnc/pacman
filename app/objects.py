import pygame
import numpy as np

from utils import (pacman_color, 
                   pacman_speed, 
                   pacman_size, 
                   width, height, 
                   freq_pieces,
                   shape_piece_map,
                   piece_size,
                   piece_color,
                   HUD_HEIGHT,
                   bullet_size,
                   bullet_speed,
                   pacman_health)

class bullet:
    def __init__(self, direction, x, y):
        self.speed = bullet_speed
        self.size = bullet_size
        self.direction = direction
        self.x = x
        self.y = y
        self.active = True
        self.skin = pygame.image.load("./static/coin.png").convert_alpha()
        self.skin = pygame.transform.scale(self.skin, (self.size, self.size))

    def update(self):
        if self.direction == 'left':
            self.x -= self.speed
        if self.direction == 'right':
            self.x += self.speed
        if self.direction == 'up':
            self.y -= self.speed
        if self.direction == 'down':
            self.y += self.speed
        
        if self.y > height + HUD_HEIGHT:
            self.active = False
        if self.y < HUD_HEIGHT:
            self.active = False
        if self.x > width:
            self.active = False
        if self.x < 0:
            self.active = False

    def draw(self, screen):
        if self.active:
            screen.blit(self.skin, (self.x, self.y))

class Pacman:
    def __init__(self, x, y):

        self.size = pacman_size
        self.x = x
        self.y = y
        self.color = pacman_color
        self.speed = pacman_speed

        self.skin_left = pygame.image.load("./static/eleni_left.png").convert_alpha()
        self.skin_left = pygame.transform.scale(self.skin_left, (self.size, self.size))

        self.skin_right = pygame.image.load("./static/eleni_right.png").convert_alpha()
        self.skin_right = pygame.transform.scale(self.skin_right, (self.size, self.size))

        self.skin_down = pygame.image.load("./static/eleni_down.png").convert_alpha()
        self.skin_down = pygame.transform.scale(self.skin_down, (self.size, self.size))

        self.skin_up = pygame.image.load("./static/eleni_up.png").convert_alpha()
        self.skin_up = pygame.transform.scale(self.skin_up, (self.size, self.size))

        self.last_action = 'left'

        self.bullets = []

        self.health = pacman_health

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

        if keys[pygame.K_SPACE]:
            self.shoot()
        
        # Limites avec HUD_HEIGHT
        if self.y > height + HUD_HEIGHT - self.size:
            self.y = height + HUD_HEIGHT - self.size
        if self.y < HUD_HEIGHT:
            self.y = HUD_HEIGHT
        if self.x > width - self.size:
            self.x = width - self.size
        if self.x < 0:
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
    
    def shoot(self):
        bul = bullet(direction = self.last_action, x=self.x+self.size//2, y=self.y+self.size//2)
        self.bullets.append(bul)

    def update_bullets(self, screen):
        for bul in self.bullets:
            if bul.active:
                bul.update()
                bul.draw(screen)

    def clean_bullets(self):
        self.bullets = [b for b in self.bullets if b.active]

    def hurt(self, num):
        self.health -= num
        self.hurting()

    def hurting(self):
        pass

class Piecesmap:
    def __init__(self):
        self.map = np.random.choice([0, 1], size=(shape_piece_map[1], shape_piece_map[0]), p=[1-freq_pieces, freq_pieces])
        self.color = piece_color
        self.size = piece_size
        self.piece_img = pygame.image.load("./static/tsatsiki.png").convert_alpha()
        self.piece_img = pygame.transform.scale(self.piece_img, (piece_size, piece_size))
        self.cpt_pieces = 0

    def handle_input(self, pacman):
        self.cpt_pieces = 0
        for ligne in range(len(self.map)):
            for col in range(len(self.map[ligne])):
                if self.map[ligne][col] == 1:
                    piece_x = col * piece_size
                    piece_y = ligne * piece_size + HUD_HEIGHT  # Décalage pour HUD
                    if (pacman.x < piece_x + piece_size and 
                        pacman.x + pacman_size > piece_x and
                        pacman.y < piece_y + piece_size and 
                        pacman.y + pacman_size > piece_y):
                        self.map[ligne][col] = 0
                        self.cpt_pieces += 1
                        pacman.hurt(num=5)
                    for bul in pacman.bullets:
                        if bul.active:
                            if (bul.x < piece_x + piece_size and 
                            bul.x + bul.size > piece_x and
                            bul.y < piece_y + piece_size and 
                            bul.y + bul.size > piece_y):
                                self.map[ligne][col] = 0
                                self.cpt_pieces += 1
                                bul.active = False

    def draw(self, screen):
        for ligne in range(len(self.map)):
            for col in range(len(self.map[ligne])):
                if self.map[ligne][col] == 1:
                    # Décalage vertical de HUD_HEIGHT
                    screen.blit(self.piece_img, (col * piece_size, ligne * piece_size + HUD_HEIGHT))

    def victory(self):
        return not np.any(self.map)