import pygame_gui
import pygame

class UIManager:
    def __init__(self, width, height):
        self.manager = pygame_gui.UIManager((width, height))

        self.num_birds_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((10, 10), (200, 30)),
            start_value=30,
            value_range=(10, 32),
            manager=self.manager
        )
        self.speed_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((10, 50), (200, 30)),
            start_value=5,
            value_range=(1, 10),
            manager=self.manager
        )
        self.add_predator_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, 90), (200, 30)),
            text='Add Predator',
            manager=self.manager
        )

    def process_events(self, event):
        self.manager.process_events(event)

    def update(self, time_delta):
        self.manager.update(time_delta)

    def draw_ui(self, window):
        self.manager.draw_ui(window)
