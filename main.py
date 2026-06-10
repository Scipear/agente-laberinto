import sys
import pygame
from src.matrix import Maze
from src.config import CELL_SIZE, SIDEBAR_WIDTH
from src.interface import draw_maze

def main():
    pygame.init()

    screen_width = 25 * CELL_SIZE + SIDEBAR_WIDTH
    screen_height = 25 * CELL_SIZE
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Agente Que Resuelve Laberintos")
    clock = pygame.time.Clock()
    
    maze = Maze(25, 25)
    maze.generate_random_maze()

    algo_running = False
    is_finished = False
    generator = None
    running = True
    maze.scroll_offset = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    algo_running = False
                    generator = None
                    maze.reset_data()
                    maze.generate_random_maze()
                    maze.scroll_offset = 0
                
                elif event.key == pygame.K_SPACE:
                    generator = maze.evaluate_cell()
                    algo_running = True
                    maze.scroll_offset = 0
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in (4, 5):
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if mouse_x >= 25 * CELL_SIZE:
                        if event.button == 4:  # Scrolleo hacia arriba
                            maze.scroll_offset = max(0, maze.scroll_offset - 25)
                        elif event.button == 5:  # Scrolleo hacia abajo
                            maze.scroll_offset += 25
            
            elif event.type == pygame.MOUSEWHEEL:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if mouse_x >= 25 * CELL_SIZE:
                    maze.scroll_offset = max(0, maze.scroll_offset - event.y * 25)
            
        if algo_running and generator is not None:
            try:
                finished = next(generator)
                if finished:
                    algo_running = False
            except StopIteration:
                algo_running = False

        screen.fill((50, 50, 50))
        draw_maze(screen, maze, algo_running)
        
        pygame.display.flip()
        clock.tick(15)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()