import unittest
from plateau import Plateau
from rover import Rover

class RoverTestCase(unittest.TestCase):
    def test_forward_blocked_by_obstacle(self):
        p = Plateau(3, 3, obstacles={(1, 2)})
        r = Rover(p, 1, 1, 'N')
        moved = r.forward()
        self.assertFalse(moved)
        self.assertEqual((r.x, r.y, r.direction), (1, 1, 'N'))

    def test_no_diagonal_move_via_lf(self):
        p = Plateau(3, 3, obstacles={(1, 2)})
        r = Rover(p, 1, 1, 'N')
        r.execute_commands('L')
        r.execute_commands('F')
        # forward should have been skipped due to obstacle ahead before turning
        self.assertEqual((r.x, r.y, r.direction), (1, 1, 'W'))

    def test_move_after_skipped_forward(self):
        p = Plateau(4, 4, obstacles={(1, 2)})
        r = Rover(p, 1, 1, 'N')
        r.execute_commands('L')  # sets skip flag
        r.execute_commands('F')  # skipped
        r.execute_commands('F')  # this should move west
        self.assertEqual((r.x, r.y, r.direction), (0, 1, 'W'))

if __name__ == '__main__':
    unittest.main()
