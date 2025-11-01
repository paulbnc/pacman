import pygame

fps = 120

width, height = 600, 520
pacman_speed = 4
pacman_color = (10, 225, 146)
pacman_size = 50

piece_size = 20

piece_color = (225, 189, 10)

shape_piece_map = (width//piece_size, height//piece_size)
freq_pieces = 0.05

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
    surface.blit(popup, ((width - 400) // 2, (height - 200) // 2))

