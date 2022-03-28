
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

#defining an acceleration for the ball

ACCELERATION = 0.3

#--------------------------


#basic colours

BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)
BLUE = ( 0, 0, 255)


#--------------------------


#loading all the images for sprites 


Rightload =[pygame.image.load('R'+str(i)+'.png')  for i in range(1,10) ]
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

#defining time for the timer

starttime = time.time()

#--------------------------


#functions to transform all images and make them transparent

def getimage(image):
    image = pygame.transform.scale (image, (96,96))
    image.set_colorkey(WHITE)
    
    return image
    
    
def getimagedancing(image):
    image = pygame.transform.scale (image, (300,300))
    
    return image
    
#--------------------------



#Ball class for the football
velocity = [-10,-9,-8,-7,-6,-5,-4,-3,-2,-1,1,2,3,4,5,6,7,8,9,10]

class Ball():
    def __init__(self):
        self.x = 640
        self.y = 250
        self.velocity_y = random.choice(velocity)
        self.velocity_x = random.choice(velocity)
        self.radius = 15
        self.color = (WHITE)
        self.direction = [1,-1]


    def draw(self):
        pygame.draw.circle(screen, (self.color), (int(self.x),int(self.y)),self.radius)
        #pygame.draw.rect(int(self.x), int(self.y),10,140)

    def move(self):
        self.velocity_y += ACCELERATION
        self.y += self.velocity_y
        if self.y >= 500:
            self.velocity_y = -self.velocity_y


        if self.y > 550:
            self.reset()
            #p1.resetplayers(100,400)
            #p2.resetplayers(1000,400)
        
        


        self.x += self.velocity_x
        
        if self.velocity_x > 0:
            self.velocity_x - 1
        if self.velocity_x < 0:
            self.velocity_x + 1
            
            
    def reset(self):

        self.x = 640
        self.y = 250

        self.velocity_y = random.choice(velocity)
        self.velocity_x = random.choice(velocity)

#--------------------------


            
#Players class for both the sprites
    
                
class Players(object):
    def __init__(self,x,y,height,width):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 3
        self.isJump = False
        self.left = False
        self.right = False
        self.head = False
        self.walkCount = 0
        self.jumpCount = 10
        self.danceCount = 0
        self.walkLeft = []
        self.walkRight = []
        self.char = ()
        self.hitbox = (self.x + 25 , self.y + 5, 50 , 75)
        self.bighead= ()
        self.dance = False
        self.dancinlist =[]
        
    

    def draw(self, screen):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if self.danceCount + 1 >= 54:
            self.danceCount = 0

        if self.left:
            screen.blit(self.walkLeft [self.walkCount//3], (self.x,self.y))
            self.walkCount += 1
        elif self.right:
            screen.blit(self.walkRight [self.walkCount//3], (self.x,self.y))
            self.walkCount +=1
        elif self.head:
            screen.blit(self.bighead, (int(self.x),int(self.y)))
            self.hitbox = (self.x, self.y,self.height,self.width)
            pygame.draw.rect(screen, (255,0,0),(self.hitbox),2)
        elif self.dance:
            screen.blit(self.dancinlist [self.danceCount//9], (580,280))
            self.danceCount += 1
        else:
            screen.blit(self.char, (int(self.x),int(self.y)))
            
        
        self.hitbox = (self.x + 25 , self.y + 5, 50 , 75)
        pygame.draw.rect(screen, (255,0,0),(self.hitbox),2)

    def reset(self,x,y):
        self.x = x
        self.y = y
    
#--------------------------

#read the player names from the file to be able use them later

def readnames():
    file =  open("names.txt","r")

    csvfile = csv.reader(file)
    for column in csvfile:
        p1name=(column[0])
        p2name=(column[1])


    print(p1name,p2name)

    file.close()
    return p1name,p2name    
            
p1name,p2name = readnames()

#--------------------------

#function to record the scores of the players after the match ends
    
def recordscore(p1score,p2score):
    scoresfile = open("scores.txt","w")
    
    scoresfile.write(str(p1score))
    scoresfile.write(",")
    scoresfile.write(str(p2score))
    scoresfile.write("\n")

            
    scoresfile.close()

    
#--------------------------

#the main loop for the gameover window

def gameoverwindow(p1score,p2score):
    finishedovergame = False


    p1= Players(100,450,128,128)
    p2= Players(1000,450,128,128)
    
    
    
    p1.dancinlist = []
    p2.dancinlist = []
    
    font = pygame.font.SysFont('comicsans', 60)
    p1namedisplay = font.render(p1name, True, (BLUE))
    p2namedisplay = font.render(p2name, True, (RED))

    
    screen.blit(background,(0,0))
    pygame.draw.rect(screen, (WHITE),(100,100,1080,520))
    
    while finishedovergame == False:


        #timer
        elapsedtime = time.time() - starttime
        inttime = str(int(elapsedtime))

        if int(elapsedtime)>20:
            import leaderboard
            
        
        dan = 0
        while dan<6:
            dancingcalp1 = getimagedancing(dancingp1[dan])
            p1.dancinlist.append(dancingcalp1)
            
            dancingcalp2 = getimagedancing(dancingp2[dan])
            p2.dancinlist.append(dancingcalp2)
            
            
            dan +=1
            
        if p1score>p2score:
            pygame.draw.rect(screen, (BLUE),(100,100,1080,520),20)
            winnercolor = (BLUE)
            screen.blit(p1namedisplay, (800,200))
            p1.dance = True
            p1.draw(screen)
            
            
        elif p2score>p1score:
            pygame.draw.rect(screen, (RED),(100,100,1080,520),20)
            winnercolor= (RED)
            screen.blit(p2namedisplay, (800,200))
            p2.dance = True
            p2.draw(screen)
            
            
        else:
            pygame.draw.rect(screen, (BLACK),(100,100,1080,520),20)
            winnercolor = (WHITE)
        
        

        
        
        Congrats = font.render("CONGRATULATIONS", True, (winnercolor))
        
        screen.blit(Congrats, (120, 200))
        
        clock = pygame.time.Clock()    
        clock.tick(FPS)
        pygame.display.update()
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


#--------------------------


#defining the framerate for the game
                
FPS = 100


#--------------------------


#initialising the display

width, height = (1280, 720)
screen = pygame.display.set_mode((width, height))

#title, icon, background
pygame.display.set_caption("kick it")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)


backgroundimg = pygame.image.load('background.png')
background = pygame.transform.scale (backgroundimg, (width, height))


#--------------------------



#function to draw elements that go in the main loop

def redrawGameWindow(screen, p1, p2, ball):
    screen.blit(background, (0,0))
    n=0    
    p1.walkRight = []
    p1.walkLeft = []
        
    p2.walkRight = []
    p2.walkLeft = []

    
    p1.char = getimage(charimg)
    p2.char = getimage(charimgp2)

    p1.bighead = getimage(headimg)
    p2.bighead = getimage(headimgp2)
    
    
    
    while n <9:
        walkRightcal = getimage(Rightload[n])
        p1.walkRight.append(walkRightcal)
    
        walkRightcalp2 = getimage(Rightloadp2[n])
        p2.walkRight.append(walkRightcalp2)
    
        walkLeftcal = getimage(Leftload[n])
        p1.walkLeft.append(walkLeftcal)
    
        walkLeftcalp2 = getimage(Leftloadp2[n])
        p2.walkLeft.append(walkLeftcalp2)
    
        n+=1

    
        
    
    p1.draw(screen)
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
    
    while finished == False:
        
        #timer
        elapsedtime = time.time() - starttime
        inttime = str(int(elapsedtime))
        

        #displaying text on screen after timer runs out
        
        font = pygame.font.SysFont('comicsans', 60)
        processing = font.render("processing your scores", True, (0,0,0))
        
        gameover = font.render("gameover", True, (0,0,0))
        
        timer = font.render(inttime, True, (0,0,0))
        
        screen.blit(timer, (width/2, height/2))
        pygame.display.update()
        
        if int(elapsedtime) >= 50:
                   
            screen.blit(gameover, ((width/2)+50, (height/2)-50))
            screen.blit(processing, ((width/2)-50, (height/2)+50))
            pygame.display.update()
                   
            print(p1score)
            print(p2score)

            #record the scores using the function       
            recordscore(p1score,p2score)

            time.sleep(3)

            #run the database file to save scores to the database
            exec(open('databseconnect.py').read())

            print (int(elapsedtime))
            
            #run the gameoverwindow
            gameoverwindow(p1score,p2score)

            
            
        
        
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()




        #checking for keys pressed
        
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] and p1.x > 90:
            p1.x -= p1.vel
            p1.left = True
            p1.right = False
        elif keys[pygame.K_d] and p1.x < 1100:
            p1.x += p1.vel
            p1.right = True
            p1.left = False
        elif keys[pygame.K_s]:
            p1.head = True
        else:
            p1.right = False
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
            if p1.jumpCount >= -10:
                neg = 1
                if p1.jumpCount < 0:
                    neg = -1
                p1.y -= (p1.jumpCount ** 2) * 0.5 * neg
                p1.jumpCount -= 1
            else:
                p1.isJump = False
                p1.jumpCount = 10
                
                
                
                
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

        #drawing all the sprites on the screen using the function
                
        redrawGameWindow(screen, p1,p2, ball)
        

        
        #Checking for collisions   
        if ball.x <= p2.hitbox[0] + p2.hitbox[2] and ball.x >= (p2.hitbox[0]) and ball.y <= p2.hitbox[1] + p2.hitbox[3] and ball.y >= p2.hitbox[1]:
            ball.velocity_y = -ball.velocity_y
            ball.velocity_x = -ball.velocity_x
            
            if p2.right:
                if ball.velocity_x < 0:
                    ball.velocity_x = ball.velocity_x * -1
                if ball.velocity_x > 0:
                    ball.velocity_x += 1
                
            if p2.left:
                if ball.velocity_x > 0:
                    ball.velocity_x = ball.velocity_x * -1
                if ball.velocity_x > 0:
                    ball.velocity_x += 1
           
            
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
                    
                    
                    
     
        if ball.x <= 90 or ball.x >= 1195:
                
            
            if ball.x >=1195 and ball.y > 380:
                p1score += 1
                ball.color = (BLUE)
                ball.reset()
                print("blue:",p1score)
                 
                
            elif ball.x <= 90 and ball.y > 380:
                p2score += 1
                ball.color = (RED)
                ball.reset()
                print("red:",p2score)
                
            elif ball.y < 380 and ball.y > 200:
                print("check")
                ball.velocity_x = -ball.velocity_x
                ball.velocity_y = -ball.velocity_y
                
            else:
                ball.reset()
       
         
            
            
            
        pygame.display.update()
    pygame.quit() 


main()
    
