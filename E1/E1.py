#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *

chessplate = (
    ('L', 'C', 'C', 'R', '6', 'R', 'I', 'E'),
    ('E', 'E', 'L', 'S', 'S', 'P', '9', 'E'),
    ('E', 'E', 'E', '1', 'U', 'E', 'D', 'U'),
    ('S', 'L', 'U', 'E', 'M', '9', 'V', 'R'),
    ('D', 'L', '1', 'S', 'T', 'E', 'A', 'S'),
    ('L', 'O', 'C', 'P', '5', 'O', 'T', 'D'),
    ('A', 'U', 'A', 'D', 'T', 'E', 'R', 'N'),
    ('R', 'E', 'R', 'C', 'A', 'U', 'R', 'N')
)

# index de ligne [0 (null),1,2,3,4,5,6,7,8]
ligne = [0, 7, 6, 5, 4, 3, 2, 1, 0]
colonne = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7}
colonne_label = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']


def get_coord(sym2, sym1):
    return [ligne[sym1], colonne[sym2]]


def d(sym2, sym1, tableau):
    return tableau[ligne[sym1]][colonne[sym2]]


def get_chess_coord(i, j):
    string = "(%s,%s)" % (colonne_label[j], 8 - i)
    return string


def disp_table(table):
    for ligne in table:
        string = ""
        for lettre in ligne:
            string = string + lettre.__str__() + " "
        print(string)


def decode_mess(string, tableau):
    retour = ""
    string = string.split(" ")
    for j in string:
        retour = retour + d(j[0], int(j[1]), tableau)
    return retour


def rot90(tableau):
    # Alloue nouveau tableau
    hauteur = len(tableau)
    nouveau = hauteur * [0]
    for i in range(len(nouveau)):
        nouveau[i] = hauteur * [0]
    # colonne devient le numéro de ligne
    for n_ligne in range(hauteur):
        for n_colonne in range(hauteur):
            nouveau[n_colonne][hauteur - n_ligne - 1] = tableau[n_ligne][n_colonne]
    return nouveau


def rotinv90(tableau):
    # Alloue nouveau tableau
    hauteur = len(tableau)
    nouveau = hauteur * [0]
    for i in range(len(nouveau)):
        nouveau[i] = hauteur * [0]
    # numéro de ligne reste
    for n_ligne in range(hauteur):
        for n_colonne in range(hauteur):
            nouveau[hauteur - 1 - n_colonne][n_ligne] = tableau[n_ligne][n_colonne]
    return nouveau


def highlight_case(screen, case, color):
    i = case[0]
    j = case[1]
    highlight = pygame.Surface((caseSize, caseSize))
    highlight.fill(color)
    pos = (j * caseSize + offset, i * caseSize + offset)
    screen.blit(highlight, pos)
    text = font.render(chessplate[i][j], 1, (0, 0, 0,))
    screen.blit(text, (pos[0] + 20, pos[1] + 20))
    pygame.display.flip()


def is_valid(i, j):
    if i > 7 or i < 0 or j < 0 or j > 7:
        return False
    else:
        return True


def get_possibilities(case, passed):
    i = case[0]
    j = case[1]
    futureCase = []

    if is_valid(i + 2, j - 1) and [i + 2, j - 1] not in passed: futureCase.append([i + 2, j - 1])
    if is_valid(i + 2, j + 1) and [i + 2, j + 1] not in passed: futureCase.append([i + 2, j + 1])

    if is_valid(i - 2, j - 1) and [i - 2, j - 1] not in passed: futureCase.append([i - 2, j - 1])
    if is_valid(i - 2, j + 1) and [i - 2, j + 1] not in passed: futureCase.append([i - 2, j + 1])

    if is_valid(i + 1, j - 2) and [i + 1, j - 2] not in passed: futureCase.append([i + 1, j - 2])
    if is_valid(i + 1, j + 2) and [i + 1, j + 2] not in passed: futureCase.append([i + 1, j + 2])

    if is_valid(i - 1, j - 2) and [i - 1, j - 2] not in passed: futureCase.append([i - 1, j - 2])
    if is_valid(i - 1, j + 2) and [i - 1, j + 2] not in passed: futureCase.append([i - 1, j + 2])

    return futureCase


def disp_chess(screen):
    color = 1
    for i in range(8):
        label = little_font.render((8 - i).__str__(), 1, (0, 0, 0))
        screen.blit(label, (25, i * caseSize + offset + 25))
        screen.blit(label, (screen_square - 25, i * caseSize + offset + 25))

        label = little_font.render(colonne_label[i], 1, (0, 0, 0))
        screen.blit(label, (i * caseSize + offset + 25, 25))
        screen.blit(label, (i * caseSize + offset + 25, screen_square - 25))

        color = 1 - color
        for j in range(8):
            pos = (j * caseSize + offset, i * caseSize + offset)
            current_case = pygame.Surface((caseSize, caseSize))
            if (color):
                current_case.fill((0, 0, 0))
                text = font.render(chessplate[i][j], 1, (255, 255, 255))
            else:
                current_case.fill((255, 255, 255))
                text = font.render(chessplate[i][j], 1, (0, 0, 0))
            screen.blit(current_case, pos)
            screen.blit(text, (pos[0] + 20, pos[1] + 20))
            color = 1 - color
        # highlight blue ppassed case
        for case in passed:
            highlight_case(app, case, (128, 128, 128))
    pygame.display.flip()


def case_choosed(case):
    global phrase
    global passed
    i = case[0]
    j = case[1]
    passed.append([i, j])
    phrase = phrase + chessplate[i][j]


def disp_choice_for_case(screen, case):
    global last_possibilities
    global phrase
    disp_chess(screen)
    print(phrase)
    print("Choose the next case:")
    # lastPossibilities = getPossibilities(case,passed)
    last_possibilities = get_next(case, passed)
    if last_possibilities == 0:
        print("Result : " + phrase)
    for index in range(len(last_possibilities)):
        i = last_possibilities[index][0]
        j = last_possibilities[index][1]
        highlight_case(screen, last_possibilities[index], (255, 0, 255))
        print("[%i] %s Coord %s" % (index, chessplate[i][j], get_chess_coord(i, j)))
    highlight_case(app, case, (0, 0, 255))


def get_next(case, passed):
    temp = passed[:]
    possib = get_possibilities(case, temp)
    temp.append(case)
    next = []
    for pos in possib:
        next.append(len(get_possibilities(pos, temp)))
    # print "Next Possibilities :" + next.__str__()
    mini = next[0]
    index = []
    for i in range(len(next)):
        if (next[i] < mini):
            mini = next[i]

    # print "Mini:" + mini.__str__()
    for i in range(len(next)):
        if next[i] == mini:
            index.append(i)
    retour = []
    for i in index:
        retour.append(possib[i])
    # print "Retour pour case:" + retour.__str__()
    return retour


if __name__ == '__main__':
    # param
    caseSize = 50
    screen_square = 500
    app_size = (screen_square, screen_square)
    chessplate_square = 8 * caseSize
    offset = (screen_square - chessplate_square) / 2
    START_POINT = get_coord('D', 3)
    passed = []
    phrase = ""
    last_possibilities = []

    pygame.init()
    font = pygame.font.Font(None, 40)
    little_font = pygame.font.Font(None, 15)
    app = pygame.display.set_mode(app_size)
    pygame.display.set_caption('E1 - Beta')
    app.fill((250, 250, 250))
    pygame.display.flip()

    case_choosed(START_POINT)
    disp_choice_for_case(app, START_POINT)

    # Loop
    go_out = 1
    while (go_out):
        for event in pygame.event.get():
            if event.type == QUIT:
                go_out = 0
            elif event.type == KEYDOWN:
                if event.key == K_KP0 or event.key == K_0:
                    case_choosed(last_possibilities[0])
                    disp_choice_for_case(app, last_possibilities[0])
                elif event.key == K_KP1 or event.key == K_1:
                    case_choosed(last_possibilities[1])
                    disp_choice_for_case(app, last_possibilities[1])
                elif event.key == K_KP2 or event.key == K_2:
                    case_choosed(last_possibilities[2])
                    disp_choice_for_case(app, last_possibilities[2])
                elif event.key == K_KP3 or event.key == K_3:
                    case_choosed(last_possibilities[3])
                    disp_choice_for_case(app, last_possibilities[3])
                elif event.key == K_KP4 or event.key == K_4:
                    case_choosed(last_possibilities[4])
                    disp_choice_for_case(app, last_possibilities[4])
                elif event.key == K_KP5 or event.key == K_5:
                    case_choosed(last_possibilities[5])
                    disp_choice_for_case(app, last_possibilities[5])
                elif event.key == K_KP6 or event.key == K_6:
                    case_choosed(last_possibilities[6])
                    disp_choice_for_case(app, last_possibilities[6])
                elif event.key == K_KP7 or event.key == K_7:
                    case_choosed(last_possibilities[7])
                    disp_choice_for_case(app, last_possibilities[7])
                elif event.key == K_KP8 or event.key == K_8:
                    case_choosed(last_possibilities[8])
                    disp_choice_for_case(app, last_possibilities[8])
                elif event.key == K_BACKSPACE:
                    if (len(passed) > 1):
                        phrase = phrase[:-1]
                        passed = passed[:-1]
                        disp_choice_for_case(app, passed[-1])
                    else:
                        passed = []
                        phrase = ""
                        case_choosed(START_POINT)
                        disp_choice_for_case(app, START_POINT)
