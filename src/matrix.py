import random
from src.config import CELL_SIZE, WALL, FLOOR, START, FINISH

class Cell():
    def __init__(self, x: int, y: int, type: int):
        self.x = x
        self.y = y
        self.type = type
        self.size = CELL_SIZE

class Maze():
    def __init__(self, height: int, width: int, ):
        self.height = height
        self.width = width
        self.grid = [[Cell(x, y, WALL) for x in range(width)] for y in range(height)]
        self.start_cell = None
        self.finish_cell = None

    def set_cell_type(self, x: int, y: int, cell_type: int):
        if 0 <= x < self.width and 0 <= y < self.height:
            cell = self.grid[y][x]
            cell.type = cell_type
            
            if cell_type == START:
                self.start_cell = cell
            elif cell_type == FINISH:
                self.finish_cell = cell

    def generate_random_maze(self, loop_density: float = 0.001):
        """Genera un laberinto aleatorio usando DFS con Backtracking."""
        # 1. Llenar todo el laberinto de paredes
        for row in self.grid:
            for cell in row:
                cell.type = WALL

        # Pila para el backtracking (guarda tuplas con las coordenadas x, y)
        stack = []
        
        # Empezamos en una celda aleatoria (preferiblemente en coordenadas impares)
        start_x, start_y = 1, 1
        self.grid[start_y][start_x].type = FLOOR
        stack.append((start_x, start_y))

        # Conjunto de celdas ya visitadas por el generador
        visited = {(start_x, start_y)}

        while stack:
            current_x, current_y = stack[-1]
            
            # Buscar vecinos que estén a 2 celdas de distancia (para dejar paredes intermedias)
            neighbors = []
            directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]
            
            for dx, dy in directions:
                nx, ny = current_x + dx, current_y + dy
                if 0 < nx < self.width - 1 and 0 < ny < self.height - 1:
                    if (nx, ny) not in visited:
                        neighbors.append((nx, ny, dx, dy))

            if neighbors:
                # Elegir un vecino al azar
                nx, ny, dx, dy = random.choice(neighbors)
                
                # Derribar la pared intermedia
                self.grid[current_y + dy // 2][current_x + dx // 2].type = FLOOR
                # Hacer que la celda destino sea camino
                self.grid[ny][nx].type = FLOOR
                
                visited.add((nx, ny))
                stack.append((nx, ny))
            else:
                # Si no hay vecinos elegibles, retrocedemos
                stack.pop()

            for y in range(1, self.height - 1):
                for x in range(1, self.width - 1):
                    if self.grid[y][x].type == WALL:
                        # Contamos cuántos caminos vacíos rodean a esta pared
                        adjacent_floors = 0
                        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
                        for dx, dy in directions:
                            if self.grid[y + dy][x + dx].type == FLOOR:
                                adjacent_floors += 1
                        
                        # Si la pared está justo en medio de dos caminos y pasa el ratio de aleatoriedad
                        if adjacent_floors >= 2 and random.random() < loop_density:
                            self.grid[y][x].type = FLOOR

        # 2. Asegurar que colocamos un Inicio y un Fin en zonas transitables
        # Por ejemplo: esquina superior izquierda e inferior derecha
        self.set_cell_type(1, 1, START)
        self.set_cell_type(self.width - 2, self.height - 2, FINISH)

