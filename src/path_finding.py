import math
from src.config import CELL_SIZE

def heuristic(cell_a, cell_b):
    a = abs(cell_b.x - cell_a.x) * CELL_SIZE
    b = abs(cell_b.y - cell_a.y) * CELL_SIZE

    return math.sqrt(a**2 + b**2)


