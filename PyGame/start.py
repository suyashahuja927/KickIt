
#importing modules

import pygame
import sys
import os
import time

#--------------------------

#initialise pygame

pygame.init()

#--------------------------

#basic colours

BLACK = ( 0, 0, 0)
WHITE = (255,255,255)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)
BLUE = ( 0, 0, 255)

#--------------------------

#importing and loading pictures

arrower = pygame.image.load('arrow.png')
wasder = pygame.image.load('wasd.png')

#--------------------------


#function to transform all imported images and make their background transparent

def getimage(sheet):
    sheet = pygame.transform.scale (sheet, (300,200))
    sheet.set_colorkey(WHITE)
    
    return sheet


#--------------------------

#function to store the player names in a file (so they can be read by the other files)

def recordnames(p1name,p2name):
    scoresfile = open("names.txt","w")
    
    scoresfile.write(str(p1name))
    scoresfile.write(",")
    scoresfile.write(str(p2name))
    scoresfile.write("\n")

            
    scoresfile.close()    
    
#--------------------------

#a button class for all the buttons that would be displayed
    
class boxes:
    def __init__(self, x,y,height,width,color):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.color = color

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False


class button(boxes):   
    def __init__(self, x,y,height,width, color,text=''):
        super().__init__(x,y,height,width,color)
        self.text = text


    def draw(self,screen,outline=None):
        if outline:
            pygame.draw.rect(screen, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(screen, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 32)
            text = font.render(self.text, True, (0,0,0))
            screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

   


class inputboxes(boxes):
    def __init__(self,x,y,height,width,color):
        super().__init__(x,y,height,width,color)
        self.active = False
        
    def draw(self):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x,self.y,self.width,self.height),5)
                         
#--------------------------

#defining the games framerate

FPS = 60

#--------------------------

# initialising the display

size = width, height = (1280, 720)
screen = pygame.display.set_mode((width, height))

#title, icon, background

pygame.display.set_caption("kick it")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

backgroundimg = pygame.image.load('lightbackground.png')
background = pygame.transform.scale (backgroundimg, (width, height))


#--------------------------

#functions for fading the screen after user presses a button (different functions for different screens)

def fade(width, height): 
    fade = pygame.Surface((width, height))
    fade.fill((0,0,0))
    opacity = 0
    for o in range(0, 40):
        opacity += 10
        fade.set_alpha(opacity)
        drawmain()
        screen.blit(fade, (0,0))
        pygame.display.update()
        pygame.time.delay(1)


def fadeback(width, height):
    fade = pygame.Surface((width, height))
    fade.fill((0,0,0))
    opacity = 0
    for o in range(0, 40):
        opacity += 8
        fade.set_alpha(opacity)
        nameswindowdraw("hope you enjoy! :)","hope you enjoy! :)", 0)
        screen.blit(fade, (0,0))
        pygame.display.update()
        pygame.time.delay(1)
    
    
    
    
def fadetutorial(width,height):
    fade = pygame.Surface((width, height))
    fade.fill((0,0,0))
    opacity = 0
    for o in range(0, 40):
        opacity += 10
        fade.set_alpha(opacity)
        drawtutorialwindow()
        screen.blit(fade, (0,0))
        pygame.display.update()
        pygame.time.delay(1)


#--------------------------
    
    
    
#****************************************#
#                                        #
#                                        #
#           MAIN PROGRAM                 #
#                                        #
#                                        #
#****************************************#



#STARTING SCREEN



#function to store everything that happens in the main loop (starting screen)

def drawmain():
    screen.blit(background, (0,0))
    playbutton.draw(screen, (WHITE))
    leaderboardbutton.draw(screen, (WHITE))
    exitbutton.draw(screen,(WHITE))
        

#initialising objects from the button class to display buttons

playbutton=button(450, 100, 100, 400,(RED), 'PLAY')
leaderboardbutton=button(450, 310, 100,400,(RED), 'LEADERBOARD')
exitbutton=button(450,520, 100,400,(RED), 'EXIT')
    
playernames=[]    
    

    
#this function is the loop for the starting screen

    
def mainprogram():
    
    
    
    clock = pygame.time.Clock()
    finished = False


    while finished == False:

        


        clock.tick(FPS)

        drawmain()
        
        
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if playbutton.isOver(pos):
                    print("play")
                    fade(width,height)
                    inputwindow()
                    
                if leaderboardbutton.isOver(pos):
                    print("leaderboard")
                    fade(width,height)
                    import leaderboard
                    
                if exitbutton.isOver(pos):
                    fade(width,height)
                    finished = True
            
            if event.type == pygame.MOUSEMOTION:
                if playbutton.isOver(pos):
                    playbutton.color = (WHITE)
                elif leaderboardbutton.isOver(pos):
                    leaderboardbutton.color = (WHITE)
                elif exitbutton.isOver(pos):
                    exitbutton.color = (WHITE)
                else:
                    playbutton.color = (RED)
                    leaderboardbutton.color = (RED)
                    exitbutton.color = (RED)
                            
                
            
          
        pygame.display.update()
    
    pygame.quit()
    
#-------------------------------------------------------------------------------------------------------------



#ENTER_NAMES_SCREEN



#function to store everything that goes in the enter names screen    
    
error = 0   
    
def nameswindowdraw(p1name,p2name,error):
        font=pygame.font.SysFont('comicsans',44)
    
        if error == 0:
            enternamep1= ("Please enter player 1 name here: (max 10 chars)")
            enternamep2= ("Please enter player 2 name here: (max 10 chars)")
        elif error == 1:
            enternamep1= ("Error, try again (max 10 chars)")
            enternamep2= ("Please enter player 2 name here:")
        elif error == 2:
            enternamep1= ("Please enter player 1 name here:")
            enternamep2= ("Error, try again (max 10 chars)")
        elif error == 3:
            enternamep1= ("Please enter player 1 name here:")
            enternamep2= ("Error, try again (names can't be the same)")
        screen.blit(background, (0,0))

        pygame.draw.rect(screen, (RED), (75, 75, 1080, 450))
        pygame.draw.rect(screen, (WHITE), (75, 75, 1080, 450),5)
        
        
        enter1 = font.render(enternamep1,True,(WHITE))
        enter2 = font.render(enternamep2,True,(WHITE))

        takeinputp1 = font.render (p1name, True, (WHITE))
        takeinputp2 = font.render (p2name, True, (WHITE))

        nextbutton.draw(screen, (WHITE))
        backbutton.draw(screen, (WHITE))

        
        p1box.draw()
        p2box.draw()
        
        screen.blit(enter1, (100,75))
        screen.blit(enter2, (100,275))
        screen.blit(takeinputp1, (p1box.x + 10,p1box.y + 10))
        screen.blit(takeinputp2, (p2box.x + 10,p2box.y + 10)) 



#initialsing objects from the button and inputboxes class for buttons and boxes
        
p1box = inputboxes(100,175, 100,500,BLACK)
p2box = inputboxes(100,400,100,500,BLACK)

nextbutton=button( 900, 600, 100, 400,(RED), 'NEXT')
backbutton=button(20,600,100,400,(RED), 'BACK')

#loop for the enter names window    

def inputwindow():

    clock = pygame.time.Clock()
    finished = False
    

    p1name = ''
    p2name = ''
    

    while finished == False:
        
        nameswindowdraw(p1name, p2name,0)
        

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


            if p1box.active == True:
                p1box.color = WHITE

            elif p1box.active == False:
                p1box.color = BLACK

            if p2box.active == True:
                p2box.color = WHITE

            elif p2box.active == False:
                p2box.color = BLACK

            if event.type == pygame.MOUSEBUTTONDOWN:
                if p1box.isOver(pos):
                    p1box.active=True
                    p2box.active=False

                elif p2box.isOver(pos):
                    p1box.active=False
                    p2box.active=True
                    
                else:
                    p1box.active=False
                    p2box.active=False
                    
                if nextbutton.isOver(pos):
                    if (len(p1name)) > 10 or (len(p1name)) == 0:

                        nameswindowdraw(p1name,p2name,1)
                        print(len(p1name))
                        pygame.display.update()
                        #time.sleep(2)
                        
                    elif (len(p2name)) > 10 or (len(p2name)) == 0:

                        nameswindowdraw(p1name,p2name,2)
                        print(len(p2name))
                        pygame.display.update()
                        #time.sleep(2)

                    elif p1name == p2name:

                        nameswindowdraw(p1name,p2name,3)
                        print(len(p2name))
                        pygame.display.update()
                        #time.sleep(2)
                        
                    else:
                        fadeback(width,height)
                    
                        playernames.append(p1name)
                        playernames.append(p2name)
                        print (playernames)
                        print(p1name,len(p1name))
                        print(p2name,len(p2name))
                        tutorialwindow()
                    
                elif backbutton.isOver(pos):
                    fadeback(width,height)
                    mainprogram()
                    
                    
            if event.type == pygame.KEYDOWN:
                if p1box.active == True:
                    if event.key == pygame.K_BACKSPACE:
                        p1name = p1name[:-1]
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_TAB:
                        p1box.active = False
                        p2box.active = True
                        
                        

                    else:
                        p1name += event.unicode
    
                elif p2box.active == True:
                    if event.key == pygame.K_BACKSPACE:
                        p2name = p2name[:-1]
                        
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_TAB:
                        p1box.active = False
                        p2box.active = False

                    else:
                        p2name += event.unicode
                        
                        
                


            if event.type == pygame.MOUSEMOTION:
                if nextbutton.isOver(pos):
                    nextbutton.color = (WHITE)
                elif backbutton.isOver(pos):
                    backbutton.color=(WHITE)
                else:
                    nextbutton.color = (RED)
                    backbutton.color=(RED)
                    
                    
                  
        
        
        pygame.display.update()


#-------------------------------------------------------------------------------------------------------------                    


#INSTRUCTION_SCREEN
        

#function to store everything that goes in the instruction/tutorial window    
    
    
def drawtutorialwindow():  
    font=pygame.font.SysFont('comicsans',32)
    smallfont=pygame.font.SysFont('comicsans',20)
    
    welcome = font.render(("Welcome to _KICKIT_"), True,(WHITE))
    instructions = smallfont.render(("Please follow the instructions below have fun!"),True,(WHITE))
    
    screen.blit(background, (0,0))
    pygame.draw.rect(screen, (RED), (100,100,500,470))
    pygame.draw.rect(screen, (RED), (690,100,500,470))
    
    hello = font.render("hello", True, (WHITE))
    
    names1 = font.render(playernames[0],True,(WHITE))
    names2 = font.render(playernames[1],True,(WHITE))


    screen.blit(hello, (100,100))
    screen.blit(hello, (700,100))
    
    screen.blit(names1, (180,100))
    screen.blit(names2, (780,100))
    
    screen.blit(welcome, (100,170))
    screen.blit(welcome, (700,170))
    
    screen.blit(instructions, (100, 240))
    screen.blit(instructions, (700, 240))
    
    screen.blit(wasd, (200, 320))
    screen.blit(arrow, (800,320))

    nextbutton.draw(screen, (WHITE))





#running the images that i need through the transform and transperancy function

arrow = getimage(arrower)
wasd = getimage(wasder)

    
#the main loop for the instruction screen


def tutorialwindow():

    clock = pygame.time.Clock()
    finished = False
        
    while finished == False:
        
        drawtutorialwindow()

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if nextbutton.isOver(pos):
                    fadetutorial(width,height)
                    recordnames(playernames[0],playernames[1])
                    
                    
                    
                    import main
                    
                    
                    
            if event.type == pygame.MOUSEMOTION:
                if nextbutton.isOver(pos):
                    nextbutton.color = (WHITE)
                else:
                    nextbutton.color = (RED)
                    
        pygame.display.update()
        
        clock.tick(FPS)

#---------------------------------------------------------------------------------------------------------------------#

        
#--------------------------------------   
#Running the starting screen loop to start the game#

if __name__ == "__main__":
    mainprogram()
                    
        

