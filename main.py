import sys
import pygame
from src.matrix import Maze
from src.config import CELL_SIZE, WALL, START, FINISH, COLOR_WALL, COLOR_FLOOR, COLOR_START, COLOR_FINISH

def draw_maze(screen, maze: Maze):
    for y in range(maze.height):
        for x in range(maze.width):
            cell = maze.grid[y][x]
            
            # 1. Determinar el color según el tipo de celda o su estado en A*
            if cell.type == WALL:
                color = COLOR_WALL
            elif cell.type == START:
                color = COLOR_START
            elif cell.type == FINISH:
                color = COLOR_FINISH
            else:
                color = COLOR_FLOOR

            # 2. Calcular la posición física en píxeles
            # x es la columna (eje X), y es la fila (eje Y)
            rect = pygame.Rect(cell.x * cell.size, cell.y * cell.size, cell.size, cell.size)
            
            # 3. Dibujar el rectángulo relleno
            pygame.draw.rect(screen, color, rect)
            
            # 4. (Opcional) Dibujar un borde gris muy fino para ver la cuadrícula
            pygame.draw.rect(screen, (200, 200, 200), rect, 1)

def main():
    # Inicializar Pygame
    pygame.init()
    
    # Calcular el tamaño de la ventana en píxeles
    screen_width = 25 * CELL_SIZE
    screen_height = 25 * CELL_SIZE
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Agente Explorador Laberinto - A*")
    
    clock = pygame.time.Clock()
    
    # Instanciar el laberinto y generar uno aleatorio desde el inicio
    maze = Maze(25, 25)
    maze.generate_random_maze()

    running = True
    while running:
        # --- 1. Manejo de Eventos ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Presionar 'R' para recrear el laberinto
                    # maze.reset_algorithm_data()
                    maze.generate_random_maze()
                
                elif event.key == pygame.K_SPACE:
                    # Aquí lanzarás el algoritmo A* más adelante
                    print("¡Espacio presionado! Iniciar A*")

        # --- 2. Lógica de Dibujo ---
        screen.fill((50, 50, 50)) # Fondo oscuro por si acaso
        
        draw_maze(screen, maze)   # Dibujamos nuestro laberinto actual
        
        # --- 3. Actualizar Pantalla ---
        pygame.display.flip()
        clock.tick(60) # Limitar a 60 FPS para no saturar el procesador

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()