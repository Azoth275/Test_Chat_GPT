class Plateau:
    """Square grid plateau where the rover operates."""

    def __init__(self, width, height, obstacles=None):
        self.width = width
        self.height = height
        self.obstacles = set(obstacles or [])

    def is_within_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def is_free(self, x, y):
        return self.is_within_bounds(x, y) and (x, y) not in self.obstacles
