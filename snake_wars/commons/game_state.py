
from dataclasses import dataclass
from typing import Tuple, Dict
import numpy as np


@dataclass
class GameState:

    head: Tuple[int, int]
    surroundings: Dict[str, Tuple[int, int]]
    direction: Dict[str, bool]
    foods: np.array
