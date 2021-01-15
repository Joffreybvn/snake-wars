
import pygame
from typing import List, Dict
from snake_wars.client.entities import Snake, Food
from snake_wars.commons import Size


class Renderer:
    """PyGame renderer."""

    def __init__(self, screen_size: Size, grid_size: Size):

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

    def __math_cell_size(self) -> Size:
        """
        Math and return the size of a cell from the size of the
        window and the size of the grid.
        """

        return Size(
            self.screen_size.width // self.grid_size.width,
            self.screen_size.height // self.grid_size.height
        )

    def render(self, snakes: List[Snake], foods: Dict[tuple, Food]):
        self.__draw_grid()
        self.__draw_foods(foods)
        self.__draw_snakes(snakes)

        # text = self.myfont.render("Score {0}".format(snake.score), 1, (0, 0, 0))
        self.screen.blit(self.surface, (0, 0))
        pygame.display.update()

    def __draw_grid(self):

        for h in range(0, self.grid_size.height):
            for w in range(0, self.grid_size.width):

                rect = pygame.Rect(
                    (w * self.cell_size.width, h * self.cell_size.height),
                    (self.screen_size.width, self.screen_size.height)
                )

                if (w + h) % 2 == 0:
                    pygame.draw.rect(self.surface, (93, 216, 228), rect)
                else:
                    pygame.draw.rect(self.surface, (84, 194, 205), rect)

    def __draw_snakes(self, snakes: List[Snake]):

        for snake in snakes:
            for loc in snake.positions:

                rect = pygame.Rect(
                    loc.x * self.cell_size.width,
                    loc.y * self.cell_size.height,
                    self.cell_size.width,
                    self.cell_size.height
                )

                pygame.draw.rect(self.surface, snake.color, rect)
                pygame.draw.rect(self.surface, (93, 216, 228), rect, 1)

    def __draw_foods(self, foods: Dict[tuple, Food]):

        for location, food in foods.items():

            rect = pygame.Rect(
                location[0] * self.cell_size.width,
                location[1] * self.cell_size.height,
                self.cell_size.width,
                self.cell_size.height
            )

            pygame.draw.rect(self.surface, food.color, rect)
            pygame.draw.rect(self.surface, (93, 216, 228), rect, 1)
