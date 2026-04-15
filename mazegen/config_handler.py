"""Configuration parsing module for the maze generator."""
import os
from typing import Dict, Optional


class Settings:
    """Handles parsing and validating the maze configuration file."""

    def __init__(self, filepath: str) -> None:
        """Initialize and parse the configuration file.

        Args:
            filepath (str): Path to the configuration file.
        """
        self.filepath = filepath
        self.cols: int = 0
        self.rows: int = 0
        self.start_pt: Dict[str, int] = {}
        self.end_pt: Dict[str, int] = {}
        self.out_file: str = ""
        self.is_perfect: bool = True
        self.rng_seed: Optional[int] = None
        self._extract_data()

    def _extract_data(self) -> None:
        """Extract and validate parameters from the configuration file.

        Raises:
            FileNotFoundError: If the config file does not exist.
            ValueError: If parameters are invalid or out of bounds.
        """
        if not os.path.exists(self.filepath):
            raise FileNotFoundError()

        params = {}
        with open(self.filepath, 'r') as file_obj:
            for text in file_obj:
                text = text.strip()
                if not text or text.startswith('#'):
                    continue
                k, v = text.split('=', 1)
                params[k.strip().upper()] = v.strip()

        self.rng_seed = int(params['SEED']) if 'SEED' in params else None
        self.cols = int(params['WIDTH'])
        self.rows = int(params['HEIGHT'])

        if self.cols < 2 or self.rows < 2:
            raise ValueError("Maze size too small (min 2x2).")

        sx, sy = params['ENTRY'].split(',')
        self.start_pt = {'x': int(sx), 'y': int(sy)}

        ex, ey = params['EXIT'].split(',')
        self.end_pt = {'x': int(ex), 'y': int(ey)}

        if not (0 <= self.start_pt['x'] < self.cols):
            raise ValueError("ENTRY x coordinate is out of bounds.")
        if not (0 <= self.start_pt['y'] < self.rows):
            raise ValueError("ENTRY y coordinate is out of bounds.")

        if not (0 <= self.end_pt['x'] < self.cols):
            raise ValueError("EXIT x coordinate is out of bounds.")
        if not (0 <= self.end_pt['y'] < self.rows):
            raise ValueError("EXIT y coordinate is out of bounds.")

        if self.start_pt == self.end_pt:
            raise ValueError("ENTRY and EXIT cannot be the same point.")

        self.out_file = params['OUTPUT_FILE']
        self.is_perfect = params['PERFECT'].upper() == 'TRUE'
