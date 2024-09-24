'''
Program name: SaveGame.py
Description: Saves how many times each player has won
Inputs: who won the game and a txt file
Outputs: a txt file
Sources of code: None 
Authors: Kyle
Creation Date: 9/23/24
'''

from os import system, name #sets the system name to name

Player1, Player2, CPU = range(3) #enumorators for each player

''' 
def getSystem()
    if name == 'nt':
        #windows save file
        print("windows")
    else:
        #linux save file
        print("linux")
'''

'''
if there is no save file one is created. writes all of the data from
the games that were played to the save file
save file is saved locally and it is marked as unchanged so that 
it does not get pushed to the repo
'''
def updateSave(winner):
    validate() #if there is no save file it will create one if there is already one then the program will continue 
    try:
        temp = getSave() #sets a temporary list to whatever the contents of the file are
        f = open("save.txt", "w") #opens the existing save file
        temp[winner] = str(int(temp[winner]) + 1) #adds 1 to the counter of whoever won the game converts string to int to add then back to string to append
        for i in temp: #for every element i in the temporary list write the element i and then a newline after that to the file
            f.write(i)
            f.write('\n')
        f.close() #close the file
    except:
        print("error")  #error message

'''
Gets the content from the current save file as a list
'''
def getSave():
    try:
        f = open("save.txt", "r") #opens the existing save file
        data = [] #temporary variable to hold contents of save file
        for line in f: #for every line in the save file
            data.append(line.rstrip('\n')) #append the line to the data list without an '\n'
        f.close() #close the file
        return data #return the list of the contents of the data file
    except:
        print("error")


'''
initialize and or validate that there is a scorebard as save.txt
'''
def validate():
    try:
        f = open("save.txt", "r") #opens the existing save file and then closes it to validate it is there
        f.close()
    except:
        f = open("save.txt", "w" )
        f.write("0\n0\n0") #writes 0 wins for each player into the new file assuming there is not one there and closes it 
        f.close()

'''
prints the scoreboard
'''
def printScoreBoard():
    try:
        f = open("save.txt", "r")
        data = [] #temporary variable to hold contents of save file
        for line in f: #for every line in the save file
            data.append(line.rstrip('\n')) #append the line to the data list without an '\n'
        print("************ Score Board ************")
        print(f"Player 1 has won {data[Player1]} times")
        print(f"Player 2 has won {data[Player2]} times")
        print(f"CPU has won {data[CPU]} times")
    except:
        print("scoreboard is missing")

def test():
    #strucute of list and save file
    #update with respecive player's number adds 1 to their score on how many times they have won
    #player 1 is 0
    #player 2 is 1
    #cpu is 2 
    updateSave(0)
    updateSave(2)
    updateSave(2)