from typing import Tuple, Iterable, List

from src.position import Position
from src.utils.group import group
from src.world_map import WorldMap


RED = "\033[91m"
GREEN = "\033[92m"
ENDC = "\033[0m"


class ColorGenerator:
    def __init__(self):
        self.colors = [GREEN, RED]
        self.call_count = 0

    def __call__(self):
        self.call_count += 1
        return self.colors[self.call_count % len(self.colors)]


class ConsoleWorldMap(WorldMap):
    def __init__(self):
        self.elements = []

    def add_element(self, element: Tuple[str, Position]):
        self.elements.append(element)

    def display(self):
        color_generator = ColorGenerator()
        grouped_elements = group(self.elements, key=lambda element: element[0])
        grouped_elements_by_color = list(
            map(lambda element: (color_generator(), element[1]), grouped_elements)
        )
        self._print_abscissa()
        for y in range(self.top_left_corner.y, self.bottom_right_corner.y + 1):
            self._print_row(y, grouped_elements_by_color)
            print(20 * "-")

    def _print_abscissa(self):
        line = " |"
        for x in range(self.top_left_corner.x, self.bottom_right_corner.x + 1):
            line += f"{x}|"
        print(line)

    def _print_row(
        self,
        y: int,
        grouped_elements_by_color: Iterable[Tuple[str, List[Tuple[str, Position]]]],
    ):
        line = f"{y}|"
        for x in range(self.top_left_corner.x, self.bottom_right_corner.x + 1):
            color = self.get_color_at(Position(x, y), grouped_elements_by_color)
            line += f"{color}o{ENDC}|"
        print(line)

    def get_color_at(
        self,
        position: Position,
        grouped_elements: Iterable[Tuple[str, List[Tuple[str, Position]]]],
    ) -> str:
        for color, elements in grouped_elements:
            for element in elements:
                if position == element[1]:
                    return color
        return ENDC

    @property
    def top_left_corner(self) -> Position:
        min_x = min(self.elements, key=lambda element: element[1].x)
        min_y = min(self.elements, key=lambda element: element[1].y)
        return Position(min_x[1].x, min_y[1].y)

    @property
    def bottom_right_corner(self) -> Position:
        max_x = max(self.elements, key=lambda element: element[1].x)
        max_y = max(self.elements, key=lambda element: element[1].y)
        return Position(max_x[1].x, max_y[1].y)
