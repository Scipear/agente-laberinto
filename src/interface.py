import pygame
from src.matrix import Maze
from src.config import CELL_SIZE, WALL, START, FINISH, COLOR_WALL, COLOR_FLOOR, COLOR_START, COLOR_FINISH

def draw_maze(screen, maze: Maze):
    for y in range(maze.height):
        for x in range(maze.width):
            cell = maze.grid[y][x]
            
            if cell.type == WALL:
                color = COLOR_WALL
            elif cell.type == START:
                color = COLOR_START
            elif cell.type == FINISH:
                color = COLOR_FINISH
            else:
                color = COLOR_FLOOR

            rect = pygame.Rect(cell.x * cell.size, cell.y * cell.size, cell.size, cell.size)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (200, 200, 200), rect, 1)
    
    rect = pygame.Rect(maze.agent.x * CELL_SIZE, maze.agent.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, maze.agent.color, rect)

