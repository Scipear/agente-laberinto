import sys
import pygame
from src.matrix import Maze
from src.config import CELL_SIZE
from src.interface import draw_maze

def main():
    pygame.init()

    screen_width = 25 * CELL_SIZE
    screen_height = 25 * CELL_SIZE
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Agente Que Resuelve Laberintos")
    clock = pygame.time.Clock()
    
    maze = Maze(25, 25)
    maze.generate_random_maze()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    maze.reset_data()
                    maze.generate_random_maze()
                
                # elif event.key == pygame.K_SPACE:

        screen.fill((50, 50, 50))
        draw_maze(screen, maze)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()