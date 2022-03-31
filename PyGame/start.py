
## STARTING MENU ##

#=============================================================================================================================#
#=============================================================================================================================#


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
    
#=============================================================================================================================#
#=============================================================================================================================#

##CLASSES

    
# a super class boxes from which i can make different types of boxes    
class boxes:
    def __init__(self, x,y,height,width,color):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.color = color

    def isOver(self, pos):  # checks the mouse position, if mouse position is over this box, it would return as True
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False

#--------------------------
    
# Button class for all the buttons throughout the game

class button(boxes):   
    def __init__(self, x,y,height,width, color,text=''):
        super().__init__(x,y,height,width,color) #inherits those attributes from boxes class
        self.text = text


    def draw(self,screen,outline=None): #draws the button, and adds text and outline if there is any
        if outline: 
            pygame.draw.rect(screen, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(screen, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 32)
            text = font.render(self.text, True, (0,0,0))
            screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

   
#--------------------------

class inputboxes(boxes):
    def __init__(self,x,y,height,width,color): #inherits those attributes from boxes class
        super().__init__(x,y,height,width,color)
        self.active = False #if its selected
        
    def draw(self):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x,self.y,self.width,self.height),5) #draws the input boxes on screen
        
                         
#=============================================================================================================================#
#=============================================================================================================================#

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


#=============================================================================================================================#
#=============================================================================================================================#

#functions for fading the screen after user presses a button (different functions for different screens)

def fade(width, height): 
    fade = pygame.Surface((width, height))
    fade.fill((0,0,0)) #fills the screen with black and then redraws the image over it slowly
    opacity = 0
    for o in range(0, 40):
        opacity += 10
        fade.set_alpha(opacity) #increases opacity as it displaying the black screen giving the effect of a fade
        drawmain()
        screen.blit(fade, (0,0))
        pygame.display.update()
        pygame.time.delay(1)

#same as above but different for each screen/game loop
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


#=============================================================================================================================#
#=============================================================================================================================#
    
    
    
#****************************************#
#                                        #
#                                        #
#             MAIN PROGRAM               #
#                                        #
#                                        #
#****************************************#



#STARTING SCREEN



#function to draw everything needed in the main loop (starting screen)

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
            pos = pygame.mouse.get_pos() #gets the mouse position
            
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN: #if the mouse button is pressed
                if playbutton.isOver(pos): #while its pressed, if its over the play button:
                    #print("play")
                    fade(width,height) #use the fade function to transition
                    inputwindow() #runs the input window screen
                    
                if leaderboardbutton.isOver(pos): #if the mouse is over leaderboard button
                    #print("leaderboard")
                    fade(width,height) #fade transition
                    import leaderboard # run the leaderboard.py file
                    
                if exitbutton.isOver(pos): #if the mouse button is over the exit button
                    fade(width,height) #fade transition
                    finished = True #stops the main loop and quits
            
            if event.type == pygame.MOUSEMOTION:
                #if the mouse is over any of the buttons, change their colour to show that their being hovered
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

    
#=============================================================================================================================#
#=============================================================================================================================#



#ENTER_NAMES_SCREEN



#function to draw everything that goes in the enter names screen    
    
error = 0   
    
def nameswindowdraw(p1name,p2name,error):
        font=pygame.font.SysFont('comicsans',44)
    
        if error == 0: #if there is no error
            enternamep1= ("Please enter player 1 name here: (max 10 chars)")
            enternamep2= ("Please enter player 2 name here: (max 10 chars)")
        elif error == 1: #if there is an error with the 1st input box
            enternamep1= ("Error, try again (max 10 chars)")
            enternamep2= ("Please enter player 2 name here:")
        elif error == 2: #if there is an error with the 2nd input box
            enternamep1= ("Please enter player 1 name here:")
            enternamep2= ("Error, try again (max 10 chars)")
        elif error == 3: #if both the names are same
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
    

    p1name = '' #where the user input will be scored
    p2name = ''
    

    while finished == False:
        
        nameswindowdraw(p1name, p2name,0) #run the function above to draw all the objects
        
        #if x top corner is pressed
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            #change the colour of the box to show that its selected
            if p1box.active == True:
                p1box.color = WHITE

            elif p1box.active == False:
                p1box.color = BLACK

            if p2box.active == True:
                p2box.color = WHITE

            elif p2box.active == False:
                p2box.color = BLACK

            if event.type == pygame.MOUSEBUTTONDOWN: # when the mouse button is pressed
                if p1box.isOver(pos): # when the mouse button is pressed and the mouse is over a box then the respective .active becomes true
                    p1box.active=True
                    p2box.active=False

                elif p2box.isOver(pos):
                    p1box.active=False
                    p2box.active=True
                    
                else:
                    p1box.active=False
                    p2box.active=False

                #if they press the next button  
                if nextbutton.isOver(pos):
                    if (len(p1name)) > 10 or (len(p1name)) == 0: #checking if the player 1 input is empty or over 10 characters

                        nameswindowdraw(p1name,p2name,1) #if it is, run the draw program with the respective error message
                        #print(len(p1name))
                        pygame.display.update()
                        time.sleep(2) #pause the game for 2 seconds and then switch back to the normal screen the next time the loop is run
                        
                    elif (len(p2name)) > 10 or (len(p2name)) == 0: #checking if the player 2 input is empty or over 10 characters

                        nameswindowdraw(p1name,p2name,2) #if it is, run the draw program with the respective error message
                        #print(len(p2name))
                        pygame.display.update()
                        time.sleep(2) #pause the game for 2 seconds and then switch back to the normal screen the next time the loop is run

                    elif p1name == p2name: #checking if both the names are the same

                        nameswindowdraw(p1name,p2name,3) #if it is run the draw program with the respective error message
                        print(len(p2name))
                        pygame.display.update()
                        time.sleep(2)
                        
                    else: # if the inputs pass all the validation checks

                        fadeback(width,height) #fade transition
                    
                        playernames.append(p1name) #add names to the playernames list
                        playernames.append(p2name) 
                        #print (playernames)
                        #print(p1name,len(p1name))
                        #print(p2name,len(p2name))
                        tutorialwindow() #run the tutorial window screen
                    
                elif backbutton.isOver(pos): #if they press the back button: 
                    fadeback(width,height) #fade
                    mainprogram() #run the starting screen
                    
                    
            if event.type == pygame.KEYDOWN: #checking if the end user is typing
                
                #if they're typing, and the 1st box is selected
                if p1box.active == True: 
                    if event.key == pygame.K_BACKSPACE: #check if they pressed backspace
                        p1name = p1name[:-1] #take away the last character
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_TAB: # if tab or enter is pressed, deselect the first box and select the 2nd box
                        p1box.active = False
                        p2box.active = True    
    
                    else: #if any other keys are pressed
                        p1name += event.unicode #add the key to the string

                #same as above but for the 2nd box
                elif p2box.active == True:
                    if event.key == pygame.K_BACKSPACE:
                        p2name = p2name[:-1]
                        
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_TAB: #deselect both the boxes
                        p1box.active = False
                        p2box.active = False

                    else:
                        p2name += event.unicode
                        
                        
                

            
            if event.type == pygame.MOUSEMOTION: #check if mouse is hovering over any buttons, if they are change colour to show they're selected
                if nextbutton.isOver(pos):
                    nextbutton.color = (WHITE)
                elif backbutton.isOver(pos):
                    backbutton.color=(WHITE)
                else:
                    nextbutton.color = (RED)
                    backbutton.color=(RED)
                    
                    
                  
        
        
        pygame.display.update()


#=============================================================================================================================#
#=============================================================================================================================#                    


#INSTRUCTION_SCREEN
        

#function to draw everything that goes in the instruction/tutorial window    
    
    
def drawtutorialwindow():  
    font=pygame.font.SysFont('comicsans',32)
    smallfont=pygame.font.SysFont('comicsans',20)
    
    welcome = font.render(("Welcome to _KICKIT_"), True,(WHITE))
    instructions = smallfont.render(("Please follow the instructions below have fun!"),True,(WHITE))
    
    screen.blit(background, (0,0))
    pygame.draw.rect(screen, (RED), (100,100,500,470))
    pygame.draw.rect(screen, (RED), (690,100,500,470))
    
    hello = font.render("hello", True, (WHITE))
    
    names1 = font.render(playernames[0],True,(WHITE)) #getting the names from the list
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





#running the images that through the transform and transperancy function

arrow = getimage(arrower)
wasd = getimage(wasder)

    
#the main loop for the instruction screen


def tutorialwindow():

    clock = pygame.time.Clock()
    finished = False
        
    while finished == False:
        
        drawtutorialwindow() #draw everything from the function above

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN: #if the next buttons pressed:
                if nextbutton.isOver(pos):
                    fadetutorial(width,height)#fade
                    recordnames(playernames[0],playernames[1]) #store the names of the players using the function
 
                    import main  #run the main.py file
                    
                    
                    
            if event.type == pygame.MOUSEMOTION: #change colour if hovering
                if nextbutton.isOver(pos):
                    nextbutton.color = (WHITE)
                else:
                    nextbutton.color = (RED)
                    
        pygame.display.update() #updates the display everytime the loop is run
        
        clock.tick(FPS)
        
#=============================================================================================================================#
#=============================================================================================================================#      
  
#Running the starting screen loop to start the game#

if __name__ == "__main__": #only runs the file when the file is run from within the file
    #this is because i import some of the functions from here in another file and i dont want it to run the file there
    
    mainprogram() #run the starting screen program
                    
        

