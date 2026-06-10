import random
import heapq
from src.path_finding import heuristic
from src.config import CELL_SIZE, WALL, FLOOR, START, FINISH, COLOR_AGENT

class Agent():
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.color = COLOR_AGENT

class Cell():
    def __init__(self, x: int, y: int, type: int):
        self.x = x
        self.y = y
        self.type = type
        self.size = CELL_SIZE
        self.g = 0
        self.h = 0 
        self.f = 0
        self.parent = None
        self.is_opened = False
        self.is_closed = False
        self.is_path = False

    # Ordenamiento de menor a mayor para el heapq
    def __lt__(self, other):
        return self.f < other.f

class Maze():
    def __init__(self, height: int, width: int, ):
        self.height = height
        self.width = width
        self.grid = [[Cell(x, y, WALL) for x in range(width)] for y in range(height)]
        self.start_cell = None
        self.finish_cell = None
        self.agent = None
        self.visited_history = []

    def set_cell_type(self, x: int, y: int, cell_type: int):
        if 0 <= x < self.width and 0 <= y < self.height:
            cell = self.grid[y][x]
            cell.type = cell_type
            
            if cell_type == START:
                self.start_cell = cell
            elif cell_type == FINISH:
                self.finish_cell = cell

    def generate_random_maze(self, loop_density: float = 0.25):
        stack = [] # Pila para guardar temporalmente los pisos del camino generado
        
        start_x, start_y = 1, 1
        self.grid[start_y][start_x].type = FLOOR
        stack.append((start_x, start_y))

        visited = {(start_x, start_y)}

        while stack:
            current_x, current_y = stack[-1]
            
            neighbors = []
            directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]
            
            for dx, dy in directions:
                nx, ny = current_x + dx, current_y + dy
                if 0 < nx < self.width - 1 and 0 < ny < self.height - 1 and (nx, ny) not in visited:
                    neighbors.append((nx, ny, dx, dy))

            if neighbors:
                nx, ny, dx, dy = random.choice(neighbors)
                
                self.grid[current_y + dy // 2][current_x + dx // 2].type = FLOOR
                self.grid[ny][nx].type = FLOOR # Convierte al vecino y a la celda que se encuentra entre ellos en piso
                
                visited.add((nx, ny))
                stack.append((nx, ny))
            else:
                stack.pop()

        # Posibilidad de destruir paredes para crear caminos adicionales
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                if self.grid[y][x].type == WALL:
                    adjacent_floors = 0
                    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

                    for dx, dy in directions:
                        if self.grid[y + dy][x + dx].type == FLOOR:
                            adjacent_floors += 1

                    if adjacent_floors >= 2 and random.random() < loop_density:
                        self.grid[y][x].type = FLOOR

        self.set_cell_type(1, 1, START)
        self.set_cell_type(self.width - 2, self.height - 2, FINISH)
        self.agent = Agent(1, 1)
        self.heuristic_cells()
        self.visited_history = [{
            'x': self.start_cell.x,
            'y': self.start_cell.y,
            'g': 0,
            'h': self.start_cell.h,
            'f': self.start_cell.h
        }]

    def heuristic_cells(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x].type == FLOOR or self.grid[y][x].type == START:
                    self.grid[y][x].h = heuristic(self.grid[y][x], self.finish_cell)
                    print(f"Cell ({x}, {y}) has heuristic {self.grid[y][x].h}")

    def evaluate_cell(self):
        self.start_cell.f = self.start_cell.g + self.start_cell.h

        open_set = [] # Lista que guarda el recorrido del agente
        heapq.heappush(open_set, self.start_cell)
        self.start_cell.is_opened = True # La celda se encuentra dentro de la lista para considerar su analisis

        while open_set:
            current = heapq.heappop(open_set)
            current.is_opened = False
            current.is_closed = True # La celda ya fue analizada, por lo tanto, no se vuelve a considerar

            if self.agent is not None:
                self.agent.x = current.x
                self.agent.y = current.y
                if not self.visited_history or (self.visited_history[-1]['x'] != current.x or self.visited_history[-1]['y'] != current.y):
                    self.visited_history.append({
                        'x': current.x,
                        'y': current.y,
                        'g': current.g,
                        'h': current.h,
                        'f': current.f
                    })
            
            # Si el agente se encuentra en la celda de la meta, se hace un recorrido por todos los padres
            # hasta llegar a la celda de inicio y se marca como el camino definitivo
            if current == self.finish_cell:
                temp = current
                while temp is not None:
                    temp.is_path = True
                    temp = temp.parent

                yield True
                return

            neighbors = self.get_neighbors(current)
            
            for neighbor in neighbors:
                if not neighbor.is_closed:        
                    tentative_g = current.g + 1
                    
                    if neighbor.g == 0:
                        neighbor.parent = current
                        neighbor.g = tentative_g
                        neighbor.f = neighbor.g + neighbor.h
                        
                        if not neighbor.is_opened:
                            heapq.heappush(open_set, neighbor) # Se guarda la celda vecina en la lista y se ordena automaticamente
                            neighbor.is_opened = True
                        
            yield False 
            
        yield True

    def get_neighbors(self, cell: Cell):
        neighbors = []
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        
        for dx, dy in directions:
            nx, ny = cell.x + dx, cell.y + dy
            
            if 0 <= nx < self.width and 0 <= ny < self.height:
                neighbor = self.grid[ny][nx]
                if neighbor.type != WALL:
                    neighbors.append(neighbor)
                    
        return neighbors

    def reset_data(self):
        for row in self.grid:
            for cell in row:
                cell.type = WALL
                cell.g = 0
                cell.h = 0
                cell.f = 0
                cell.parent = None
                cell.is_opened = False
                cell.is_closed = False
                cell.is_path = False
        self.visited_history = []

