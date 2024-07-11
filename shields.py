import pygame

class Block(pygame.sprite.Sprite):
    """Block to create the shields"""

    def __init__(self, x, y):
        """Initializes the class to fill the image up"""
        super().__init__()
        self.image = pygame.Surface((3, 3))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect(topleft=(x, y))

def generate_grid(rows, columns):
    """Generates a grid pattern for the shields."""
    grid = []
    for _ in range(rows):
        grid.append([1] * columns)
    return grid

class Obstacle:
    """Creates the shield obstacle."""

    def __init__(self, x, y, rows=5, columns=18):
        """initializes them into a group."""
        self.block_group = pygame.sprite.Group()
        self.grid = generate_grid(rows, columns)
        self.create_blocks(x, y)

    def create_blocks(self, x, y):
        """This function draws the block in the right spots."""
        for row, row_values in enumerate(self.grid):
            for column, cell in enumerate(row_values):
                if cell == 1:
                    pos_x = x + column * 3
                    pos_y = y + row * 3
                    block = Block(pos_x, pos_y)
                    self.block_group.add(block)

