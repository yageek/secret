#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, pygame
from pygame.locals import *
chessplate =(
('L','C','C','R','6','R','I','E'),
('E','E','L','S','S','P','9','E'),
('E','E','E','1','U','E','D','U'),
('S','L','U','E','M','9','V','R'),
('D','L','1','S','T','E','A','S'),
('L','O','C','P','5','O','T','D'),
('A','U','A','D','T','E','R','N'),
('R','E','R','C','A','U','R','N')
)

#index de ligne [0 (null),1,2,3,4,5,6,7,8]
ligne = [0,7,6,5,4,3,2,1,0]
colonne = {'A' : 0,'B' : 1,'C':2,'D':3,'E':4,'F':5,'G':6,'H':7}
colonne_label = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

message_p2=["B5 G5 E7 C1 A8 E6 A1 G6 G4","B1 F8 D5 D3 E5 E4 A2 H3 D3 A2","H8 F8 D7 F6 F5 F4 A6 F2 F7","F1 D3 F2 E1 F5 E3 B6 G4 D3","C6 F1 A2 G7 D6 B7 G3 E7 A3 G4"]

def getCoord(sym2,sym1):
	return [ligne[sym1],colonne[sym2]]
def d(sym2,sym1,tableau):
	return tableau[ligne[sym1]][colonne[sym2]]

def getChessCoord(i, j):
    string = "(%s,%s)"%(colonne_label[j], 8-i)
    return string
def dispTable(table):
	for ligne in table:
		string = ""
		for lettre in ligne:
			string = string + lettre.__str__() + " "
		print string
	


def decodeMess(string,tableau):
	retour = ""
	string = string.split(" ")
	for j in string:
		retour = retour + d(j[0],int(j[1]),tableau)
	return retour

def rot90(tableau):
	#Alloue nouveau tableau
	hauteur  = len(tableau)
	nouveau = hauteur *[0]
	for i in range(len(nouveau)):
		nouveau[i] = hauteur*[0]
	#colonne devient le numéro de ligne
	for n_ligne in range(hauteur):
		for n_colonne in range(hauteur):
			nouveau[n_colonne][hauteur - n_ligne - 1] = tableau[n_ligne][n_colonne]
	return nouveau

def rotinv90(tableau):
	#Alloue nouveau tableau
	hauteur  = len(tableau)
	nouveau = hauteur *[0]
	for i in range(len(nouveau)):
		nouveau[i] = hauteur*[0]
	#numéro de ligne reste
	for n_ligne in range(hauteur):
		for n_colonne in range(hauteur):
			nouveau[hauteur - 1 - n_colonne][n_ligne] = tableau[n_ligne][n_colonne]
	return nouveau

#chessplateRot = rot90(chessplate)
#chessplateinvRot = rotinv90(chessplate)

#for i in message_p2:
#	print decodeMess(i,chessplateRot)

#Navigation

def TestMonte(start):
	if(start[0] - 1 <0 ): return False
	else: return True
	
def TestDescend(start):
	if(start[0] + 1 > 7): return False
	else: return True
	
def TestGauche(start):
	if(start[1] - 1 < 0): return False
	else: return True

def TestDroite(start):
	if(start[1] + 1 > 7): return False
	else: return True


def Monte(start):
	if(start[0] - 1 <0 ): return start
	else: return [start[0]-1,start[1]]
	
def Descend(start):
	if(start[0] + 1 > 7): return start
	else: return [start[0]+1,start[1]]
	
def Gauche(start):
	if(start[1] - 1 < 0): return start
	else: return [start[0],start[1] - 1]

def Droite(start):
	if(start[1] + 1 > 7): return start
	else: return [start[0],start[1] + 1]
	
def isInt(coord,tableau):
	try:
		int(tableau[coord[0]][coord[1]])
	except:
		return False
	else: return True



def parseFromStartPoint(coord,tableau,path,path_forbid=[],passed=[]):
	passed.append(coord)
	path[-1].append(tableau[coord[0]][coord[1]])
	print "Passed" +  passed.__str__()
	
	
		
	if TestMonte(coord) is False and not isInt(Monte(coord),tableau) and TestMonte(coord) not in passed:
		path_forbid.append(Monte(coord))
	if Monte(coord) not in path_forbid:
		parseFromStartPoint(Monte(coord),tableau,path,path_forbid,passed)
		
			
		

	if(TestDescend(coord) is not False and not isInt(Descend(coord),tableau)):
		if Descend(coord) not in path_forbid:
			parseFromStartPoint(Monte(coord),tableau,path,path_forbid)
	else :
		path_forbid.append(Descend(coord))
		

	if TestGauche(coord) is False and not isInt(Gauche(coord),tableau) and TestGauche(coord) not in passed :
		path_forbid.append(Gauche(coord))
	if Gauche(coord) not in path_forbid:
			parseFromStartPoint(Monte(coord),tableau,path,path_forbid,passed)
	
	if TestDroite(coord) is not False and not isInt(Droite(coord),tableau):
			if Droite(coord) not in path_forbid:
				parseFromStartPoint(Monte(coord),tableau,path,path_forbid)
	else:
		path_forbid.append(Droite(Forbid))
def highlightCase(screen,case, color):
    i = case[0]
    j = case[1]
    highLight = pygame.Surface((caseSize, caseSize))
    highLight.fill(color)
    pos =  (j*caseSize + offset, i*caseSize + offset)
    screen.blit(highLight, pos)
    text = font.render(chessplate[i][j], 1, (0, 0, 0,))
    screen.blit(text, (pos[0] + 20, pos[1] +  20))
    pygame.display.flip()
    
def isValid(i, j):
    
    if(i > 7 or i <0 or j <0 or j>7):
        return False
    else:
        return True
    
def getPossibilities(case, passed):
    i = case[0]
    j = case[1]
    futureCase = []
    
    if isValid(i+2, j-1) and [i+2, j-1] not in passed: futureCase.append([i+2, j-1])
    if isValid(i+2, j+1) and [i+2, j+1] not in passed: futureCase.append([i+2, j+1])
    
    if isValid(i-2, j-1) and [i-2, j-1] not in passed: futureCase.append([i-2, j-1])
    if isValid(i-2, j+1) and [i-2, j+1] not in passed: futureCase.append([i-2, j+1])
    
    if isValid(i+1, j-2) and [i+1, j-2] not in passed: futureCase.append([i+1, j-2])
    if isValid(i+1, j+2) and [i+1, j+2] not in passed: futureCase.append([i+1, j+2])
    
    if isValid(i-1, j-2) and [i-1, j-2] not in passed: futureCase.append([i-1, j-2])
    if isValid(i-1, j+2) and [i-1, j+2] not in passed: futureCase.append([i-1, j+2])
    
    return futureCase
    
    
    
    
    
def dispChess(screen):
    color = 1
    for i in range(8):
        label = little_font.render((8-i).__str__(), 1, (0, 0, 0))
        screen.blit(label,  (25, i*caseSize + offset + 25))
        screen.blit(label,  (screen_square - 25, i*caseSize + offset + 25))
        
        label = little_font.render(colonne_label[i], 1, (0, 0, 0))
        screen.blit(label,  (i*caseSize + offset + 25, 25))
        screen.blit(label,  (i*caseSize + offset + 25, screen_square - 25))
            
        color = 1-color
        for j in range(8):
            pos =  (j*caseSize + offset, i*caseSize + offset)
            currentCase = pygame.Surface((caseSize, caseSize))
            if(color):
                currentCase.fill((0, 0, 0))
                text = font.render(chessplate[i][j], 1, (255, 255, 255))
            else:
                currentCase.fill((255, 255, 255))
                text = font.render(chessplate[i][j], 1, (0, 0,0))            
            screen.blit(currentCase,pos)
            screen.blit(text, (pos[0] + 20, pos[1] +  20))
            color = 1 - color
        #highlight blue ppassed case
        for case in passed:
            highlightCase(app, case, (128, 128, 128))
    pygame.display.flip()
def caseChoosed(case):
    global phrase
    global passed
    i = case[0]
    j = case[1]
    passed.append([i, j])
    phrase = phrase + chessplate[i][j]
def dispChoiceForCase(screen, case):
    global lastPossibilities
    global phrase
    dispChess(screen)
    print phrase
    print "Choose the next case:"
    lastPossibilities = getPossibilities(case, passed)
    for index in range(len(lastPossibilities)):
        i = lastPossibilities[index][0]
        j = lastPossibilities[index][1]
        highlightCase(screen, lastPossibilities[index], (255, 0, 255))
        print "[%i] %s Coord %s"%(index, chessplate[i][j],getChessCoord(i, j))
    highlightCase(app, case, (0, 0, 255))
    
if __name__ == '__main__':
#param 
    caseSize = 50
    screen_square = 500
    app_size = (screen_square,screen_square)
    chessplate_square = 8 *caseSize
    offset = (screen_square - chessplate_square)/2
    START_POINT = getCoord('D',3)
    passed=[]
    phrase=""
    lastPossibilities = []
    
    pygame.init()
    font = pygame.font.Font(None, 40)
    little_font = pygame.font.Font(None, 15)
    app = pygame.display.set_mode(app_size)
    pygame.display.set_caption('E1 - Beta')
    app.fill((250, 250, 250))
    pygame.display.flip()

    
    
    caseChoosed(START_POINT)
    dispChoiceForCase(app, START_POINT)
    
    
    
    
    # Loop
    go_out = 1
    while (go_out):
        for event in pygame.event.get():
            if event.type == QUIT:
                go_out =0
            elif event.type == KEYDOWN:
                if(event.key == K_KP0):
                    caseChoosed(lastPossibilities[0])
                    dispChoiceForCase(app, lastPossibilities[0])
                elif(event.key == K_KP1):
                    caseChoosed(lastPossibilities[1])
                    dispChoiceForCase(app, lastPossibilities[1])
                elif(event.key == K_KP2):
                    caseChoosed(lastPossibilities[2])
                    dispChoiceForCase(app, lastPossibilities[2])
                elif(event.key == K_KP3):
                    caseChoosed(lastPossibilities[3])
                    dispChoiceForCase(app, lastPossibilities[3])
                elif(event.key == K_KP4):
                    caseChoosed(lastPossibilities[4])
                    dispChoiceForCase(app, lastPossibilities[4])
                elif(event.key == K_KP5):
                    caseChoosed(lastPossibilities[5])
                    dispChoiceForCase(app, lastPossibilities[5])
                elif(event.key == K_KP6):
                    caseChoosed(lastPossibilities[6])
                    dispChoiceForCase(app, lastPossibilities[6])
                elif(event.key == K_KP7):
                    caseChoosed(lastPossibilities[7])
                    dispChoiceForCase(app, lastPossibilities[7])
                elif(event.key == K_KP8):
                    caseChoosed(lastPossibilities[8])
                    dispChoiceForCase(app, lastPossibilities[8])
                elif(event.key == K_BACKSPACE):
                    if(len(passed ) > 1):
                        phrase = phrase[:-1]
                        passed = passed[:-1]
                        #caseChoosed(passed[-1])
                        dispChoiceForCase(app, passed[-1])
                    else:
                        passed = []
                        phrase = []
                        caseChoosed(START_POINT)
                        dispChoiceForCase(app, START_POINT)
                    
    
    
    
    
    
    
    
    

