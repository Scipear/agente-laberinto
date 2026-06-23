import pygame
from src.matrix import Maze
from src.config import (
    CELL_SIZE, WALL, START, FINISH, COLOR_WALL, COLOR_FLOOR, COLOR_START, 
    COLOR_FINISH, COLOR_VISITED, COLOR_PATH, SIDEBAR_WIDTH, COLOR_SIDEBAR_BG, 
    COLOR_CARD_BG, COLOR_CARD_BORDER, COLOR_TEXT_MAIN, COLOR_TEXT_MUTED, 
    COLOR_ACCENT, COLOR_BORDER
)


font_coord = None
font_sidebar_title = None
font_sidebar_text = None
font_sidebar_small = None

def _init_fonts():
    global font_coord, font_sidebar_title, font_sidebar_text, font_sidebar_small

    if font_coord is None:
        if not pygame.font.get_init():
            pygame.font.init()

        font_coord = pygame.font.SysFont("Segoe UI", 8, bold=True)
        font_sidebar_title = pygame.font.SysFont("Segoe UI", 16, bold=True)
        font_sidebar_text = pygame.font.SysFont("Segoe UI", 13)
        font_sidebar_small = pygame.font.SysFont("Segoe UI", 11)


def get_contrast_color(bg_color):
    r, g, b = bg_color

    brightness = (r * 299 + g * 587 + b * 114) / 1000 # formula de luminancia rgb
    return (40, 40, 40) if brightness > 128 else (220, 220, 220)

def draw_sidebar(screen, maze: Maze, algo_running: bool = False):
    _init_fonts()
    
    start = maze.width * CELL_SIZE
    height = maze.height * CELL_SIZE
    sidebar_rect = pygame.Rect(start, 0, SIDEBAR_WIDTH, height)
    
    pygame.draw.rect(screen, COLOR_SIDEBAR_BG, sidebar_rect)

    title_render = font_sidebar_title.render("Historial", True, COLOR_ACCENT)
    screen.blit(title_render, (start + 15, 15))
    
    card_x = start + 12
    card_y = 48
    card_width = SIDEBAR_WIDTH - 24
    card_height = height - 165
    card_rect = pygame.Rect(card_x, card_y, card_width, card_height)
    
    pygame.draw.rect(screen, COLOR_CARD_BG, card_rect, border_radius=8)
    pygame.draw.rect(screen, COLOR_CARD_BORDER, card_rect, 2, border_radius=8)
    
    header_y = card_y + 10
    headers = [
        ("Posicion (x,y)", card_x + 10),
        ("Costo (g)", card_x + 75),
        ("Heuristica (h)", card_x + 120),
        ("Total (f)", card_x + 185)
    ]
    for text, x_pos in headers:
        sub_render = font_sidebar_small.render(text, True, COLOR_TEXT_MUTED)
        screen.blit(sub_render, (x_pos, header_y))
            
    divider_y = card_y + 32
    pygame.draw.line(screen, COLOR_CARD_BORDER, (card_x + 2, divider_y), (card_x + card_width - 2, divider_y), 1)
    
    history = getattr(maze, 'visited_history', [])

    list_y = divider_y + 2
    list_height = card_height - 36
    scroll_rect = pygame.Rect(card_x + 2, list_y, card_width - 4, list_height - 4)
    
    row_height = 25
    total_content_height = len(history) * row_height
    max_scroll = max(0, total_content_height - scroll_rect.height)
    
    scroll_offset = getattr(maze, 'scroll_offset', 0)
    if algo_running:
        scroll_offset = max_scroll
    scroll_offset = max(0, min(scroll_offset, max_scroll))
    maze.scroll_offset = scroll_offset
    
    screen.set_clip(scroll_rect)

    for i, item in enumerate(history):
        item_y = list_y + i * row_height - scroll_offset
        
        if item_y + row_height < list_y or item_y > list_y + list_height:
            continue
            
        is_last = (i == len(history) - 1)
        
        if is_last:
            row_bg = (40, 65, 95)
            row_border = COLOR_ACCENT
            row_rect = pygame.Rect(card_x + 5, item_y + 1, card_width - 10, row_height - 2)
            pygame.draw.rect(screen, row_bg, row_rect, border_radius=4)
            pygame.draw.rect(screen, row_border, row_rect, 1, border_radius=4)
        elif i % 2 == 0:
            row_bg = (35, 35, 45)
            row_rect = pygame.Rect(card_x + 5, item_y + 1, card_width - 10, row_height - 2)
            pygame.draw.rect(screen, row_bg, row_rect, border_radius=4)
            
        coord_str = f"{i+1}. ({item['x']},{item['y']})"
        txt_coord = font_sidebar_text.render(coord_str, True, COLOR_TEXT_MAIN if not is_last else (255, 255, 255))
        screen.blit(txt_coord, (card_x + 10, item_y + 4))
        
        txt_g = font_sidebar_text.render(str(item['g']), True, COLOR_TEXT_MUTED if not is_last else COLOR_TEXT_MAIN)
        screen.blit(txt_g, (card_x + 75, item_y + 4))
        
        txt_h = font_sidebar_text.render(f"{item['h']:.1f}", True, COLOR_ACCENT if not is_last else (255, 255, 255))
        screen.blit(txt_h, (card_x + 120, item_y + 4))
        
        txt_f = font_sidebar_text.render(f"{item['f']:.1f}", True, COLOR_ACCENT if not is_last else (255, 255, 255))
        screen.blit(txt_f, (card_x + 185, item_y + 4))
        
    screen.set_clip(None)
    
    if total_content_height > scroll_rect.height:
        scrollbar_width = 6
        scrollbar_x = card_x + card_width - scrollbar_width - 4
        scrollbar_y = list_y + 4
        scrollbar_height = list_height - 8
        scrollbar_rect = pygame.Rect(scrollbar_x, scrollbar_y, scrollbar_width, scrollbar_height)
        pygame.draw.rect(screen, (20, 20, 25), scrollbar_rect, border_radius=3)
        
        thumb_height = max(15, int(scrollbar_height * (scroll_rect.height / total_content_height)))
        if max_scroll > 0:
            thumb_y = scrollbar_y + int((scrollbar_height - thumb_height) * (scroll_offset / max_scroll))
        else:
            thumb_y = scrollbar_y
        
        thumb_rect = pygame.Rect(scrollbar_x, thumb_y, scrollbar_width, thumb_height)
        pygame.draw.rect(screen, (80, 80, 95), thumb_rect, border_radius=3)

    inst_y = height - 105
    inst_rect = pygame.Rect(start + 12, inst_y, SIDEBAR_WIDTH - 24, 95)
    pygame.draw.rect(screen, COLOR_CARD_BG, inst_rect, border_radius=8)
    pygame.draw.rect(screen, COLOR_BORDER, inst_rect, 1, border_radius=8)
    
    inst_title = font_sidebar_small.render("CONTROLES", True, COLOR_TEXT_MUTED)
    screen.blit(inst_title, (start + 22, inst_y + 6))
    
    ctrl_1 = font_sidebar_small.render("[Espacio] - Iniciar", True, COLOR_TEXT_MAIN)
    ctrl_2 = font_sidebar_small.render("[R] - Reiniciar", True, COLOR_TEXT_MAIN)
    
    screen.blit(ctrl_1, (start + 22, inst_y + 24))
    screen.blit(ctrl_2, (start + 22, inst_y + 44))


def draw_maze(screen, maze: Maze, algo_running: bool):
    _init_fonts()
    
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

            if cell.is_closed:
                color = COLOR_VISITED

            if not algo_running and cell.is_path:
                color = COLOR_PATH

            rect = pygame.Rect(cell.x * cell.size, cell.y * cell.size, cell.size, cell.size)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (200, 200, 200), rect, 1)

            coord_text = f"{cell.x},{cell.y}"
            text_color = get_contrast_color(color)
            text_render = font_coord.render(coord_text, True, text_color)
            screen.blit(text_render, (cell.x * cell.size + 2, cell.y * cell.size + 1))

    if maze.agent is not None:
        agent_rect = pygame.Rect(maze.agent.x * CELL_SIZE, maze.agent.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, maze.agent.color, agent_rect)
        
        coord_text = f"{maze.agent.x},{maze.agent.y}"
        text_surface = font_coord.render(coord_text, True, (255, 255, 255))
        screen.blit(text_surface, (maze.agent.x * CELL_SIZE + 2, maze.agent.y * CELL_SIZE + 1))

    draw_sidebar(screen, maze, algo_running)

