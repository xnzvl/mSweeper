from enum import Enum
from typing import Dict, List, Tuple


DEFAULT_MARGIN = 25


class Margins(Enum):
    TOP = DEFAULT_MARGIN
    RIGHT = DEFAULT_MARGIN
    BOTTOM = DEFAULT_MARGIN
    LEFT = DEFAULT_MARGIN


class Shape(Enum):
    MINE = "mine_shape"
    FLAG = "flag_shape"
    STAND = "stand_shape"
    TROPHY_BODY = "trophy_body_shape"
    TROPHY_EARS = "trophy_ears_shape"
    SMILE = "smile_shape"


SW_TITLE = ":: mSweeper _"
SW_VERSION = "1.41"

BOX_A = 90
CELL_SIZE = 40
GAP_SIZE = 30


SHAPE: Dict[Shape, List[int]] = {}
TEMPLATE: Dict[Shape, Tuple[Tuple[int, int], List[int]]] = {
    Shape.MINE:        ((6, 2), [1, 2, 3, -1, -1, 3, 2, 1, -2, 3, 1, -1, -3, 2, -1, -2, -3, 1, 1, -3, -2, -1, 2, -3, -1, 1, 3]),
    Shape.FLAG:        ((4, 3), [1, 1, 3, -1, 1, 5, -1, 1, -3, -1, -1, -5]),
    Shape.STAND:       ((3, 3), [3, -1, 1, 1, 3, 1, -3, 6, 1, 1, -3, -1, 1, -6, -3]),
    Shape.TROPHY_BODY: ((4, 3), [5, 1, 1, 1, -1, 2, -1, 1, -1, 2, 2, 1, -5, -1, 2, -2, -1, -1, -1, -2, -1, -1, 1]),
    Shape.TROPHY_EARS: ((2, 2), [2, 1, 5, -1, 2, 2, -1, -1, -7, 1, -1]),
    Shape.SMILE:       ((2, 7), [2, 1, 5, -1, 2, 2, -2, 1, -5, -1, -2])
}


def init_shapes() -> None:
    def from_template(
        template: List[int],
        x: int,
        y: int
    ) -> List[int]:
        even = True
        shape = []

        shape.append(x)
        shape.append(y)

        for coord in template:
            x += coord if even else 0
            y += coord if not even else 0

            shape.append(x)
            shape.append(y)

            even = not even

        return shape

    global TEMPLATE

    for shape, ((x0, y0), template) in TEMPLATE.items():
        SHAPE[shape] = from_template(template, x0, y0)

    del TEMPLATE
