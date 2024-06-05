import pygame

class UI:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)

    def update(self):
        self.screen.fill((255, 255, 255))  # White background
        self.draw_text("Press C to create a new student", 50, 50)
        self.draw_text("Press A to add an existing student to a class", 50, 100)
        self.draw_text("Press D to delete a student", 50, 150)
        self.draw_text("Press U to update a student's score", 50, 200)
        self.draw_text("Press V to view the average score of a class for a specific subject", 50, 250)

    def draw_text(self, text, x, y):
        text_surface = self.font.render(text, True, (0, 0, 0))
        self.screen.blit(text_surface, (x, y))
