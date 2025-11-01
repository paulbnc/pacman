# main.py
import pygame
from utils import width, height, draw_popup, fps, piece_size, shape_piece_map
from objects import Pacman, Piecesmap
from session_status import best, total
import time
import numpy as np

HUD_HEIGHT = 80  # bande pour HUD au-dessus du jeu

def main():
    pygame.init()
    pygame.font.init()

    # Polices "retro gaming"
    vic_font = pygame.font.SysFont("Courier", 64, bold=True)
    btn_font = pygame.font.SysFont("Courier", 28, bold=True)
    hud_font = pygame.font.SysFont("Courier", 20, bold=True)

    screen = pygame.display.set_mode((width, height + HUD_HEIGHT))
    pygame.display.set_caption("Pacman Prototype")
    clock = pygame.time.Clock()

    pacman = Pacman(width // 2, height // 2 + HUD_HEIGHT)
    pieces = Piecesmap()
    victory_mode = False

    scanlines = [y for y in range(HUD_HEIGHT, height + HUD_HEIGHT, 4)]
    restart_rect = pygame.Rect(width//2 - 100, height//2 + HUD_HEIGHT + 60, 200, 60)

    # Timer de partie
    start_time = time.time()

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
            # Affichage popup
            draw_popup(screen, victory=True, font=vic_font)

            # Bouton RESTART
            if restart_rect.collidepoint(mouse_pos):
                color = (255, 220, 120)
                if click:
                    pacman = Pacman(width // 2, height // 2 + HUD_HEIGHT)
                    pieces = Piecesmap()
                    victory_mode = False
                    start_time = time.time()
            else:
                color = (180, 180, 180)

            pygame.draw.rect(screen, color, restart_rect, border_radius=8)
            restart_text = btn_font.render("RESTART", True, (0, 0, 0))
            text_rect = restart_text.get_rect(center=restart_rect.center)
            screen.blit(restart_text, text_rect)

            # Scanlines pour effet retro
            for y in scanlines:
                pygame.draw.line(screen, (0, 0, 0), (0, y), (width, y), 1)

        else:
            # Gestion du joueur et des pièces
            pacman.handle_input()
            pieces.handle_input(pacman.x, pacman.y)

            # Mise à jour du total de pièces mangées
            total['pieces'] += pieces.cpt_pieces

            pieces.draw(screen)
            pacman.draw(screen)

            # Victoire
            if pieces.victory():
                victory_mode = True
                elapsed_time = time.time() - start_time
                if (total['pieces'] > best['pieces'] or 
                    (total['pieces'] == best['pieces'] and elapsed_time < best['time'])):
                    best['pieces'] = total['pieces']
                    best['time'] = elapsed_time

        # -------------------------------
        # Affichage HUD (en haut)
        # -------------------------------
        pygame.draw.rect(screen, (30, 30, 30), (0, 0, width, HUD_HEIGHT))
        hud_y = 10
        total_pieces_text = hud_font.render(f"Total Pieces: {total['pieces']}", True, (255, 215, 0))
        screen.blit(total_pieces_text, (10, hud_y))

        remaining = np.sum(pieces.map)
        proportion_text = hud_font.render(f"Remaining: {remaining}", True, (255, 215, 0))
        screen.blit(proportion_text, (10, hud_y + 25))

        # Timer partie en cours
        if not victory_mode:
            elapsed_time = time.time() - start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        tenths = int((elapsed_time * 10) % 10)
        timer_text = hud_font.render(f"Time: {minutes:02}:{seconds:02}.{tenths}", True, (255, 215, 0))
        screen.blit(timer_text, (10, hud_y + 50))

        # Stats meilleure partie
        best_time = best['time']
        if best_time == float('inf'):
            best_time = 0
        best_minutes = int(best_time // 60)
        best_seconds = int(best_time % 60)
        best_tenths = int((best_time * 10) % 10)
        best_text = hud_font.render(f"Best: {best['pieces']} pieces in {best_minutes:02}:{best_seconds:02}.{best_tenths}", True, (255, 215, 0))
        screen.blit(best_text, (width - 350, 10))

        pygame.display.flip()
        clock.tick(fps) 

if __name__ == "__main__":
    main()
