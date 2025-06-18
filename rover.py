from plateau import Plateau

# Orientation order for turning
_ORIENTATIONS = ['N', 'E', 'S', 'W']

# Movement deltas for orientations
_MOVE = {
    'N': (0, 1),
    'E': (1, 0),
    'S': (0, -1),
    'W': (-1, 0),
}

class Rover:
    """A rover that moves on a plateau while avoiding obstacles."""

    def __init__(self, plateau: Plateau, x: int = 0, y: int = 0, direction: str = 'N'):
        if direction not in _ORIENTATIONS:
            raise ValueError(f"Invalid direction {direction}")
        if not plateau.is_free(x, y):
            raise ValueError("Starting position is not free")
        self.plateau = plateau
        self.x = x
        self.y = y
        self.direction = direction
        # flag to prevent diagonal moves around obstacles
        self._skip_next_forward = False

    def _index(self) -> int:
        return _ORIENTATIONS.index(self.direction)

    def _blocked_ahead(self) -> bool:
        dx, dy = _MOVE[self.direction]
        nx, ny = self.x + dx, self.y + dy
        return not self.plateau.is_free(nx, ny)

    def turn_left(self):
        if self._blocked_ahead():
            self._skip_next_forward = True
        idx = (self._index() - 1) % 4
        self.direction = _ORIENTATIONS[idx]

    def turn_right(self):
        if self._blocked_ahead():
            self._skip_next_forward = True
        idx = (self._index() + 1) % 4
        self.direction = _ORIENTATIONS[idx]

    def forward(self):
        if self._skip_next_forward:
            # skip this move once to prevent diagonal bypass
            self._skip_next_forward = False
            return False
        dx, dy = _MOVE[self.direction]
        nx, ny = self.x + dx, self.y + dy
        if self.plateau.is_free(nx, ny):
            self.x, self.y = nx, ny
            return True
        return False

    def execute_commands(self, commands):
        """Execute a sequence of commands.

        Commands should be an iterable containing 'L', 'R', or 'F'.
        """
        for cmd in commands:
            if cmd == 'L':
                self.turn_left()
            elif cmd == 'R':
                self.turn_right()
            elif cmd == 'F':
                self.forward()
            else:
                raise ValueError(f"Unknown command {cmd}")
        return self.x, self.y, self.direction
