import numpy as np

# Eksempel på kørsel:
# new 3 3 tic put O b2
# laver nyt bræt som er 3x3, bruger spilleregler for tic tac toe og forsøger at putte en bolle på b2.

# Dictionary der definere positioner for bogstaver. Starter ved 1 fordi plads 0 bliver brugt af pladens tal visere.
position = {"a" : 1, "b" : 2, "c" : 3, "d" : 4, "e" : 5, "f" : 6, "g" : 7, "h" : 8, "i" : 9, "j" : 10, "k" : 11, "l" : 12, "m" : 13, "n" : 14};
print(position);

global boardRows;
global boardColumns;
global board;
global game;
game = "";
# Funktion som opsætter spillebrættet med de ønskede dimensioner, og sætter bogstaver øverst og tal på siden.
def boardSetup(rows, columns):
    # boardRows = int(input("Rows of the board: "))+1
    # boardColumns = int(input("Columns of the board: "))+1
    global boardRows
    global boardColumns
    boardRows = rows + 1
    boardColumns = columns + 1
    global board
    board = [[" " for x in range(boardColumns)] for y in range(boardRows)]
    letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N',]

    # Sætter bogstaver øverst på brættet
    for i in range(1, boardColumns):
        board[0][i] = letters[i-1]
    
    # Sætter tal i siden på brættet
    for i in range(1, boardRows):
        board[i][0] = i

    # Sætter første felt til at være et ikke iøjefaldende symbol.
    board[0][0] = "~"

    # Printer brættet
    # for i in range(boardRows):    gammel print funktion
    #    print(board[i][:])
    print(np.matrix(board))


# Funktion som tager en string tekst, og deler den tekst op i en liste af strenge, hvor de er indelt af mellemrummet. "hej du" bliver til ["hej", "du"]
def lexer(tekst):
    argumentList = []
    tmp = ""

    for i in range(len(tekst)):
        if tekst[i] == " ":
            argumentList.append(tmp)
            tmp = ""
        else:
            tmp = tmp + tekst[i]
    argumentList.append(tmp)
    return argumentList

# Tager tokens listen lavet af lexeren ind, og patternmatcher med korrekte funktionskald. 
# Hvis der er et korrekt patternmatch kalder den den reele funktion. F.eks. 'new 5 7' og
# 'move a1 b2'.
def parser(tokens):
    global game
    argRow = 0
    argCol = 0
    argFrom = ""
    argTo = ""
    for i in range(len(tokens)):
        if tokens[i] == "new":
            print("keyword 'new' accepted")
            argRow = int(tokens[i+1])
            argCol = int(tokens[i+2])
            boardSetup(argRow, argCol)     # kalder funktionen 'boardSetup' som laver et bræt ud fra 2 argumenter. F.eks. 'new 5 7' laver 5x7 bræt.
            print(argFrom+argTo)
        elif tokens[i] == "move":
            print("keyword 'move' accepted")
            argFrom = tokens[i+1]
            argTo = tokens[i+2]
            # Tester om argumenterne er af længden 2. F.eks. 'h2'. Ellers er det ikke lovligt
            if (len(argFrom) == 2 and len(argTo) == 2):
                # move(argFrom, argTo)      kalder en funktion der ikke er oprettet endnu
                print("succesfully moved " + argFrom + " to " + argTo) # TEST PRINT
            else:
                print("Not a valid operation. Use coordinates from and to.") # error message
        # put Z a1, putter et 'Z' på plads a1.
        elif tokens[i] == "put":
            print("keyword 'put' accepted")
            if tokens[i+1] == "x" or tokens[i+1] == "o":
                putBrik(tokens[i+1], tokens[i+2])
                score()
            else:
                print("Unvalid piece. Place either x or o.")
        # Sætter gamemode til tic. Så disse regler gælder. 
        elif tokens[i] == "tic":
            game = "tic"
            print("Gamemode rules: tic tac toe")   # TEST PRINT?
        else:
           print("KEYWORD '" + tokens[i] + "' IS NOT ACCEPTED") # TEST PRINT

# Putter en brik på koordinatet. Bruger dictionary 'position' til at oversætte f.eks. d3 til [3][3]
def putBrik(brik,coordinat):
    col = position[coordinat[0]]
    row = int(coordinat[1])
    global board
    if (board[row][col] == " "):
        board[row][col] = brik
        print(np.matrix(board))
    else:
        print("Already a piece here!")
   
def score():
    global board;
    global boardRows;
    global boardColumns;
    # Herunder score reglerne for tic tac toe
    if (game == "tic"): 
        for i in range(1, boardRows):
            for j in range (1, boardColumns):
                if (board[i][j] == " "):
                    continue
                if j < (boardColumns-1):    #Sørger for vi ikke får "list out of index" ved kollonerne.
                    if (board[i][j-1] == board[i][j]) and (board[i][j] == board[i][j+1]):
                        print("3 på stribe vandret")
                if i < (boardRows-1):       #Sørger for at vi ikke får list out of index ved rækkerne.
                    if (board[i-1][j] == board[i][j]) and (board[i][j] == board[i+1][j]):
                        print("3 på strive lodret")
                if i < (boardRows-1) and (j < boardColumns-1):
                    if (board[i-1][j-1] == board[i][j]) and (board[i][j] == board[i+1][j+1]):
                        print("3 på strive skråt nedad")
                if i < (boardRows-1) and (j < boardColumns-1):
                    if (board[i+1][j-1] == board[i][j]) and (board[i][j] == board[i-1][j+1]):
                        print("3 på strive skråt opad")
    else:
        print("No gamemode chosen");

# 'main' funktion som kører lexeren, så parseren. Virker generelt som interpreter.
def main(tekst):
    tekstTokens = lexer(tekst)
    print(tekstTokens) # TEST PRINT
    parser(tekstTokens)
    orgTekst = input();
    main(orgTekst);
    

orgTekst = input();
main(orgTekst);
# boardSetup();