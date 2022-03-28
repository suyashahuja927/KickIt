import pygame
import csv
import os
import sys
from start import *

winners = []
goaldifference = []

def readleaderboard(winners,goaldifference):
    file =  open("leader.txt","r")

    csvfile = csv.reader(file)
    
    for column in csvfile:
        wn=(column[0])
        winners.append(wn)
        gd=int(column[1])
        goaldifference.append(gd)


    file.close()
    return winners,goaldifference

def fadetable(width,height,searchinput):
    fade = pygame.Surface((width, height))
    fade.fill((0,0,0))
    opacity = 0
    for o in range(0, 40):
        opacity += 10
        fade.set_alpha(opacity)
        drawtablewindow(searchinput,1)
        screen.blit(fade, (0,0))
        pygame.display.update()
        pygame.time.delay(1)

        

sorting = 1


def bubblesort(goaldifference,winners):
    for outer in range(len(goaldifference)-1,0,-1):
        for inner in range(outer):
            if goaldifference[inner]<goaldifference[inner+1]:
                temp = goaldifference[inner]
                tempn = winners[inner]
                goaldifference[inner] = goaldifference [inner+1]
                winners[inner] = winners[inner+1]
                goaldifference[inner+1] = temp
                winners[inner+1] = tempn

    return goaldifference,winners

def bubblesortalphabetically(winners,goaldifference):
    for outer in range(len(winners)-1,0,-1):
        for inner in range(outer):
            if winners[inner].lower()>winners[inner+1].lower():
                temp = winners[inner]
                tempn = goaldifference[inner]
                winners[inner] = winners[inner+1]
                goaldifference[inner] = goaldifference[inner+1]
                winners[inner+1] = temp
                goaldifference[inner+1] = tempn

    return winners,goaldifference

searchname = []
searchgd = []

def binarysearch(searchinput):


    winalpha,gdalpha = bubblesortalphabetically(winners,goaldifference)
    
    found = False
    startpos = 0
    endpos = len(winalpha)-1

    print ("endpos at beginning =" , endpos)

    while (startpos <= endpos) and found == False:
        middle = (startpos + endpos)//2
        if winalpha[middle].lower() == searchinput.lower():
            found = True
            print (middle)
            print (winalpha[middle])
            print (gdalpha[middle])
            searchname.append(winalpha[middle])
            searchgd.append(gdalpha[middle])
            winalpha.remove(winalpha[middle])
            gdalpha.remove(gdalpha[middle])
            
            binarysearch(searchinput)
        
            return searchname,searchgd
            
        elif winalpha[middle].lower() < searchinput.lower():
            startpos = middle + 1
        else:
            endpos = middle - 1

        #return searchname,searchgd
    
    
    
    
    
backbuttontable=button(20,600,100,350,(RED),'BACK TO START')
sortbutton=button(400, 600, 100, 380, (RED), 'SORT BY HIGHEST GD')
searchbox = inputboxes(820, 600, 100,400,(BLACK))

        
def drawtablewindow(searchinput,sorting):

    font=pygame.font.SysFont('comicsans',20)
    
    screen.blit(background,(0,0))    
    pygame.draw.rect(screen, (WHITE), (15, 15, 1250, 550))
    pygame.draw.rect(screen, (BLACK), (15, 15, 1250, 550),5)
    pygame.draw.line(screen,(BLACK),(630,15),(630,563),5)
    x = 65
        
    while x<565: 
        pygame.draw.line(screen,(BLACK),(15,x),(1263,x),5)
        x+=50
            
    backbuttontable.draw(screen, (WHITE))
    sortbutton.draw(screen,(WHITE))
    searchbox.draw()
    search = font.render ("search by name below:", True, (BLACK))

    winnercolumn = font.render ("WINNERS", True, (RED))
    gdcolumn = font.render ("GOAL DIFFERENCE", True, (RED))

    takeinputsearch = font.render (searchinput, True, (WHITE))

    screen.blit(takeinputsearch, (searchbox.x + 10,searchbox.y + 10))
    screen.blit(winnercolumn, (250, 30))
    screen.blit(gdcolumn, (850, 30))
    screen.blit(search, (searchbox.x + 5, searchbox.y - 30))

    
    if sorting == 1:
         for n in range(10):
            winnerprinter = font.render(winners[n],True,(BLACK))
            screen.blit((winnerprinter), (250, (75 + (50*n))))
            gdprinter = font.render(str(goaldifference[n]),True,(BLACK))
            screen.blit((gdprinter), (950, (75 + (50*n))))

           
    elif sorting == 2:        
        
        
        sortedgd, sortedwn = bubblesort(goaldifference,winners)
        for n in range(10):
            
            winnerprinter = font.render(sortedwn[n],True,(BLACK))
            screen.blit((winnerprinter), (250, (75 + (50*n))))
            gdprinter = font.render(str(sortedgd[n]),True,(BLACK))
            screen.blit((gdprinter), (950, (75 + (50*n))))

    

def drawtablesearch(searchinput):
    
    clock = pygame.time.Clock()
    finished = False


    font=pygame.font.SysFont('comicsans',20)
    screen.blit(background,(0,0))    
    pygame.draw.rect(screen, (WHITE), (15, 15, 1250, 550))
    pygame.draw.rect(screen, (BLACK), (15, 15, 1250, 550),5)
    pygame.draw.line(screen,(BLACK),(630,15),(630,563),5)
    x = 65
        
    while x<565: 
        pygame.draw.line(screen,(BLACK),(15,x),(1263,x),5)
        x+=50
            
    backbuttontable.draw(screen, (WHITE))
    sortbutton.draw(screen,(WHITE))
    searchbox.draw()
    search = font.render ("search by name below:", True, (BLACK))

    winnercolumn = font.render ("WINNERS", True, (RED))
    gdcolumn = font.render ("GOAL DIFFERENCE", True, (RED))

    takeinputsearch = font.render (searchinput, True, (WHITE))

    screen.blit(takeinputsearch, (searchbox.x + 10,searchbox.y + 10))
    screen.blit(winnercolumn, (250, 30))
    screen.blit(gdcolumn, (850, 30))
    screen.blit(search, (searchbox.x + 5, searchbox.y - 30))

    searchname, searchgd = binarysearch(searchinput)
    print(searchname)
    print(searchgd)


    for n in range(len(searchname)):

        winnerprinters = font.render(searchname[n],True,(BLACK))
        screen.blit((winnerprinters), (250, (75 + (50*n))))
        gdprinters = font.render(str(searchgd[n]),True,(BLACK))
        screen.blit((gdprinters), (950, (75 + (50*n))))
            

    while finished == False:
        


        for event in pygame.event.get():
            
            pos = pygame.mouse.get_pos()
            

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                font=pygame.font.SysFont('comicsans',20)
    
        pygame.display.update()
      
    
        

        
def tablescreen():

    searchinput = ''
    
    clock = pygame.time.Clock()
    finished = False
        
    while finished == False:
        
        drawtablewindow(searchinput,1)

        for event in pygame.event.get():
            
            pos = pygame.mouse.get_pos()
            

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                

            if event.type == pygame.MOUSEBUTTONDOWN:

                if backbuttontable.isOver(pos):
                    fadetable(width,height,searchinput)
                    mainprogram()

                if sortbutton.isOver(pos):
                    drawtablewindow(searchinput, 2)

                if searchbox.isOver(pos):
                    searchbox.active=True

                    
                else:
                    searchbox.active=False

            if searchbox.active == True:
                searchbox.color = WHITE

            elif searchbox.active == False:
                searchbox.color = BLACK
      
                    
            if event.type == pygame.MOUSEMOTION:
               
                if backbuttontable.isOver(pos):
                    backbuttontable.color=(WHITE)
                else:
                    backbuttontable.color=(RED)

                if sortbutton.isOver(pos):
                    sortbutton.color=(WHITE)
                else:
                    sortbutton.color = (RED)

            if event.type == pygame.KEYDOWN:
                if searchbox.active == True:
                    if event.key == pygame.K_BACKSPACE:
                        searchinput = searchinput[:-1]

                    elif event.key == pygame.K_RETURN:

                        searchbox.active = False
                        drawtablesearch(searchinput)
 
                    else:
                        searchinput += event.unicode


                    


        pygame.display.update()

        
        clock.tick(FPS)


#------------------------






#========================




winners,goaldifference = readleaderboard(winners,goaldifference)






print (winners)
print (goaldifference)
   



        

tablescreen()

