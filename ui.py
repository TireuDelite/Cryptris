import pygame
from config import BUTTON_COLOR, BUTTON_HOVER_COLOR, WHITE

class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.action = action
        self.color = BUTTON_COLOR
        self.hover_color = BUTTON_HOVER_COLOR
        self.font = pygame.font.SysFont("Arial", 36)

    def draw(self, surface):
        
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))

        
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        surface.blit(text_surface, text_rect)

    def check_hover(self, mouse_pos):
        
        if self.x <= mouse_pos[0] <= self.x + self.width and self.y <= mouse_pos[1] <= self.y + self.height:
            self.color = self.hover_color  
        else:
            self.color = BUTTON_COLOR 

    def check_click(self, mouse_pos):
        if self.x <= mouse_pos[0] <= self.x + self.width and self.y <= mouse_pos[1] <= self.y + self.height:
            if self.action:
                self.action()  

def draw_input_box(surface, text, x, y, width, height, font, color):

    input_box = pygame.Rect(x, y, width, height)
    pygame.draw.rect(surface, color, input_box, 2)

    txt_surface = font.render(text, True, color)
    surface.blit(txt_surface, (x + 5, y + 5))
    
    return input_box