import pygame
import random
import pygame_gui
from bird import Bird
from predator import Predator
from boundary import Boundary
from UIManager import UIManager
from collections import deque

class Simulation:
    """
    Represents the main simulation for the bird flocking behavior and predator interaction.
    """

    def __init__(self, width, height):
        """
        Initialize the simulation with a given window width and height.
        Sets up the display, clock, UI manager, and bird group.
        """
        self.Width, self.Height = width, height
        self.window = pygame.display.set_mode((self.Width, self.Height), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.scale = 10
        self.Distance = 5

        self.ui_manager = UIManager(self.Width, self.Height)

        self.group = []  # List of birds in the simulation
        self.n = 30  # Initial number of birds
        self.bird_max_speed = 3.5
        self.predator = None

        # Create the initial group of birds
        for i in range(self.n):
            self.group.append(Bird(random.randint(20, self.Width - 20), random.randint(20, self.Height - 20)))

    def run(self):
        """
        Run the main simulation loop.
        Handles events, updates UI, updates and draws birds and predators, and manages collisions.
        """
        run = True
        while run:
            time_delta = self.clock.tick(self.fps) / 1000.0  # Time delta for frame rate control

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False  # Exit the loop if the quit event is detected

                # Handle slider events for adjusting number of birds and bird speed
                if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                    if event.ui_element == self.ui_manager.num_birds_slider:
                        self.n = int(event.value)
                        self.group = [Bird(random.randint(20, self.Width - 20), random.randint(20, self.Height - 20))
                                      for _ in range(self.n)]
                    if event.ui_element == self.ui_manager.speed_slider:
                        self.bird_max_speed = event.value
                        for bird in self.group:
                            bird.maxSpeed = self.bird_max_speed
                        if self.predator:
                            self.predator.max_speed = self.bird_max_speed * 0.8

                # Handle button event for adding a predator
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.ui_manager.add_predator_button:
                        self.predator = Predator(random.randint(20, self.Width - 20),
                                                 random.randint(20, self.Height - 20),
                                                 self.bird_max_speed)  # Initialize with bird_max_speed

                self.ui_manager.process_events(event)

            self.ui_manager.update(time_delta)  # Update UI elements
            self.window.fill((10, 10, 15))  # Clear the window

            # Update and draw the predator if it exists
            if self.predator:
                self.predator.update([bird.position for bird in self.group])
                self.predator.draw(self.window)

            # Update and draw each bird in the group
            for obj in self.group:
                obj.boundary = Boundary(0, self.Width, 0, self.Height)
                obj.update(self.group, self.predator)
                obj.draw(self.window, self.Distance, self.scale)

            # Check for collisions between birds and the predator
            if self.predator:
                bird_queue = deque(self.group)
                while bird_queue:
                    bird = bird_queue.popleft()
                    if (bird.position - self.predator.position).length() <= 10:  # Adjust collision distance as needed
                        self.group.remove(bird)
                        # No break here to allow multiple collisions to be checked

            self.ui_manager.draw_ui(self.window)  # Draw the UI elements
            pygame.display.flip()  # Update the display

        pygame.quit()  # Quit Pygame when the loop ends


if __name__ == "__main__":
    pygame.init()
    simulation = Simulation(960, 540)  # Initialize the simulation with a window size of 960x540
    simulation.run()  # Run the simulation
