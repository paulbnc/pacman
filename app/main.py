import pygame
from utils import width, height, draw_popup, fps
from objects import Pacman, Piecesmap
from session_status import best, total

def main():
    pygame.init()
    pygame.font.init()

    vic_font = pygame.font.SysFont("Courier", 64, bold=True)
    btn_font = pygame.font.SysFont("Courier", 28, bold=True)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Pacman Prototype")
    clock = pygame.time.Clock()

    pacman = Pacman(width // 2, height // 2)
    pieces = Piecesmap()
    victory_mode = False

    scanlines = [y for y in range(0, height, 4)]

    restart_rect = pygame.Rect(width//2 - 100, height//2 + 60, 200, 60)

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True

        screen.fill("black")

        if victory_mode:
            draw_popup(screen, victory=True, font=vic_font)

            if restart_rect.collidepoint(mouse_pos):
                color = (255, 220, 120)
                if click:
                    pacman = Pacman(width // 2, height // 2)
                    pieces = Piecesmap()
                    victory_mode = False
            else:
                color = (180, 180, 180)

            pygame.draw.rect(screen, color, restart_rect, border_radius=8)
            restart_text = btn_font.render("RESTART", True, (0, 0, 0))
            text_rect = restart_text.get_rect(center=restart_rect.center)
            screen.blit(restart_text, text_rect)

            for y in scanlines:
                pygame.draw.line(screen, (0, 0, 0), (0, y), (width, y), 1)

        else:
            pacman.handle_input()
            pieces.handle_input(pacman.x, pacman.y)

            total['pieces'] += pieces.cpt_pieces

            pieces.draw(screen)
            pacman.draw(screen)

            if pieces.victory():
                victory_mode = True

        pygame.display.flip()
        clock.tick(fps) 

if __name__ == "__main__":
    main()
