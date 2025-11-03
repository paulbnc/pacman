import pygame

fps = 120

HUD_HEIGHT = 80  # Hauteur de la bande HUD

width, height = 600, 520
pacman_speed = 4
bullet_speed = 10
bullet_size = 7
pacman_color = (10, 225, 146)
pacman_size = 50
pacman_health = 100
piece_size = 20

piece_color = (225, 189, 10)

enemy_size = 50
enemy_speed = 1

shape_piece_map = (width//piece_size, height//piece_size)
freq_pieces = 0.1

def draw_popup(surface, victory:bool, font):
    popup = pygame.Surface((400, 200))
    popup.set_alpha(200)
    popup.fill((50, 50, 50))
    if victory:
        text = font.render("You Won", True, (255, 215, 0))
    else:
        text = font.render("Game Over", True, (255, 215, 0))
    text_rect = text.get_rect(center=(200, 100))
    popup.blit(text, text_rect)
    # Centrage avec prise en compte du HUD
    surface.blit(popup, ((width - 400) // 2, (height - 200) // 2 + HUD_HEIGHT))