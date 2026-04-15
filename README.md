*This project has been created as part of the 42 curriculum by hilyas, isiboub.*

# A-Maze-Ing

## Description
A-Maze-Ing is a highly customizable and interactive maze generator and solver written in Python. It parses a configuration file to construct mazes of varying dimensions, optionally ensuring they are "perfect" (only one valid path). The project emphasizes modularity, clean code structure, and visualization, featuring an interactive terminal UI with customizable emoji themes, live generation animations, and a shortest-path solver. It also exports the generated maze data into a structured hexadecimal file format.

---

## Instructions

### Requirements
- Python >= 3.10
- Optional development tools: `flake8`, `mypy`

### Installation
Clone the repository and install the required dependencies (linters/type checkers) using the provided Makefile:

```bash
make install
```

### Execution
Run the interactive generator using the Makefile or directly via Python:

```bash
make run
# Or directly:
python3 a_maze_ing.py config.txt
```

### Available Make Commands
- `make run` : Runs the main program.
- `make lint` : Runs strict code analysis using `flake8` and `mypy`.
- `make debug` : Runs the script using the Python debugger (`pdb`).
- `make package` : Builds the reusable `mazegen` package (`.tar.gz` and `.whl`).
- `make clean` : Cleans up build artifacts, caches, and packaged files.

---

## Configuration File Format
The program is driven by a configuration file. It must contain one `KEY=VALUE` pair per line. Lines starting with `#` are ignored as comments.

Example `config.txt`:
```text
WIDTH=25
HEIGHT=9
ENTRY=0,0
EXIT=24,8
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
```

### Key Descriptions:
* `WIDTH` / `HEIGHT`: Dimensions of the maze grid (Width must be $\ge$ 9, Height $\ge$ 7 to accommodate the mandatory "42" pattern).
* `ENTRY` / `EXIT`: The `x,y` coordinates for the start and finish points.
* `OUTPUT_FILE`: The destination path for the hexadecimal exported maze.
* `PERFECT`: `True` ensures a single valid path. `False` introduces random loops and multiple paths.
* `SEED`: (Optional) An integer used to ensure deterministic maze generation.

---

## Chosen Maze Algorithm
* **Algorithm:** Randomized Iterative Depth-First Search (DFS) for generation, and Breadth-First Search (BFS) for solving.
* **Reason for choice:** An *iterative* DFS approach was chosen over recursion to completely bypass Python's recursion depth limits, preventing crashes on massive grids while naturally producing long, winding corridors. BFS was chosen for the solver because it systematically explores all nodes level-by-level, mathematically guaranteeing the discovery of the absolute shortest path between the entry and exit points.

---

## Code Reusability Requirements
The maze generation logic is entirely encapsulated within the `mazegen` module, making it highly portable. 

To use the generator in another project, install the built package (`pip install mazegen-1.0.0.tar.gz`) and import `MazeCore`:

```python
from mazegen.maze import MazeCore
from mazegen.components import Palette

# Instantiate the core generator with a config file
maze = MazeCore("config.txt", use_anim=False)

# Build the maze and solve it
maze.build_maze()

# Draw the maze to the terminal (customizing walls and emojis)
maze.draw(clr=Palette.W.value, char_wall="██", show_sol=True, sol_char="··", start_char="🟢", end_char="🔴")

# Export the maze structure and shortest path to the configured output file
maze.export_to_file()
```

---

## Team & Project Management

### Roles
* **isiboub:** Project initialization, interactive terminal display, ASCII/Emoji graphics rendering, output file formatting, and packaging (`setup.py` / `pyproject.toml`).
* **hilyas:** Algorithm implementation (Iterative DFS & BFS queue), custom configuration parser, data structures, and Makefile automation.

### Planning & Evolution
Our initial approach focused purely on getting a recursive DFS algorithm working. As the project scaled, we hit recursion depth limits, prompting a complete architectural refactor to an iterative stack-based approach. We also evolved the rendering engine from basic ASCII to supporting dynamically aligned, continuous emoji walls.

### What Worked Well & Areas for Improvement
* **Worked well:** Separating the underlying data structure (`components.py` and `config_handler.py`) from the visualization loop allowed us to rapidly test new visual themes without breaking the generation logic.
* **To improve:** Expanding the visualizer to support a graphical window using MiniLibX (MLX) or Pygame would be an exciting next step.

---

## Tools Used
* **Python 3.10+**: Core language utilizing `match-case` and modern type hinting.
* **flake8 & mypy**: Used strictly for static analysis to ensure code quality.
* **setuptools**: Utilized to compile the module into a standalone wheel/tar package.

---

## Resources
* Python Official Documentation (specifically the `collections.deque` and `enum` modules).
* Wikipedia articles on Graph Theory and Maze Generation Algorithms.
* **AI Usage:** AI assistance was strictly used for just deepening understanding of algorithms and providing explanations of some functions.

---

## Advanced Features
* **Interactive UI Loop:** A live menu allows users to regenerate mazes, toggle the solution path, and export data without restarting the script.
* **Dynamic Emoji Themes:** The rendering engine supports 10 distinct, perfectly aligned themes (e.g., Mouse/Cheese, Astronaut/Earth, Zombie/Brain) with continuous emoji walls.
* **Live Animation:** Users can toggle an animation mode to visually watch the DFS algorithm carve the maze in real-time.