import pygame
from collections import deque

class Predator:
    """
    Represents the predator in the simulation that chases birds.
    """
    def __init__(self, x, y, max_speed):
        """
        Initialize the predator with a starting position and a maximum speed.

        Args:
            x (float): The initial x-coordinate of the predator.
            y (float): The initial y-coordinate of the predator.
            max_speed (float): The maximum speed of the predator.
        """
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.max_speed = max_speed * 0.8  # Predator's speed is 80% of the bird's maximum speed
        self.history = deque(maxlen=50)  # History of positions for drawing the trail

    def update(self, target_positions):
        """
        Update the predator's position to chase the target positions.

        Args:
            target_positions (list): List of target positions (birds) to chase.
        """
        if target_positions:
            # Chase the nearest bird
            target = min(target_positions, key=lambda pos: (pos - self.position).length())
            direction = (target - self.position).normalize() * self.max_speed
            self.position += direction
            self.history.append(self.position)

    def draw(self, screen):
        """
        Draw the predator on the screen.

        Args:
            screen (pygame.Surface): The surface to draw the predator on.
        """
        pygame.draw.circle(screen, (255, 0, 0), (int(self.position.x), int(self.position.y)), 10)
        # Optionally draw the predator's trail
        for pos in self.history:
            pygame.draw.circle(screen, (255, 0, 0), (int(pos.x), int(pos.y)), 3)
