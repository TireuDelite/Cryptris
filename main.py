##############################################
#        Made By - Anthony BUFFET            #
#        Made By - Gregoire MONGREDIEN       #
##############################################


import pygame
import sys

from ui import Button, draw_input_box
from config import *
from crypto import *
from assets.images import *
from game import game_easy, game_hard

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Cryptis")
pygame.mixer.music.load("cryptis\\assets\\sound\\FE!N.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.005)

background = pygame.image.load("cryptis\\assets\\images\\Fond.png")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))



def main_menu():
    running = True
    start_button = Button(500, 260, 200, 50, "Nouvelle Partie", choose_word)
    credits_button = Button(500, 360, 200, 50, "Credits", credits_menu)  
    quit_button = Button(500, 460, 200, 50, "Quitter", quit_game)

    while running:
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    start_button.check_click(pygame.mouse.get_pos())
                    credits_button.check_click(pygame.mouse.get_pos())  
                    quit_button.check_click(pygame.mouse.get_pos())

        mouse_pos = pygame.mouse.get_pos()
        start_button.check_hover(mouse_pos)
        credits_button.check_hover(mouse_pos)
        quit_button.check_hover(mouse_pos)

        start_button.draw(screen)
        credits_button.draw(screen)
        quit_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.mixer.music.stop()
    pygame.quit()

def choose_word():
    running = True
    word_input = ""
    mot_chiffre = ""  
    cle_avec_bruit = []  
    font = pygame.font.Font("cryptis\\assets\\fonts\\slkscrb.ttf", 30)
    color_inactive = pygame.Color('lightblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    input_box = pygame.Rect(50, 150, 300, 50)
    active = False

    choose_background = pygame.image.load("cryptis\\assets\\images\\Fond_choix_mot.png")
    choose_background = pygame.transform.scale(choose_background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    text_font = pygame.font.Font("cryptis\\assets\\fonts\\slkscrb.ttf", 30)
    text = text_font.render("Entrez un mot qui sera chiffre :", True, (255, 255, 255))
    text2_font = pygame.font.Font("cryptis\\assets\\fonts\\slkscrb.ttf", 30)
    text2 = text2_font.render("Voici votre mot chiffre :", True, (255, 255, 255))
    mot_font = pygame.font.Font("cryptis\\assets\\fonts\\slkscrb.ttf", 30)

    play_button = Button(500, 400, 200, 50, "Jouer", lambda: difficulty(word_input, mot_chiffre, cle_avec_bruit))

    while running:
        screen.blit(choose_background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = True
                else:
                    active = False
                color = color_active if active else color_inactive

                if play_button.check_click(event.pos):
                    print("Bouton 'Jouer' clique.")
                    difficulty()  

            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        try:
                            cle_encodage_bayesien = apply_bayesian_encoding([-1, 6, 8, 0, -2, -1, 7, 7])
                            cle_avec_bruit = apply_noise_to_key(cle_encodage_bayesien)
                            mot_chiffre = "".join(
                                ["".join(map(str, x)) for x in mot_to_ternaire(word_input.upper(), generate_ternary_table())]
                            )
                        except KeyError:
                            mot_chiffre = "Caractre invalide!"
                        print(f"Mot choisi : {word_input}, Mot chiffre : {mot_chiffre}, Cle : {cle_avec_bruit}")
                    elif event.key == pygame.K_BACKSPACE:
                        word_input = word_input[:-1]
                    else:
                        word_input += event.unicode

        screen.blit(text, (50, 100))
        screen.blit(text2, (50, 250))
        draw_input_box(screen, word_input, 50, 150, 300, 50, font, color)

        if mot_chiffre:  
            ternary_representation = mot_to_ternaire(word_input, generate_ternary_table())
            ternary_string = ' '.join(''.join(map(str, group)) for group in ternary_representation)
            mot = mot_font.render(ternary_string, True, (255, 255, 255))
            screen.blit(mot, (50, 300))

        play_button.draw(screen)
        play_button.check_hover(pygame.mouse.get_pos())

        pygame.display.flip()
        clock.tick(60)


def difficulty(word_input, mot_chiffre, cle_avec_bruit):
    running = True

    title_font = pygame.font.Font("cryptis\\assets\\fonts\\slkscrb.ttf", 40)
    background = pygame.image.load("cryptis\\assets\\images\\difficulty.png")
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    title = title_font.render("Choisissez votre difficulte", True, (255, 255, 255))
    easy_button = Button(500, SCREEN_HEIGHT - 220, 200, 50, "Facile", lambda: game_easy(word_input, mot_chiffre, cle_avec_bruit))
    hard_button = Button(500, SCREEN_HEIGHT - 120, 200, 50, "Difficile", lambda: game_hard(word_input, mot_chiffre, cle_avec_bruit))

    while running:
        screen.blit(background, (0, 0))
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    easy_button.check_click(pygame.mouse.get_pos())
                    hard_button.check_click(pygame.mouse.get_pos())

        mouse_pos = pygame.mouse.get_pos()
        easy_button.check_hover(mouse_pos)
        hard_button.check_hover(mouse_pos)

        easy_button.draw(screen)
        hard_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)

def credits_menu():
    running = True

    credits_background = pygame.image.load("cryptis\\assets\\images\\Credit_Fond.png")
    credits_background = pygame.transform.scale(credits_background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    title_font = pygame.font.Font("cryptis\\assets\\fonts\\slkscrb.ttf", 40)
    text_font = pygame.font.Font("cryptis\\assets\\fonts\\slkscrb.ttf", 30)
    credits_text = [
        "Developpement :",
        "   - Anthony BUFFET",
        "   - Gregoire MONGREDIEN",
        "Art et Graphisme :",
        "   - Gregoire MONGREDIEN",
        "Musique :",
        "   - Anthony BUFFET",
        "",
        "Merci de jouer a Cryptis !",
    ]

    back_button = Button(300, SCREEN_HEIGHT - 100, 200, 50, "Retour", main_menu)

    while running:
        screen.blit(credits_background, (0, 0))

        y_offset = 100  
        for line in credits_text:
            color = (255, 255, 255) if line.endswith(":") else (0, 0, 0)
            font = title_font if line.endswith(":") else text_font
            text = font.render(line, True, color)
            screen.blit(text, (50, y_offset))
            y_offset += 40

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    back_button.check_click(pygame.mouse.get_pos())

        mouse_pos = pygame.mouse.get_pos()
        back_button.check_hover(mouse_pos)
        back_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)


def quit_game():
    pygame.quit()
    sys.exit()

main_menu()
