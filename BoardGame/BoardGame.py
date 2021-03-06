import numpy as np

# Eksempel på kørsel:
# new 3 3 tic put O b2
# laver nyt bræt som er 3x3, bruger spilleregler for tic tac toe og forsøger at putte en bolle på b2.

# Dictionary der definere positioner for bogstaver. Starter ved 1 fordi plads 0 bliver brugt af pladens tal visere.
position = {"a" : 1, "b" : 2, "c" : 3, "d" : 4, "e" : 5, "f" : 6, "g" : 7, "h" : 8, "i" : 9, "j" : 10, "k" : 11, "l" : 12, "m" : 13, "n" : 14, "o" : 14, "p" : 14, "q" : 14,
            "r" : 14, "s" : 14, "t" : 14, "u" : 14, "v" : 14, "w" : 14, "x" : 14, "y" : 14};
# print(position);

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
    letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y',]

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
            if (tokens[i+1].isdigit()) and (tokens[i+2].isdigit()):
                argRow = int(tokens[i+1])
                argCol = int(tokens[i+2])
                if argRow < 26 and argCol < 26 and argRow >= 0 and argCol >= 0:
                    boardSetup(argRow, argCol)     # kalder funktionen 'boardSetup' som laver et bræt ud fra 2 argumenter. F.eks. 'new 5 7' laver 5x7 bræt.
                    print() # springer en linje for læse venlighed
                else:
                    print("Error: new function expects integers between 0 and 25")
            else:
                print("Error: new function expects 2 integers as arguments")
        # put Z a1, putter et 'Z' på plads a1.
        elif tokens[i] == "put":
            if tokens[i+1] == "x" or tokens[i+1] == "o":
                if len(tokens[i+2]) == 2 and tokens[i+2][1].isdigit() and not(tokens[i+2][0].isdigit()):
                    if tokens[i+1] == "x" or tokens[i+1] == "o":
                        putBrik(tokens[i+1], tokens[i+2])
                        score()
                    else:
                        print("Unvalid piece. Place either x or o.")
                else:
                    print("Error: put function expects coordinate set as second argument. E.g a1")
            else:
                print("Error: put function expects 'o' or 'x' as first argument")
        # Sætter gamemode til tic. Så disse regler gælder. 
        elif tokens[i] == "tic":
            game = "tic"
            print("Gamemode rules: tic tac toe")   # TEST PRINT?
        elif tokens[i] == "five":
            game = "five";
            print("Gamemode rules: Gomuko/Five-In-a-Row")
        elif tokens[i] == "go":
            game = "go";
            print("Gamemode rules: Go")
        elif tokens[i] == "mode":
            print("Gamemode set to: " + game);
        elif tokens[i] == "exit":
            exit()
        #else:
         #  print("KEYWORD '" + tokens[i] + "' IS NOT ACCEPTED") # TEST PRINT

# Putter en brik på koordinatet. Bruger dictionary 'position' til at oversætte f.eks. d3 til [3][3]
def putBrik(brik,coordinat):
    global boardRows;
    global boardColumns;
    global board;
    global game;
    col = position[coordinat[0]]
    row = int(coordinat[1])
    if (board[row][col] == " "):
        board[row][col] = brik
    else:
        print("Already a piece here!")
    if (game == "go"):
        for i in range(1, boardRows):
            for j in range(1, boardColumns):
                if (j < boardColumns-1) and (i < boardRows-1):
                    if (board[i][j-1] == board[i][j+1]) and (board[i][j-1] == board[i-1][j]) and (board[i-1][j] == board[i+1][j]) and (board[i][j-1] != " "):
                        if board[i][j] != " " and (board[i][j] != board[i][j-1]):
                            board[i][j] = board[i][j-1]
    print(np.matrix(board))
   
def score():
    global board;
    global boardRows;
    global boardColumns;
    global game;
    # Herunder score reglerne for tic tac toe
    if (game == "tic"): 
        for i in range(1, boardRows):
            for j in range (1, boardColumns):
                if (board[i][j] == " "):
                    continue
                if j < (boardColumns-1):    #Sørger for vi ikke får "list out of index" ved kollonerne.
                    if (board[i][j-1] == board[i][j]) and (board[i][j] == board[i][j+1]):
                        if board[i][j] == "o":
                            print("0 2")
                        else:
                            print("2 0")
                if i < (boardRows-1):       #Sørger for at vi ikke får list out of index ved rækkerne.
                    if (board[i-1][j] == board[i][j]) and (board[i][j] == board[i+1][j]):
                        if board[i][j] == "o":
                            print("0 2")
                        else:
                            print("2 0")
                if i < (boardRows-1) and (j < boardColumns-1):
                    if (board[i-1][j-1] == board[i][j]) and (board[i][j] == board[i+1][j+1]):
                        if board[i][j] == "o":
                            print("0 2")
                        else:
                            print("2 0")
                if i < (boardRows-1) and (j < boardColumns-1):
                    if (board[i+1][j-1] == board[i][j]) and (board[i][j] == board[i-1][j+1]):
                        if board[i][j] == "o":
                            print("0 2")
                        else:
                            print("2 0")
    elif (game == "five"):      # 5 på stribe
        for i in range(1, boardRows):
            for j in range (1, boardColumns):
                if (board[i][j] == " "):
                    continue
                if j < (boardColumns-2):    #Sørger for vi ikke får "list out of index" ved kollonerne.
                    if (board[i][j-2] == board[i][j]) and (board[i][j-1] == board[i][j]) and (board[i][j] == board[i][j+1]) and (board[i][j+2] == board[i][j]):
                        if board[i][j] == "o":
                            print("0 2")
                        else:
                            print("2 0")
                if i < (boardRows-2):       #Sørger for at vi ikke får list out of index ved rækkerne.
                    if (board[i-2][j] == board[i][j]) and (board[i-1][j] == board[i][j]) and (board[i][j] == board[i+1][j]) and (board[i+2][j] == board[i][j]):
                        if board[i][j] == "o":
                            print("0 2")
                        else:
                            print("2 0")
                if i < (boardRows-2) and (j < boardColumns-2):
                    if (board[i-2][j-2] == board[i][j]) and (board[i-1][j-1] == board[i][j]) and (board[i][j] == board[i+1][j+1]) and (board[i][j] == board[i+2][j+2]):
                        if board[i][j] == "o":
                            print("0 2")
                        else:
                            print("2 0")
                if i < (boardRows-2) and (j < boardColumns-2):
                    if (board[i+2][j-2] == board[i][j]) and (board[i+1][j-1] == board[i][j]) and (board[i][j] == board[i-1][j+1]) and (board[i][j] == board[i-2][j+2]):
                        if board[i][j] == "o":
                            print("0 2")
                        else:
                            print("2 0")
    elif (game == "go"):
        black = 0;
        white = 0;
        for i in range(1, boardRows):
            for j in range(1, boardColumns):
                if board[i][j] == "x":
                    black += 1;
                elif board[i][j] == "o":
                    white += 1;
        if (black > white):
            print("2 0")
        elif (white > black):
            print("0 2")
        elif (white == black):
            print("0 0")
    else:
        print("No gamemode chosen");

# 'main' funktion som kører lexeren, så parseren. Virker generelt som interpreter.
def main(tekst):
    tekstTokens = lexer(tekst)
 #   print(tekstTokens) # TEST PRINT
    parser(tekstTokens)
    orgTekst = input();
    main(orgTekst);
    
def play(tekst):
    tokens = lexer(tekst)
    parser(tokens)

orgTekst = input();
main(orgTekst);
# boardSetup();