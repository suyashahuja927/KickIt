
#LEADERBOARD

#=============================================================================================================================#
#=============================================================================================================================#

#import modules

import pygame
import csv
import os
import sys
from start import * #imports all the classes and functions from the database file

#--------------------------------------------------

winners = [] #setting up lists
goaldifference = []

#--------------------------------------------------

#imitialising pygame

pygame.init()

#--------------------------------------------------



def readleaderboard(winners,goaldifference): #read the leaderboard file and store the data in the lists
    file =  open("leader.txt","r")

    csvfile = csv.reader(file)
    
    for column in csvfile:
        wn=(column[0])
        winners.append(wn)
        gd=int(column[1])
        goaldifference.append(gd)


    file.close()
    return winners,goaldifference



def fadetable(width,height,searchinput): #fade function for transition
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


#=============================================================================================================================#
#=============================================================================================================================#

#SORT ALGORITHM - Bubble Sort

def bubblesort(goaldifference,winners): #descending to print biggest goal difference
    for outer in range(len(goaldifference)-1,0,-1): 
        for inner in range(outer):
            if goaldifference[inner]<goaldifference[inner+1]: # loops through the list, if current list item is smaller than the next one, 
                temp = goaldifference[inner] # set current to temporary
                tempn = winners[inner]
                goaldifference[inner] = goaldifference [inner+1] #set next one in the list as current
                winners[inner] = winners[inner+1]
                goaldifference[inner+1] = temp #set temporary to the next
                winners[inner+1] = tempn

    return goaldifference,winners


def bubblesortalphabetically(winners,goaldifference): #same as above but this time its ascending
    for outer in range(len(winners)-1,0,-1):
        for inner in range(outer):
            if winners[inner].lower()>winners[inner+1].lower():  #.lower() function makes the text lowercase so when comparing both of them are lowercase and it doesnt have to be case sensitive
                temp = winners[inner]
                tempn = goaldifference[inner]
                winners[inner] = winners[inner+1]
                goaldifference[inner] = goaldifference[inner+1]
                winners[inner+1] = temp
                goaldifference[inner+1] = tempn

    return winners,goaldifference

#=============================================================================================================================#
#=============================================================================================================================#


#SEARCH ALGORITH - BINARY SEARCH

searchname = []
searchgd = []


def binarysearch(searchinput):

    
    winalpha,gdalpha = bubblesortalphabetically(winners,goaldifference) #run the lists through bubble sort as lists need to be sorted before binary search
    
    found = False
    startpos = 0
    endpos = len(winalpha)-1

    while (startpos <= endpos) and found == False: #while the target isn't found
        middle = (startpos + endpos)//2
        if winalpha[middle].lower() == searchinput.lower(): #if the middle of the list is equal to the target
            found = True
            
            searchname.append(winalpha[middle]) #add the target to the search final list
            searchgd.append(gdalpha[middle])
            
            winalpha.remove(winalpha[middle]) #remove them from the original list so we can run it again
            gdalpha.remove(gdalpha[middle])
            
            try: #try the search again
                binarysearch(searchinput)
                
            except: #if there is an error print stop   
                print ("stop")
                #return searchname,searchgd
            
            else: #if it works run it and store the values
                return searchname,searchgd
                searchnamelist = [] 
                searchgdlist = []
        
            
        elif winalpha[middle].lower() < searchinput.lower(): #if its smaller, change the startpos to the start of 2nd half of the list as it cant be in the first half and searches in that half
            startpos = middle + 1
            
        else: #if its bigger, change the endpos to the end of the first half so it searches through that half
            endpos = middle - 1


    
#=============================================================================================================================#
#=============================================================================================================================#    
    

#Function to draw everything in the table screen   
    
backbuttontable=button(20,600,100,350,(RED),'BACK TO START') #assigning objects from the button class (from start.py)
sortbutton=button(400, 600, 100, 380, (RED), 'SORT BY HIGHEST GD')
searchbox = inputboxes(820, 600, 100,400,(BLACK))

        
def drawtablewindow(searchinput,sorting): #sorting allows it to draw the correct table

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

    
    if sorting == 1: #if sorting is 1, then it draws the first 10 entries from from the database
         for n in range(10):
            winnerprinter = font.render(winners[n],True,(BLACK))
            screen.blit((winnerprinter), (250, (75 + (50*n))))
            gdprinter = font.render(str(goaldifference[n]),True,(BLACK))
            screen.blit((gdprinter), (950, (75 + (50*n))))

           
    elif sorting == 2: #if sorting is 2, then it draws the first 10 entries from from the bubble sort algorithm
        
        
        sortedgd, sortedwn = bubblesort(goaldifference,winners)
        
        for n in range(10):
            winnerprinter = font.render(sortedwn[n],True,(BLACK))
            screen.blit((winnerprinter), (250, (75 + (50*n))))
            gdprinter = font.render(str(sortedgd[n]),True,(BLACK))
            screen.blit((gdprinter), (950, (75 + (50*n))))


#--------------------------------------------------

    
#funtion to draw the results of what they search
            
def drawtablesearch(searchinput,searchnamelist,searchgdlist): 
    
    
    finished = False

    try: #try running the binary search 
        searchnamelist, searchgdlist = binarysearch(searchinput)
    except: # there would be an error when it isn't able to find a result because it wont be able to return the searchnamelist and searchgdlist out of the function as they're empty if none of the 
        print ("not found")
    else: #if there's no errors print them on screen
        print(searchnamelist,searchgdlist)
    
    while finished == False:

        font=pygame.font.SysFont('comicsans',20)

        #drawing the table
        
        screen.blit(background,(0,0))    
        pygame.draw.rect(screen, (WHITE), (15, 15, 1250, 550))
        pygame.draw.rect(screen, (BLACK), (15, 15, 1250, 550),5)
        pygame.draw.line(screen,(BLACK),(630,15),(630,563),5)
        x = 65
            
        while x<565: # drawing the lines in between columns using a loop to save code
            pygame.draw.line(screen,(BLACK),(15,x),(1263,x),5)
            x+=50
                
        backbuttontable.draw(screen,(WHITE)) #draw the back button

        searchbox.draw() #draw the search box
        search = font.render ("search by name below:", True, (BLACK)) #text

        winnercolumn = font.render ("WINNERS", True, (RED))
        gdcolumn = font.render ("GOAL DIFFERENCE", True, (RED))

        takeinputsearch = font.render (searchinput, True, (WHITE))

        screen.blit(takeinputsearch, (searchbox.x + 10,searchbox.y + 10))
        screen.blit(winnercolumn, (250, 30))
        screen.blit(gdcolumn, (850, 30))
        screen.blit(search, (searchbox.x + 5, searchbox.y - 30))

        for n in range(len(searchname)): #display the names they searched for in the table
            winnerprinters = font.render(searchnamelist[n],True,(BLACK))
            screen.blit((winnerprinters), (250, (75 + (50*n))))
            gdprinters = font.render(str(searchgdlist[n]),True,(BLACK))
            screen.blit((gdprinters), (950, (75 + (50*n))))

        

        for event in pygame.event.get():
            
            pos = pygame.mouse.get_pos()
            

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                font=pygame.font.SysFont('comicsans',20)

            if event.type == pygame.MOUSEBUTTONDOWN: #if they press mouse button

                if backbuttontable.isOver(pos): #if theyre hovering over back button when pressing it:
                    fadetable(width,height,searchinput) #fade
                    mainprogram() #run the mainprogram from start.py


                if searchbox.isOver(pos): # if theyre hovering over the search box when pressing mouse:
                    searchbox.active=True #changes colour and allows people to type in it
                else:
                    searchbox.active=False

            if searchbox.active == True:
                searchbox.color = WHITE

            elif searchbox.active == False:
                searchbox.color = BLACK
      
                    
            if event.type == pygame.MOUSEMOTION:
               
                if backbuttontable.isOver(pos): #if theyre hovering over the back button, change colour
                    backbuttontable.color=(WHITE)
                else:
                    backbuttontable.color=(RED)

            if event.type == pygame.KEYDOWN: 
                if searchbox.active == True: # if the searchbox is selected while they're typing:
            
                    if event.key == pygame.K_BACKSPACE:
                        searchinput = searchinput[:-1] #take away the last letter from the string

                    elif event.key == pygame.K_RETURN: #if they press enter,

                        searchbox.color = BLACK #change box colour to black
                        searchbox.active = False #set active to false
                        
                        searchnamelist = [] #define lists to store results in
                        searchgdlist = []
                        drawtablesearch(searchinput,searchnamelist,searchgdlist)
 
                    else: #if any key is pressed, add it onto the string as input
                        searchinput += event.unicode 
    
        pygame.display.update()
      
        clock = pygame.time.Clock()
        clock.tick (FPS)
        
#--------------------------------------------------
        
def tablescreen(): #main loop for the table screen

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

                if backbuttontable.isOver(pos): # if pressed on back button - fades, goes back to main program
                    fadetable(width,height,searchinput)
                    mainprogram()

                if sortbutton.isOver(pos): #if pressed on the sort by highest gd button - redraws the table but with the sorted list
                    drawtablewindow(searchinput, 2)

                if searchbox.isOver(pos):
                    searchbox.active=True
                    
                else:
                    searchbox.active=False
                    
            #everything else is same as the function above
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

                        searchbox.color = BLACK

                        searchnamelist = []
                        searchgdlist = []
                        
                        drawtablesearch(searchinput,searchnamelist,searchgdlist)
 
                    else:
                        searchinput += event.unicode


                    


        pygame.display.update()

        
        clock.tick(FPS)



#=============================================================================================================================#
#=============================================================================================================================#   


winners,goaldifference = readleaderboard(winners,goaldifference) # read the original files from the database


#--------------------------------------------------
   
        

tablescreen() #run the main loop 

