
#DATABASE FILE

#=============================================================================================================================#
#=============================================================================================================================#      

#importing modules

import mysql.connector
import csv


#--------------------------------------------------

#try to make a connection
try:
    #command to establish a connection the "project database" on the webserver
    conn = mysql.connector.connect(port = "3307", host = "127.0.0.1", user="root", passwd="usbw", db="Project")

except mysql.connector.Error as err: #if there is an error print what it is
    print ("Error with connection: {}".format(err))
    
else: #else if the connection was succesfull
    print("Connection established")
    c = conn.cursor() #assign a cursor to navigate the database

#--------------------------------------------------
    
#sql command to create the table to store the data
c.execute("""CREATE TABLE IF NOT EXISTS NamesScores (
            player1name VARCHAR(10),
            player2name VARCHAR(10),
            player1score smallint,
            player2score smallint);""")



#=============================================================================================================================#
#=============================================================================================================================# 

#functions

def readscores(): #reading the scores from the scores file and storing them as variables
    file =  open("scores.txt","r")

    csvfile = csv.reader(file)
    for column in csvfile:
        p1score=int(column[0])
        p2score=int(column[1])


    print(p1score,p2score)

    file.close()
    return p1score,p2score

def readnames(): #reading the names from the names file and storing them as variables
    file =  open("names.txt","r")

    csvfile = csv.reader(file)
    for column in csvfile:
        p1name=(column[0])
        p2name=(column[1])


    print(p1name,p2name)

    file.close()
    return p1name,p2name



    
def recordscore(winners,goaldifference): #writes the name of the winner and goaldifference they won by in a csv file
    scoresfile = open("leader.txt","w")

    for n in range (len(winners)):
        scoresfile.write(str(winners[n]))
        scoresfile.write(",")
        scoresfile.write(str(goaldifference[n]))
        scoresfile.write("\n")
        

            
    scoresfile.close()
    

#=============================================================================================================================#
#=============================================================================================================================#      



p1score, p2score = readscores() #get variables from the functions
p1name,p2name = readnames()

#insert the variables into the table
c.execute("""INSERT INTO NamesScores
            (player1name,player2name,player1score,player2score)
            VALUES (%s,%s,%s,%s)""",(p1name,p2name,p1score,p2score)) #using string formatting to put in variables

conn.commit()


#--------------------------------------------------

# SQL QUERY TO FIND THE WINNER AND THE GOAL DIFFERENCE THEY WON BY FROM THE 4 COLUMNS

c.execute("""

SELECT `player1name` AS Winner, (`player1score` - `player2score`) AS GoalDifference
FROM `namesscores`
WHERE `player1score` > `player2score`


UNION ALL 

SELECT `player2name` AS Winner, (`player2score` - `player1score`) AS Goaldifference
FROM `namesscores`
WHERE `player2score` > `player1score`


""") #"union" combines the 2 queries into one as they both have the same arguments for SELECT. "all" allows duplicates



winners = [] #making new lists to store data
goaldifference = []

for wn,gd in c: #run the query and store the data in the lists
    print (wn,gd)
    winners.append(wn)
    goaldifference.append(gd)

#print (winners)
#print (goaldifference)

#--------------------------------------------------

recordscore(winners,goaldifference) #save the lists into a csv file to be accessed outside





