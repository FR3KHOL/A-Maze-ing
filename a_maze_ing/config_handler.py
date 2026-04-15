import os
from typing import Dict, Optional

class Settings:
    def __init__(self, filepath: str):
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
        
        sx, sy = params['ENTRY'].split(',')
        self.start_pt = {'x': int(sx), 'y': int(sy)}
        
        ex, ey = params['EXIT'].split(',')
        self.end_pt = {'x': int(ex), 'y': int(ey)}
        
        self.out_file = params['OUTPUT_FILE']
        self.is_perfect = params['PERFECT'].upper() == 'TRUE'