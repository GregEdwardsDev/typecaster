#!/usr/bin/env python3

import random
import pygame
import pygame.freetype
import wizard_stats
import enemy_stats
from sys import exit

spell_image = pygame.image.load("sprites/spell_32x20.png")

class Spell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 10
        self.image = spell_image  # Set the image for the spell
        self.rect = spell_image.get_rect()
        self.rect.x = x
        self.rect.y = y

spells = []
score = 0
score_rect = pygame.Rect((1080,20),(280,180))

pygame.init()
screen = pygame.display.set_mode((1280,720))
pygame.display.set_caption("TypeCaster")
GAME_FONT = pygame.freetype.SysFont("courier",120)
TEXT_FONT = pygame.freetype.SysFont("courier",30)
clock = pygame.time.Clock()

background = pygame.image.load("sprites/background_3lanes_1280x720.png")
hp3_ui = pygame.image.load("sprites/hp3_ui_196x70.png")
hp2_ui = pygame.image.load("sprites/hp2_ui_196x70.png")
hp1_ui = pygame.image.load("sprites/hp1_ui_196x70.png")
hp0_ui = pygame.image.load("sprites/hp0_ui_196x70.png")

wizard = pygame.image.load("sprites/wizard_256x256.png")
wizard_rect = wizard.get_rect(midbottom = (192,451))
enemy = pygame.image.load("sprites/enemy_256x256.png")
enemy_rect = enemy.get_rect(midbottom = (1280,451))

word_list = [
    "ZAP","POW","ALAKAZAM","FIREBOLT","MAGICMISSILE","KAPOW","ZAP","LIGHTNINGBOLT","RADIANTBEAM","NECROTICO",
    "ACIDBLOB","FORCE","FIREBALL","EXPELLIARMUS","STUPEFY","AVADAKEDAVRA","REND","FUSRODAH","KABOOM","EXPLODE",
    "SHABANG","THUNDER","ICESPIKE","EARTHTREMOR","SHATTER","ZING","ABRACADABRA","HEX","SHAZAM","POWER",
    "HOCUSPOCUS","SIMSALABIM","CALAMARIS","ENCHANT","DISCOMBOBULATE","DAZZLE","BEWITCH","MADNESS","BIND","RAZZLEDAZZLE",
    "THAUMATURGY","WRATH","VOODOO","BAMBOOZLE","BEFOOL","SLIME","FLIMFLAM","POISON","BLIND","DEAFEN",
    "CURSE","SMITE"
]
def get_random_word():
    return word_list[random.randint(0, (len(word_list) - 1))]

row1_word = get_random_word()
row1_rect = pygame.Rect((283,203),(963,133))
row1_input = ""

row2_word = get_random_word()
row2_rect = pygame.Rect((283,383),(963,133))
row2_input = ""

row3_word = get_random_word()
row3_rect = pygame.Rect((283,563),(963,133))
row3_input = ""

def check_hp():
    if wizard_stats.hp == 3:
        screen.blit(hp3_ui,(0,0))
    elif wizard_stats.hp == 2:
        screen.blit(hp2_ui,(0,0))
    elif wizard_stats.hp == 1:
        screen.blit(hp1_ui,(0,0))
    else:
        screen.blit(hp0_ui,(0,0))
        print("Game Over")
        pygame.quit()
        exit()

def move_wizard(key):
    if key == pygame.K_1:
        wizard_stats.current_row = 1
        wizard_rect.y = 23
    elif key == pygame.K_2:
        wizard_stats.current_row = 2
        wizard_rect.y = 203
    elif key == pygame.K_3:
        wizard_stats.current_row = 3
        wizard_rect.y = 383

def get_random_lane():
    lane = random.randint(1, 3)
    if lane == 1:
        return 23
    elif lane == 2:
        return 203
    elif lane == 3:
        return 383

def type_input(key, code):
    global row1_input, row2_input, row3_input
    global row1_word, row2_word, row3_word
    if key == pygame.K_1 or key == pygame.K_2 or key == pygame.K_3:
            move_wizard(key)
    else:
        if wizard_stats.current_row == 1:
            if key == pygame.K_BACKSPACE:
                row1_input = row1_input[:-1]
            else:
                row1_input += code.upper()
        elif wizard_stats.current_row == 2:
            if key == pygame.K_BACKSPACE:
                row2_input = row2_input[:-1]
            else:
                row2_input += code.upper()
        elif wizard_stats.current_row == 3:
            if key == pygame.K_BACKSPACE:
                row3_input = row3_input[:-1]
            else:
                row3_input += code.upper()

        if row1_input == row1_word:
            spells.append(Spell(260,155))
            row1_word = get_random_word()
            row1_input = ""

        elif row2_input == row2_word:
            spells.append(Spell(260,335))
            row2_word = get_random_word()
            row2_input = ""

        elif row3_input == row3_word:
            spells.append(Spell(260,515))
            row3_word = get_random_word()
            row3_input = ""



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            type_input(event.key, event.unicode)

    screen.blit(background,(0,0))

    row1,rect = GAME_FONT.render(row1_word,(40,40,40))
    screen.blit(row1,row1_rect)
    row1_typing,rect = GAME_FONT.render(row1_input,(255,255,255))
    screen.blit(row1_typing,row1_rect)

    row2,rect = GAME_FONT.render(row2_word,(40,40,40))
    screen.blit(row2,row2_rect)
    row2_typing,rect = GAME_FONT.render(row2_input,(255,255,255))
    screen.blit(row2_typing,row2_rect)

    row3,rect = GAME_FONT.render(row3_word,(40,40,40))
    screen.blit(row3,row3_rect)
    row3_typing,rect = GAME_FONT.render(row3_input,(255,255,255))
    screen.blit(row3_typing,row3_rect)

    screen.blit(wizard,wizard_rect)

    if enemy_rect.left == 180:
        enemy_rect.left = 1280
        enemy_rect.y = get_random_lane()
        wizard_stats.hp -=1

    check_hp()

    score_text,rect = TEXT_FONT.render("Score: " + str(score),(0,0,0))
    screen.blit(score_text,score_rect.topleft)

    enemy_rect.x -= 2
    screen.blit(enemy,enemy_rect)

    new_list = []
    for instance in spells:
        if instance.rect.x > 1280:
            pass
        elif instance.rect.colliderect(enemy_rect):
            enemy_rect.left = 1280
            enemy_rect.y = get_random_lane()
            score += 1
        else:
            new_list.append(instance)
            instance.rect.x += 15
            screen.blit(instance.image, instance.rect)
    spells = new_list

    pygame.display.update()
    clock.tick(120)
