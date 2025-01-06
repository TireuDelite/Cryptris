##############################################
#        Made By - Anthony BUFFET            #
#        Made By - Gregoire MONGREDIEN       #
##############################################

import pygame
from ui import Button, draw_input_box
from config import *
import random
import pygame
from config import *
import re

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

def extract_numbers(mot_chiffre):
    numbers = []
    current_number = ""
    

    for char in mot_chiffre:
        if char in '0123456789':  
            current_number += char  
        elif char == '-':  
            if current_number: 
                numbers.append(int(current_number))
            current_number = char  
        elif current_number:  
            numbers.append(int(current_number))
            current_number = ""  

    if current_number:  
        numbers.append(int(current_number))
    

    result = []
    for num in numbers:
        if num < 0:

            result.append(-1)
            result.extend(map(int, str(abs(num))))  
        else:
            result.append(num)
    
    return result

def Victoire():
    victory_image = pygame.image.load("cryptis\\assets\\images\\Victory.png") 
    victory_image = pygame.transform.scale(victory_image, (300, 300))  
    screen.blit(victory_image, (SCREEN_WIDTH // 2 - victory_image.get_width() // 2, SCREEN_HEIGHT // 2 - victory_image.get_height() // 2))
    pygame.display.flip()  

def game_easy(mot, mot_chiffre, cle_avec_bruit):

    grid_width, grid_height = 8, 14
    cell_size = 40  

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    grid_x_offset = (SCREEN_WIDTH - grid_width * cell_size) // 2  
    grid_y_offset = (SCREEN_HEIGHT - grid_height * cell_size) // 2  

    top_row = [None] * grid_width  

    num_values = random.randint(3, 8)

    for i in random.sample(range(grid_width), num_values):
        top_row[i] = random.randint(1, 5)  

    bottom_row = extract_numbers(mot_chiffre)  
    print(bottom_row)

    while len(bottom_row) < grid_width:
        bottom_row.append(0)
    
    bottom_row = bottom_row[:grid_width]

    running = True
    font = pygame.font.Font("cryptis\\assets\\fonts\\slkscrb.ttf", 28)  
    operations = {"add": "+", "sub": "-", "mul": "*", "div": "/"}
    selected_operation = None

    selected_index = None  
    selected_value = None  

    pygame.display.set_caption("Mode Facile")

    while running:
        screen.fill((0, 0, 0))  

        mot_text = font.render(f"Mot : {mot}", True, WHITE)
        screen.blit(mot_text, (10, 10))
        cle_text = font.render(f"Clef avec bruit : {cle_avec_bruit}", True, WHITE)
        screen.blit(cle_text, (10, 50))

        for row in range(grid_height):
            for col in range(grid_width):
                rect_x = grid_x_offset + col * cell_size
                rect_y = grid_y_offset + row * cell_size
                rect = pygame.Rect(rect_x, rect_y, cell_size, cell_size)

                if row == 0:  
                    value = top_row[col]
                    if value is not None:  
                        pygame.draw.rect(screen, (0, 0, 255), rect) 
                        text = font.render(str(value), True, WHITE)
                        screen.blit(text, (rect_x + cell_size // 2 - text.get_width() // 2, rect_y + cell_size // 2 - text.get_height() // 2))
                    else:
                        pygame.draw.rect(screen, (50, 50, 50), rect)  

                elif row == grid_height - 1:  
                    value = bottom_row[col]  
                    if value == cle_avec_bruit[col] or (cle_avec_bruit[col] != 0 and value % cle_avec_bruit[col] == 0):
                        pygame.draw.rect(screen, (0, 255, 0), rect)  
                    else:
                        pygame.draw.rect(screen, (169, 169, 169), rect)  
                    text = font.render(str(value), True, WHITE)
                    screen.blit(text, (rect_x + cell_size // 2 - text.get_width() // 2, rect_y + cell_size // 2 - text.get_height() // 2))

                else:  
                    pygame.draw.rect(screen, (50, 50, 50), rect)  

                pygame.draw.rect(screen, WHITE, rect, 2)  

        for col in range(grid_width):
            value = top_row[col]
            if value is not None:  
                for i in range(1, value):  
                    rect_x = grid_x_offset + col * cell_size
                    rect_y = grid_y_offset + i * cell_size
                    pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(rect_x, rect_y, cell_size, cell_size))
                    pygame.draw.rect(screen, WHITE, pygame.Rect(rect_x, rect_y, cell_size, cell_size), 2)  

        if all(bottom_row[i] == cle_avec_bruit[i] or (cle_avec_bruit[i] != 0 and bottom_row[i] % cle_avec_bruit[i] == 0) for i in range(grid_width)):
            Victoire()  
            

        if selected_operation:
            operation_text = font.render(f"Operation : {operations[selected_operation]}", True, WHITE)
            screen.blit(operation_text, (grid_x_offset, grid_y_offset + grid_height * cell_size + 20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and selected_index is not None and selected_index < grid_width - 1:
                    if top_row[selected_index + 1] is None:
                        top_row[selected_index + 1] = top_row[selected_index]
                        top_row[selected_index] = None
                        selected_index += 1  

                elif event.key == pygame.K_LEFT and selected_index is not None and selected_index > 0:
                    if top_row[selected_index - 1] is None:
                        top_row[selected_index - 1] = top_row[selected_index]
                        top_row[selected_index] = None
                        selected_index -= 1  

                if event.key == pygame.K_RETURN:  
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    for col in range(grid_width):
                        rect_x = grid_x_offset + col * cell_size
                        rect_y = grid_y_offset
                        rect = pygame.Rect(rect_x, rect_y, cell_size, cell_size)
                        if rect.collidepoint(mouse_x, mouse_y):
                            selected_index = col  
                            selected_value = top_row[selected_index] 

                if event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS or event.key == pygame.K_KP_PLUS:  
                    selected_operation = "add"
                elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:  
                    selected_operation = "sub"
                elif event.key == pygame.K_ASTERISK or event.key == pygame.K_KP_MULTIPLY:  
                    selected_operation = "mul"
                elif event.key == pygame.K_SLASH or event.key == pygame.K_KP_DIVIDE:  
                    selected_operation = "div"

                if event.key == pygame.K_SPACE:
                    selected_operation = None  

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                for col in range(grid_width):
                    rect_x = grid_x_offset + col * cell_size
                    rect_y = grid_y_offset
                    rect = pygame.Rect(rect_x, rect_y, cell_size, cell_size)
                    if rect.collidepoint(mouse_x, mouse_y):
                        selected_index = col  
                        selected_value = top_row[selected_index]  

                if selected_operation and selected_index is not None:
                    if selected_operation == "add":
                        bottom_row[selected_index] += selected_value
                    elif selected_operation == "sub":
                        bottom_row[selected_index] -= selected_value
                    elif selected_operation == "mul":
                        bottom_row[selected_index] *= selected_value
                    elif selected_operation == "div" and selected_value != 0:
                        bottom_row[selected_index] //= selected_value

                    num_values = random.randint(3, 8)
                    top_row = [None] * grid_width  

                    for i in random.sample(range(grid_width), num_values):
                        top_row[i] = random.randint(1, 5)  

        pygame.display.flip()
        
def game_hard(mot, mot_chiffre, cle_avec_bruit):
    
    grid_width, grid_height = 8, 14
    cell_size = 40  

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    grid_x_offset = (SCREEN_WIDTH - grid_width * cell_size) // 2  
    grid_y_offset = (SCREEN_HEIGHT - grid_height * cell_size) // 2  

    top_row = [None] * grid_width  

    num_values = random.randint(3, 8)

    for i in random.sample(range(grid_width), num_values):
        top_row[i] = random.randint(1, 5)  

    bottom_row = extract_numbers(mot_chiffre)  
    print(bottom_row)

    while len(bottom_row) < grid_width:
        bottom_row.append(0)
    
    bottom_row = bottom_row[:grid_width]

    running = True
    font = pygame.font.Font("cryptis\\assets\\fonts\\slkscrb.ttf", 28)  
    operations = {"add": "+", "sub": "-", "mul": "*", "div": "/"}
    selected_operation = None

    selected_index = None  
    selected_value = None  

    pygame.display.set_caption("Mode Facile")

    while running:
        screen.fill((0, 0, 0))  

        mot_text = font.render(f"Mot : {mot}", True, WHITE)
        screen.blit(mot_text, (10, 10))

        for row in range(grid_height):
            for col in range(grid_width):
                rect_x = grid_x_offset + col * cell_size
                rect_y = grid_y_offset + row * cell_size
                rect = pygame.Rect(rect_x, rect_y, cell_size, cell_size)

                if row == 0:  
                    value = top_row[col]
                    if value is not None:  
                        pygame.draw.rect(screen, (0, 0, 255), rect) 
                        text = font.render(str(value), True, WHITE)
                        screen.blit(text, (rect_x + cell_size // 2 - text.get_width() // 2, rect_y + cell_size // 2 - text.get_height() // 2))
                    else:
                        pygame.draw.rect(screen, (50, 50, 50), rect)  

                elif row == grid_height - 1:  
                    value = bottom_row[col]  
                    if value == cle_avec_bruit[col] or (cle_avec_bruit[col] != 0 and value % cle_avec_bruit[col] == 0):
                        pygame.draw.rect(screen, (0, 255, 0), rect)  
                    else:
                        pygame.draw.rect(screen, (169, 169, 169), rect)  
                    text = font.render(str(value), True, WHITE)
                    screen.blit(text, (rect_x + cell_size // 2 - text.get_width() // 2, rect_y + cell_size // 2 - text.get_height() // 2))

                else:  
                    pygame.draw.rect(screen, (50, 50, 50), rect)  

                pygame.draw.rect(screen, WHITE, rect, 2)  

        for col in range(grid_width):
            value = top_row[col]
            if value is not None:  
                for i in range(1, value):  
                    rect_x = grid_x_offset + col * cell_size
                    rect_y = grid_y_offset + i * cell_size
                    pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(rect_x, rect_y, cell_size, cell_size))
                    pygame.draw.rect(screen, WHITE, pygame.Rect(rect_x, rect_y, cell_size, cell_size), 2)  

        if all(bottom_row[i] == cle_avec_bruit[i] or (cle_avec_bruit[i] != 0 and bottom_row[i] % cle_avec_bruit[i] == 0) for i in range(grid_width)):
            Victoire()  
            

        if selected_operation:
            operation_text = font.render(f"Operation : {operations[selected_operation]}", True, WHITE)
            screen.blit(operation_text, (grid_x_offset, grid_y_offset + grid_height * cell_size + 20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and selected_index is not None and selected_index < grid_width - 1:
                    if top_row[selected_index + 1] is None:
                        top_row[selected_index + 1] = top_row[selected_index]
                        top_row[selected_index] = None
                        selected_index += 1  

                elif event.key == pygame.K_LEFT and selected_index is not None and selected_index > 0:
                    if top_row[selected_index - 1] is None:
                        top_row[selected_index - 1] = top_row[selected_index]
                        top_row[selected_index] = None
                        selected_index -= 1  

                if event.key == pygame.K_RETURN:  
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    for col in range(grid_width):
                        rect_x = grid_x_offset + col * cell_size
                        rect_y = grid_y_offset
                        rect = pygame.Rect(rect_x, rect_y, cell_size, cell_size)
                        if rect.collidepoint(mouse_x, mouse_y):
                            selected_index = col  
                            selected_value = top_row[selected_index] 

                if event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS or event.key == pygame.K_KP_PLUS:  
                    selected_operation = "add"
                elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:  
                    selected_operation = "sub"
                elif event.key == pygame.K_ASTERISK or event.key == pygame.K_KP_MULTIPLY:  
                    selected_operation = "mul"
                elif event.key == pygame.K_SLASH or event.key == pygame.K_KP_DIVIDE:  
                    selected_operation = "div"

                if event.key == pygame.K_SPACE:
                    selected_operation = None  

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                for col in range(grid_width):
                    rect_x = grid_x_offset + col * cell_size
                    rect_y = grid_y_offset
                    rect = pygame.Rect(rect_x, rect_y, cell_size, cell_size)
                    if rect.collidepoint(mouse_x, mouse_y):
                        selected_index = col  
                        selected_value = top_row[selected_index]  

                if selected_operation and selected_index is not None:
                    if selected_operation == "add":
                        bottom_row[selected_index] += selected_value
                    elif selected_operation == "sub":
                        bottom_row[selected_index] -= selected_value
                    elif selected_operation == "mul":
                        bottom_row[selected_index] *= selected_value
                    elif selected_operation == "div" and selected_value != 0:
                        bottom_row[selected_index] //= selected_value

                    num_values = random.randint(3, 8)
                    top_row = [None] * grid_width  

                    for i in random.sample(range(grid_width), num_values):
                        top_row[i] = random.randint(1, 5)  

        pygame.display.flip()