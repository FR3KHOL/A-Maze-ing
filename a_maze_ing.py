"""Entry point for the A-Maze-Ing generator application."""
import sys
from mazegen.maze import MazeCore
from mazegen.components import Palette


def run_app() -> None:
    """Initialize and run the interactive terminal application."""
    src_file = sys.argv[1] if len(sys.argv) > 1 else 'config.txt'
    show_anim = False
    is_solved = False

    themes = [
        (" 🟢", " 🔴", "🔹", "█", Palette.W.value),
        (" 🐁", " 🧀", " 🐾", "*", Palette.Y.value),
        (" 🤠", " 💰", " 👣", "▀", Palette.BR.value),
        (" 🚀", " 🌍", " ✨", "@", Palette.B.value),
        (" 🧟", " 🧠", " 🩸", "■", Palette.G.value),
        (" 🧙", " 📜", " 🔮", "#", Palette.M.value),
        (" 🐶", " 🦴", " 🐾", "+", Palette.C.value),
        (" 🏎️ ", " 🏁", " 💨", "0", Palette.R.value)
    ]
    theme_idx = 0

    try:
        app = MazeCore(src_file, show_anim)
        app.build_maze()
    except Exception as err:
        print(f"Failed to boot: {err}")
        return

    while True:
        c_start, c_end, c_path, c_wall, c_color = themes[theme_idx]
        app.draw(
            clr=c_color,
            char_wall=c_wall,
            show_sol=is_solved,
            sol_char=c_path,
            start_char=c_start,
            end_char=c_end
        )

        print(
            f"\n{Palette.W.value}=== Maze Gen "
            f"(Current Seed: {app.seed_val}) ==="
        )
        print("1. New Maze")
        print("2. Toggle Solution")
        print("3. Swap Theme (Style, Emojis & Color)")
        print(f"4. Toggle Anim ({'ON' if show_anim else 'OFF'})")
        print("5. Export Hex File")
        print("0. Exit")

        try:
            cmd = input("\nSelect [0-5]: ").strip()
            match cmd:
                case '1':
                    app = MazeCore(src_file, show_anim)
                    app.build_maze()
                    is_solved = False
                case '2':
                    is_solved = not is_solved
                case '3':
                    theme_idx = (theme_idx + 1) % len(themes)
                case '4':
                    show_anim = not show_anim
                    app.anim = show_anim
                case '5':
                    app.export_to_file()
                    print(f"Saved successfully to {app.cfg.out_file}")
                    input("Press Enter to continue...")
                case '0':
                    break
                case _:
                    pass
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    run_app()
