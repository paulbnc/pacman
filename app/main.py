import pygame
from utils import width, height
from objects import Pacman, Piecesmap

def main():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Pacman Prototype")
    clock = pygame.time.Clock()
    running = True

    pacman = Pacman(width // 2, height // 2)
    pieces = Piecesmap()


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("black")

        pacman.handle_input()
        pieces.handle_input(pacman.rect.x, pacman.rect.y)

        pieces.draw(screen)
        pacman.draw(screen)
        

        pygame.display.flip()

        clock.tick(60) 

    pygame.quit()

if __name__ == "__main__":
    main()