
##### THE GAME PROGRAM #####



#importing modules

import pygame
import sys
import time
import csv
import random

#--------------------------

#initialise pygame
pygame.init()



#--------------------------


#basic colours

BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)
BLUE = ( 0, 0, 255)


#--------------------------


#loading all the images for sprites 


Rightload =[pygame.image.load('R'+str(i)+'.png')  for i in range(1,10) ] #loading all the images for the animations (ive named them R1....R19 so i can load them easier)
Leftload =[pygame.image.load('L'+str(i)+'.png')  for i in range(1,10) ]
Rightloadp2=[pygame.image.load('R'+str(i)+'p2.png')  for i in range(1,10) ]
Leftloadp2=[pygame.image.load('L'+str(i)+'p2.png')  for i in range(1,10) ]
charimg = pygame.image.load ('char.png')
charimgp2 = pygame.image.load ('charp2.png')
headimg = pygame.image.load ('bigheadp1.png')
headimgp2 = pygame.image.load ('bigheadp2.png')
dancingp1 = [pygame.image.load('dancing'+str(i)+'p1.png')  for i in range(1,7) ]
dancingp2 = [pygame.image.load('dancing'+str(i)+'p2.png')  for i in range(1,7) ]

#--------------------------

#defining initial time for the timer

starttime = time.time()

#--------------------------


#functions to transform all images and make them transparent

def getimage(image):
    image = pygame.transform.scale (image, (96,96)) #changes the image to  96x96 pixels
    image.set_colorkey(WHITE) #removes the white background
    
    return image
    
    
def getimagedancing(image):
    image = pygame.transform.scale (image, (300,300)) #changes the image to  300x300 pixels
    
    return image
    
#--------------------------

#defining the framerate for the game
                
FPS = 100


#--------------------------


#initialising the display

width, height = (1280, 720)
screen = pygame.display.set_mode((width, height))

#title, icon, background, font
pygame.display.set_caption("kick it")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)


backgroundimg = pygame.image.load('background.png')
background = pygame.transform.scale (backgroundimg, (width, height))

font = pygame.font.SysFont('comicsans', 60)

#==============================================================================================================================================#
#==============================================================================================================================================#



#Ball class for the football


ACCELERATION = 0.3 #acceleration for the ball

velocity = [-10,-9,-8,-7,-6,-5,-4,-3,-2,2,3,4,5,6,7,8,9,10] #a list of velocities so it can randomly choose the speed (and direction because negative) it goes at everytime its reset

class Ball():
    def __init__(self):  #all the attributes of the ball
        self.x = 640
        self.y = 250
        self.velocity_y = random.choice(velocity)
        self.velocity_x = random.choice(velocity)
        self.radius = 15
        self.color = (WHITE)



    def draw(self):
        pygame.draw.circle(screen, (self.color), (int(self.x),int(self.y)),self.radius) #draws the ball on screen with the attributes defined above


    def move(self):
        self.velocity_y += ACCELERATION #adds acceleration when this function is called so the ball can move
        self.y += self.velocity_y #adds the velocity to the y value hence moving the ball

        
        if self.y >= 500:   #checks if the ball is touching the ground (which is at 500 y). If it is, it reverses the velocity giving the effect of it bouncing
            self.velocity_y = -self.velocity_y
            
            if self.velocity_x > 0:     #gradually slows down the ball to give the effect of gravity affecting it
                self.velocity_x - 1
            elif self.velocity_x < 0:   #if statements check the direction, it would be negative if going left
                self.velocity_x + 1


        if self.y > 550:    #in case the ball glitches and ends up under the ground, reset it
            self.reset(3)

        
        


        self.x += self.velocity_x #changes the x position according to the velocity
        
        
            
            
    def reset(self,why):

        #checks why the ball is being reset

        if why == 1:
            screen.blit((font.render(("GOAL! BLUE :D"), True, BLUE)), ((width/2)-200,(height/2))) #if its because it went in the blue net, then it shows goal for blue text on screen
            pygame.display.update()
            pygame.time.delay(1000)
        elif why == 2:
            screen.blit((font.render("GOAL! RED :D", True, RED)), ((width/2)-200,(height/2))) #if its because it went in the red net, then it shows goal for red text on screen
            pygame.display.update()
            pygame.time.delay(1000)
        else:
            screen.blit((font.render("OUT!", True, BLACK)), ((width/2)-70,(height/2))) #if its because it went out, then it shows out text on screen
            pygame.display.update()
            pygame.time.delay(1000)

        pygame.time.delay(300)
            
        self.x = 640  #sets the x and y values to the original values when the ball was first defined (when the game started)
        self.y = 250

        self.velocity_y = random.choice(velocity) #selects a random velocity from the list and the ball then goes in that direction and speed respectively for the next round
        self.velocity_x = random.choice(velocity)


#==============================================================================================================================================#
#==============================================================================================================================================#


            
#Players class for both the sprites
    
                
class Players():
    def __init__(self,x,y,height,width):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 3
        self.isJump = False #if the players jumping
        self.left = False   #if the players going left
        self.right = False  #if the players going right
        self.head = False   #if the players using the head function
        self.walkCount = 0  
        self.jumpCount = 10
        self.danceCount = 0
        self.walkLeft = []  #lists to store the sprites
        self.walkRight = []
        self.char = ()   #when the characters standing still
        self.hitbox = (self.x + 25 , self.y + 5, 50 , 75)  #hitbox
        self.bighead= () 
        self.dance = False #if the characters dancing
        self.dancinlist =[]
        
    

    def draw(self, screen):
        self.hitbox = (self.x + 25 , self.y + 5, 50 , 75)

        ##walking
        if self.walkCount + 1 >= 27: #As I have 9 images of each walking animation, I have set a variable walkcount to 27 as this would allow me to show each frame 3 times to show a smooth animation
            self.walkCount = 0 #when it gets to 27, just resets to 0


        ##dancing
        if self.danceCount + 1 >= 54: #As I have 6 images of each dancing animation, I have set a variable walkcount to 54 as this would allow me to show each frame 6 times to show a smooth animation
            self.danceCount = 0 #when it gets to 54, just resets to 0

            
        ##walkingleft
        if self.left:    #if the player uses the key to go left, self.left becomes true and this is run
            
            screen.blit(self.walkLeft [self.walkCount//3], (self.x,self.y)) #goes through the 9 images blits the images on screen for 3 frames from the walkLeft list which has all the 9 images of the left walking animation
            self.walkCount += 1
            
        ##walkingright   
        elif self.right:  #if the player uses the key to go right, self.right becomes true and this is run
            
            screen.blit(self.walkRight [self.walkCount//3], (self.x,self.y)) #same as above but this time uses the walkRight list which stores all the images for right animation
            self.walkCount +=1

            
        ##heading function    
        elif self.head: #if the player uses the key to head, self.head becomes true and this is run
            screen.blit(self.bighead, (int(self.x),int(self.y))) #blits the sprite with a bigger head
            self.hitbox = (self.x, self.y,self.height,self.width) #makes the hitbox bigger
            #pygame.draw.rect(screen, (255,0,0),(self.hitbox),2) #just for testing to make sure the hitbox does acc get bigger

        ##dancing     
        elif self.dance: #when the player wins, it does a dancing animation on the game over window
            screen.blit(self.dancinlist [self.danceCount//9], (580,280)) #goes through the dancingList and blits each image for 9 frames
            self.danceCount += 1

        ##standing still
        else:
            screen.blit(self.char, (int(self.x),int(self.y))) #if none of the above are true, just show the player standinh still
            
        
        
        #pygame.draw.rect(screen, (255,0,0),(self.hitbox),2)

#=============================================================================================================================#
#=============================================================================================================================#

#function to read the player names from the file to be able use them later

def readnames():
    file =  open("names.txt","r")

    csvfile = csv.reader(file)
    for column in csvfile:
        p1name=(column[0])
        p2name=(column[1]) #reads the name using csv 


    print(p1name,p2name)

    file.close()
    return p1name,p2name    
            
p1name,p2name = readnames()


#=============================================================================================================================#
#=============================================================================================================================#

#function to record the scores of the players after the match ends
    
def recordscore(p1score,p2score):
    scoresfile = open("scores.txt","w")
    
    scoresfile.write(str(p1score))
    scoresfile.write(",")
    scoresfile.write(str(p2score)) 
    scoresfile.write("\n")

            
    scoresfile.close()


#=============================================================================================================================#
#=============================================================================================================================#





#function to draw all elements that go in the main loop

def redrawGameWindow(screen, p1, p2, ball):
    screen.blit(background, (0,0)) #blits the background
    n=0

    ##defining lists for walk animations
    p1.walkRight = [] 
    p1.walkLeft = []
        
    p2.walkRight = []
    p2.walkLeft = []

    ##runs the images through the transform animation
    p1.char = getimage(charimg)
    p2.char = getimage(charimgp2)

    p1.bighead = getimage(headimg)
    p2.bighead = getimage(headimgp2)
    
    
    
    while n <9: #runs all the 9 images of the animations and appends them to the respective list
        walkRightcal = getimage(Rightload[n])
        p1.walkRight.append(walkRightcal)
    
        walkRightcalp2 = getimage(Rightloadp2[n])
        p2.walkRight.append(walkRightcalp2)
    
        walkLeftcal = getimage(Leftload[n])
        p1.walkLeft.append(walkLeftcal)
    
        walkLeftcalp2 = getimage(Leftloadp2[n])
        p2.walkLeft.append(walkLeftcalp2)
    
        n+=1

    
        
    
    p1.draw(screen) #draws the players and ball
    p2.draw(screen)
    ball.move()
    ball.draw()

    
#--------------------------------------------------------------    

    
#main loop for the game

def main():

    
    
    #initialising players and ball objects from the classes
    p1= Players(100,450,128,128)
    p2= Players(1000,450,128,128)
    
    ball = Ball()
    
    
    clock = pygame.time.Clock()
    finished = False 
    
    p1score = 0
    p2score = 0
    
    while finished == False: #while the game is running

        smallfont = pygame.font.SysFont('comicsans', 30) #setting base for font

        ##show the name and scores of the players as the game is going on (scorecard)
        p1display = smallfont.render(p1name, True, BLUE) 
        p1scdisplay = smallfont.render(str(p1score), True, BLUE)
        p2display = smallfont.render(p2name, True, RED)
        p2scdisplay = smallfont.render(str(p2score), True, RED)
        
        screen.blit(p1display, (160, 280))
        screen.blit(p1scdisplay, ((width/2)-40, 280))
        screen.blit(p2display, (900, 277))
        screen.blit(p2scdisplay, ((width/2)+10, 280))
        pygame.display.update()
        
        
        #timer
        elapsedtime = time.time() - starttime
        inttime = str(int(elapsedtime))
        

        #displaying text on screen after timer runs out
        
        font = pygame.font.SysFont('comicsans', 60)
        processing = font.render("processing your scores", True, (0,0,0)) #processing your score
        gameover = font.render("gameover", True, (0,0,0)) #gameover

        timelimit = str(90 - int(elapsedtime)) #counts down from 90
        timer = font.render(timelimit, True, (0,0,0))
        screen.blit(timer, (width/2 - 30, 5))
        
        pygame.display.update()
        
        if int(timelimit) <= 0: #if timer ends
            pygame.draw.rect(screen, (WHITE), ((width/2)-200,(height/2)-150, 350,100))
            screen.blit(gameover, ((width/2)-170, (height/2)-150)) #display "game over"
            pygame.draw.rect(screen, (WHITE), ((width/2)-320,(height/2)+50, 700,100))
            screen.blit(processing, ((width/2)-300, (height/2)+50)) #display "processing your score
            pygame.display.update()
                   
##            print(p1score)
##            print(p2score)

            #record the final scores in a text file using the function       
            recordscore(p1score,p2score)

            time.sleep(3) #sleep the screen for 3 seconds

            #run the database file to save scores to the database
            exec(open('databseconnect.py').read())
     
            #run the gameoverwindow
            gameoverwindow(p1score,p2score)

            
            
        
        #drawing all the sprites on the screen using the function       
        redrawGameWindow(screen, p1,p2, ball)

        #run the clock as per the frames per second defined
        clock.tick(FPS)



        #if the x in the top right corner is pressed, exit the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


        #------------------------------------

        #CHECKING FOR KEYS PRESSED
        
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] and p1.x > 90: #if player one presses A (left key), the walkingleft list is displayed and the velocity is taken away (going negative
            p1.x -= p1.vel
            p1.left = True
            p1.right = False
        elif keys[pygame.K_d] and p1.x < 1100: #if player one presses D (right key), the walkingright list is displayed and the velocity is added on
            p1.x += p1.vel
            p1.right = True
            p1.left = False
        elif keys[pygame.K_s]: #if player one presses S (key for head), the head sprite is displayed and the hitbox is changed (in the p1.head function)
            p1.head = True
        else:
            p1.right = False #else just stand still, and it will just displau the standing still photo
            p1.left = False
            p1.head = False
            p1.walkCount = 0
        
        if not(p1.isJump): 
            if keys[pygame.K_w]:
                p1.isJump = True
                p1.right = False
                p1.left = False
                p1.walkCount = 0
        else:
            if p1.jumpCount >= -10: # I am using a quadratic function to emulate a jump as a person gets slower the higher they get and then they reach terminal velocity, which is why i want a negative number so as it goes down to negatives, the square of that negative number would still be positive
                neg = 1 
                if p1.jumpCount < 0:
                    neg = -1
                    # once jump count gets to a negative number i have to times the function below by negative 1 because i'm taking away from the y value, if i didn't the player would jump up pause and then jump further up
                    #by making it negative it makes it so that i add on to the y value hence making the character go down
                p1.y -= (p1.jumpCount ** 2) * 0.5 * neg #times it by 0.5 just to make the jump smaller so they dont jump too high
                p1.jumpCount -= 1

            # the jumping function works on the basis that the y value of the player is decreased by 100 + 81 + 64 + 49 + 36..... (10 squared + 9 squared...) until it gets to 0.
            # at 0 it reaches terminal velocity and then it goes into negative numbers which would give the same result as above but then we times it by a negative which makes it so that the sprite goes down as add on the y value.
            #hence using the quadratic function it gives the effect of a player jumping as it gets slower the higher you get and when your closer to ground you're faster as gravity is affecting you.
            else:
                p1.isJump = False
                p1.jumpCount = 10
                
                
         ## everything below is the same as above but just for player 2       
                
        if keys[pygame.K_LEFT] and p2.x > 90:
            p2.x -= p2.vel
            p2.left = True
            p2.right = False
        elif keys[pygame.K_RIGHT] and p2.x < 1100:
            p2.x += p2.vel
            p2.right = True
            p2.left = False
        elif keys[pygame.K_DOWN]:
            p2.head = True
        else:
            p2.right = False
            p2.left = False
            p2.head = False
            p2.walkCount = 0
        
        if not(p2.isJump):
            if keys[pygame.K_UP]:
                p2.isJump = True
                p2.right = False
                p2.left = False
                p2.walkCount = 0
        else:
            if p2.jumpCount >= -10:
                neg = 1
                if p2.jumpCount < 0:
                    neg = -1
                p2.y -= (p2.jumpCount ** 2) * 0.5 * neg
                p2.jumpCount -= 1
            else:
                p2.isJump = False
                p2.jumpCount = 10

        
        #------------------------------------
        
        ##CHEKCING FOR COLLISIONS

        #check if the ball is in the player 1's hitbox        
        if ball.x <= p2.hitbox[0] + p2.hitbox[2] and ball.x >= (p2.hitbox[0]) and ball.y <= p2.hitbox[1] + p2.hitbox[3] and ball.y >= p2.hitbox[1]:  
            ball.velocity_y = -ball.velocity_y #if it touches player 1, reverse the velocities (bounce back)
            ball.velocity_x = -ball.velocity_x
            
            if p2.right: #while it touches the character, if the player is walking right: 
                if ball.velocity_x < 0:
                    ball.velocity_x = ball.velocity_x * -1 #if the balls coming towards the player (ball going left), bounce back
                if ball.velocity_x > 0:
                    ball.velocity_x += 2 #if the ball's going the same direction as the player (ball going right), increase the ball velocity
                
            if p2.left: #while it touches the character, if the player is walking left:
                if ball.velocity_x > 0:
                    ball.velocity_x = ball.velocity_x * -1 #if the balls coming towards the player (ball going right), bounce back
                if ball.velocity_x > 0:
                    ball.velocity_x += 2 #if the ball's going the same direction as the player (ball going left), increase the ball velocity
           
        #check if the ball is in the player 2's hitbox

        #everything same as above just for player 2
        if ball.x <= p1.hitbox[0] + p1.hitbox[2] and ball.x >= (p1.hitbox[0]) and ball.y <= p1.hitbox[1] + p1.hitbox[3] and ball.y >= p1.hitbox[1]:
            ball.velocity_y = -ball.velocity_y
            ball.velocity_x = -ball.velocity_x
            
            if p1.right:
                if ball.velocity_x < 0:
                    ball.velocity_x = ball.velocity_x * -1
                if ball.velocity_x > 0:
                    ball.velocity_x += 1
                
            if p1.left:
                if ball.velocity_x > 0:
                    ball.velocity_x = ball.velocity_x * -1
                if ball.velocity_x > 0:
                    ball.velocity_x += 1
                    
                    
                    
        #if the ball goes out of the field:
                    
        if ball.x <= 90 or ball.x >= 1195:
                
            
            if ball.x >=1195 and ball.y > 380: #if ball touches player 2's goalpost
                p1score += 1 #add a goal to player 1's total
                ball.color = (BLUE) #change the ball's colour to blue for the next round
                ball.reset(1) #reset the ball with goal for blue display
                #print("blue:",p1score)
                 
                
            elif ball.x <= 90 and ball.y > 380: #if ball touches player 1's goalpost
                p2score += 1 #add a goal to player 2's total
                ball.color = (RED) #change the ball's colour to red for the next round
                ball.reset(2) #reset the ball with goal for red display
                #print("red:",p2score)
                
            elif ball.y < 380 and ball.y > 240: #check if the ball touches crossbar on either side
                #print("check")
                ball.velocity_x = -ball.velocity_x #bounce back
                screen.blit((font.render(("CROSSBAR! so close!"), True, WHITE)), ((width/2)-220,(height/2))) #display that it hit the crosbar
                pygame.display.update()
                pygame.time.delay(300)
                
            else: #else if the ball has just gone out (above the goalposts and crossbar)
                ball.reset(3) #reset the ball with the out display

       
         
            
            
            
        pygame.display.update()
    pygame.quit() 




#=============================================================================================================================#
#=============================================================================================================================#



#the main loop for the gameover window

def gameoverwindow(p1score,p2score):
    finishedovergame = False


    p1= Players(100,450,128,128) #assigning players
    p2= Players(1000,450,128,128)
    
    
    
    p1.dancinlist = [] #defining a list for the animation for each player
    p2.dancinlist = []
    
    
    p1namedisplay = font.render(p1name, True, (BLUE)) #to display the winner name
    p2namedisplay = font.render(p2name, True, (RED))

    
    screen.blit(background,(0,0)) 
    pygame.draw.rect(screen, (WHITE),(100,100,1080,520)) #draw a white rectangle
    
    while finishedovergame == False:


        #timer
        elapsedtime = time.time() - starttime
        inttime = str(int(elapsedtime))

        if int(elapsedtime)>=105: #the game lasts for 90 seconds, so the game over window lasts for 15 seconds, and then it imports the leaderboard file
            import leaderboard
            
        
        dan = 0
        while dan<6: #importing all the 6 images, running them through the transform function and then adding them to the dancing lists
            dancingcalp1 = getimagedancing(dancingp1[dan])
            p1.dancinlist.append(dancingcalp1)
            
            dancingcalp2 = getimagedancing(dancingp2[dan])
            p2.dancinlist.append(dancingcalp2)
            
            
            dan +=1
            
        if p1score>p2score: # if player 1 wins
            pygame.draw.rect(screen, (BLUE),(100,100,1080,520),20) #draw a blue outline around the white rectangle
            winnercolor = (BLUE) #set winner colour to blue
            screen.blit(p1namedisplay, (650,200)) #display winners name
            p1.dance = True #run the dance function for player 1
            p1.draw(screen)
            
            
        elif p2score>p1score: # if player 2 wins
            pygame.draw.rect(screen, (RED),(100,100,1080,520),20) #draw a red outline around the white rectangle
            winnercolor= (RED) #set winner colour to blue
            screen.blit(p2namedisplay, (650,200)) #display winners name
            p2.dance = True #run the dance function for player 2
            p2.draw(screen)
            
            
        else: # if there is no winner
            pygame.draw.rect(screen, (BLACK),(100,100,1080,520),20) #draw a red outline around the white rectangle
            winnercolor = (WHITE) #set winner colour to white, as its a white background, the congratulations would just be displayed in white and the players wont be able to see it
            draw = font.render("The game ended in a draw :D", True, (BLACK)) 
            wp = font.render("well played both of you!", True, (BLACK)) 
            screen.blit(draw, (200, 250)) #display it ended in a draw
            screen.blit(wp, (250, 370)) #congratulate bot the players

        Congrats = font.render("CONGRATULATIONS", True, (winnercolor)) #in all cases it would display a congratulations in the colour of the winner, or white in case of a draw
        
        screen.blit(Congrats, (120, 200))
        
        clock = pygame.time.Clock()    
        clock.tick(FPS)
        pygame.display.update()
        
        # if the x at the top right hand corner is pressed, close the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


#=============================================================================================================================#
#=============================================================================================================================#


##RUN THE MAIN FUNCTION TO START THE GAME
                
main()
    
