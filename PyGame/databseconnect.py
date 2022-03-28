import mysql.connector
import csv





try: 
    conn = mysql.connector.connect(port = "3307", host = "127.0.0.1", user="root", passwd="usbw", db="Project")

except mysql.connector.Error as err:
    print ("Error with connection: {}".format(err))
else:
    print("Connection established")

c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS NamesScores (
            player1name VARCHAR(10),
            player2name VARCHAR(10),
            player1score smallint,
            player2score smallint);""")



def readscores():
    file =  open("scores.txt","r")

    csvfile = csv.reader(file)
    for column in csvfile:
        p1score=int(column[0])
        p2score=int(column[1])


    print(p1score,p2score)

    file.close()
    return p1score,p2score

def readnames():
    file =  open("names.txt","r")

    csvfile = csv.reader(file)
    for column in csvfile:
        p1name=(column[0])
        p2name=(column[1])


    print(p1name,p2name)

    file.close()
    return p1name,p2name



    
def recordscore(winners,goaldifference):
    scoresfile = open("leader.txt","w")

    for n in range (len(winners)):
        scoresfile.write(str(winners[n]))
        scoresfile.write(",")
        scoresfile.write(str(goaldifference[n]))
        scoresfile.write("\n")
        

            
    scoresfile.close()

##################################################

p1score, p2score = readscores()
p1name,p2name = readnames()

c.execute("""INSERT INTO NamesScores
            (player1name,player2name,player1score,player2score)
            VALUES (%s,%s,%s,%s)""",(p1name,p2name,p1score,p2score))

conn.commit()


c.execute("""

SELECT `player1name` AS Winner, (`player1score` - `player2score`) AS GoalDifference
FROM `namesscores`
WHERE `player1score` > `player2score`
LIMIT 0 , 30


UNION ALL

SELECT `player2name` AS Winner, (`player2score` - `player1score`) AS Goaldifference
FROM `namesscores`
WHERE `player2score` > `player1score`
LIMIT 0 , 30


""")

winners = []
goaldifference = []

for wn,gd in c:
    print (wn,gd)
    winners.append(wn)
    goaldifference.append(gd)

print (winners)
print (goaldifference)



recordscore(winners,goaldifference)





