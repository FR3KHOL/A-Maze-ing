import os
import time
import random
from collections import deque
from a_maze_ing.config_handler import Settings
from a_maze_ing.components import Node, Palette

class MazeCore:
    def __init__(self, cfg_path: str, use_anim: bool = False):
        self.cfg = Settings(cfg_path)
        self.anim = use_anim
        self.grid = []
        self.seed_val = self.cfg.rng_seed if self.cfg.rng_seed is not None else random.randint(0, 999999)
        random.seed(self.seed_val)
        self.optimal_path = ""
        self._setup_grid()

    def _setup_grid(self) -> None:
        self.grid = [[Node(15, False) for _ in range(self.cfg.cols)] for _ in range(self.cfg.rows)]
        ox, oy = (self.cfg.cols - 7) // 2, (self.cfg.rows - 5) // 2

        if self.cfg.cols >= 7 and self.cfg.rows >= 5:
            shape_42 = [
                (0,0),(0,1),(0,2),(1,2),(2,0),(2,1),(2,2),(2,3),(2,4),
                (4,0),(5,0),(6,0),(6,1),(6,2),(5,2),(4,2),(4,3),(4,4),(5,4),(6,4)
            ]
            for dx, dy in shape_42:
                self.grid[oy + dy][ox + dx].borders = 15
                self.grid[oy + dy][ox + dx].is_locked = True
                self.grid[oy + dy][ox + dx].is_explored = True
        else:
            print("Error: Grid too small for 42 pattern")
            exit(0)

    def _knock_down(self, n: Node, d: str) -> None:
        n.borders &= ~{'N': 1, 'E': 2, 'S': 4, 'W': 8}[d]

    def build_maze(self) -> None:
        sx, sy = self.seed_val % self.cfg.cols, self.seed_val % self.cfg.rows
        while self.grid[sy][sx].is_locked:
            sx = (sx + 1) % self.cfg.cols
            sy = (sy + 1) % self.cfg.rows

        stack = [(sx, sy)]
        self.grid[sy][sx].is_explored = True
        dirs = [(-1, 0, 'W', 'E'), (1, 0, 'E', 'W'), (0, -1, 'N', 'S'), (0, 1, 'S', 'N')]

        while stack:
            cx, cy = stack[-1]
            valid_moves = []
            for dx, dy, d1, d2 in dirs:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < self.cfg.cols and 0 <= ny < self.cfg.rows:
                    if not self.grid[ny][nx].is_explored:
                        valid_moves.append((nx, ny, d1, d2))

            if valid_moves:
                nx, ny, d1, d2 = random.choice(valid_moves)
                self._knock_down(self.grid[cy][cx], d1)
                self._knock_down(self.grid[ny][nx], d2)
                self.grid[ny][nx].is_explored = True
                stack.append((nx, ny))
                if self.anim:
                    self.draw()
                    time.sleep(0.015)
            else:
                stack.pop()

        if not self.cfg.is_perfect:
            self._add_loops()
        
        self._find_shortest_path()

    def _add_loops(self) -> None:
        dirs = [(-1, 0, 'W', 'E'), (1, 0, 'E', 'W'), (0, -1, 'N', 'S'), (0, 1, 'S', 'N')]
        for y in range(self.cfg.rows):
            for x in range(self.cfg.cols):
                if random.random() < 0.1 and not self.grid[y][x].is_locked:
                    cands = []
                    for dx, dy, d1, d2 in dirs:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.cfg.cols and 0 <= ny < self.cfg.rows and not self.grid[ny][nx].is_locked:
                            cands.append((nx, ny, d1, d2))
                    if cands:
                        nx, ny, d1, d2 = random.choice(cands)
                        self._knock_down(self.grid[y][x], d1)
                        self._knock_down(self.grid[ny][nx], d2)

    def _find_shortest_path(self) -> None:
        start = (self.cfg.start_pt['x'], self.cfg.start_pt['y'])
        target = (self.cfg.end_pt['x'], self.cfg.end_pt['y'])
        
        queue = deque([(start[0], start[1], "")])
        visited = {start}
        
        while queue:
            cx, cy, path = queue.popleft()
            if (cx, cy) == target:
                self.optimal_path = path
                return
            
            b = self.grid[cy][cx].borders
            moves = []
            if not (b & 1): moves.append((cx, cy-1, 'N'))
            if not (b & 2): moves.append((cx+1, cy, 'E'))
            if not (b & 4): moves.append((cx, cy+1, 'S'))
            if not (b & 8): moves.append((cx-1, cy, 'W'))
            
            for nx, ny, d in moves:
                if 0 <= nx < self.cfg.cols and 0 <= ny < self.cfg.rows:
                    if (nx, ny) not in visited and not self.grid[ny][nx].is_locked:
                        visited.add((nx, ny))
                        queue.append((nx, ny, path + d))

    def export_to_file(self) -> None:
        with open(self.cfg.out_file, 'w') as f:
            for row in self.grid:
                f.write("".join(f"{n.borders:X}" for n in row) + "\n")
            f.write(f"\n{self.cfg.start_pt['x']},{self.cfg.start_pt['y']}\n")
            f.write(f"{self.cfg.end_pt['x']},{self.cfg.end_pt['y']}\n")
            f.write(self.optimal_path + "\n")

    def draw(self, clr: str = Palette.W.value, char_wall: str = "█", show_sol: bool = False, sol_char: str = " ● ", start_char: str = " ● ", end_char: str = " ● ") -> None:
        os.system('clear')
        path_coords = set()
        
        if show_sol and self.optimal_path:
            cx, cy = self.cfg.start_pt['x'], self.cfg.start_pt['y']
            for step in self.optimal_path:
                if step == 'N': cy -= 1
                elif step == 'S': cy += 1
                elif step == 'E': cx += 1
                elif step == 'W': cx -= 1
                path_coords.add((cx, cy))
        
        print(f"{clr}", end="")
        for y, row in enumerate(self.grid):
            top_line = ""
            mid_line = ""
            for x, node in enumerate(row):
                is_start = (x == self.cfg.start_pt['x'] and y == self.cfg.start_pt['y'])
                is_end = (x == self.cfg.end_pt['x'] and y == self.cfg.end_pt['y'])
                
                if node.borders == 15:
                    indicator = char_wall * 3
                elif is_start:
                    indicator = start_char
                elif is_end:
                    indicator = end_char
                elif show_sol and (x, y) in path_coords:
                    indicator = sol_char
                else:
                    indicator = "   "
                    
                top_line += (char_wall * 4) if node.borders & 1 else f"{char_wall}   "
                left_w = char_wall if node.borders & 8 else " "
                mid_line += f"{left_w}{indicator}"
                
            last_node = row[-1]
            top_line += char_wall
            mid_line += char_wall if last_node.borders & 2 else " "
            
            print(f"{top_line}\n{mid_line}")
        
        bottom_line = ""
        for node in self.grid[-1]:
            bottom_line += (char_wall * 4) if node.borders & 4 else f"{char_wall}   "
        bottom_line += char_wall
        print(f"{bottom_line}{Palette.RST.value}")