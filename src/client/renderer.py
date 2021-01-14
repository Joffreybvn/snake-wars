
import pygame
from typing import List
from src.commons import Snake, Food
from src.commons.utils import Coordinates


class Renderer:
    """PyGame renderer."""

    def __init__(self, screen_size: Coordinates, grid_size: Coordinates):

        # Store the screen size, game grid size, and math the size of a cell
        self.screen_size = screen_size
        self.grid_size = grid_size
        self.cell_size = self.__math_cell_size()

        # Init a pygame window
        pygame.init()

        # PyGame related values
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(screen_size.tuple(), 0, 32)

        self.surface = pygame.Surface(self.screen.get_size()).convert()
        self.font = pygame.font.SysFont("monospace", 16)

    def start(self):
        self.__draw_grid()

    def __math_cell_size(self) -> Coordinates:
        """
        Math and return the size of a cell from the size of the
        window and the size of the grid.
        """

        return Coordinates(
            self.screen_size.x // self.grid_size.x,
            self.screen_size.y // self.grid_size.y
        )

    def render(self, snakes: List[Snake], foods: List[Food]):
        self.__draw_grid()
        self.__draw_foods(foods)
        self.__draw_snakes(snakes)

        # text = self.myfont.render("Score {0}".format(snake.score), 1, (0, 0, 0))
        self.screen.blit(self.surface, (0, 0))
        pygame.display.update()

    def __draw_grid(self):

        for y in range(0, self.grid_size.y):
            for x in range(0, self.grid_size.x):

                rect = pygame.Rect(
                    (x * self.cell_size.x, y * self.cell_size.y),
                    (self.screen_size.x, self.screen_size.y)
                )

                if (x + y) % 2 == 0:
                    pygame.draw.rect(self.surface, (93, 216, 228), rect)
                else:
                    pygame.draw.rect(self.surface, (84, 194, 205), rect)

    def __draw_snakes(self, snakes: List[Snake]):

        for snake in snakes:
            for pos in snake.positions:

                rect = pygame.Rect(
                    pos.x * self.cell_size.x,
                    pos.y * self.cell_size.y,
                    self.cell_size.x,
                    self.cell_size.y
                )

                pygame.draw.rect(self.surface, snake.color, rect)
                pygame.draw.rect(self.surface, (93, 216, 228), rect, 1)

    def __draw_foods(self, foods: List[Food]):

        for food in foods:

            rect = pygame.Rect(
                food.position.x * self.cell_size.x,
                food.position.y * self.cell_size.y,
                self.cell_size.x,
                self.cell_size.y
            )

            pygame.draw.rect(self.surface, food.color, rect)
            pygame.draw.rect(self.surface, (93, 216, 228), rect, 1)
