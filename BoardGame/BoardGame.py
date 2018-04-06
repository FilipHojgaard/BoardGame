import numpy as np

# Dictionary der definere positioner for bogstaver. Starter ved 1 fordi plads 0 bliver brugt af pladens tal visere.
position = {"a" : 1, "b" : 2, "c" : 3, "d" : 4, "e" : 5, "f" : 6, "g" : 7, "h" : 8, "i" : 9, "j" : 10, "k" : 11, "l" : 12, "m" : 13, "n" : 14};
print(position);

global board;

# Funktion som opsætter spillebrættet med de ønskede dimensioner, og sætter bogstaver øverst og tal på siden.
def boardSetup(boardRows, boardColumns):
    # boardRows = int(input("Rows of the board: "))+1
    # boardColumns = int(input("Columns of the board: "))+1
    boardRows += 1
    boardColumns += 1
    global board
    board = [[0 for x in range(boardColumns)] for y in range(boardRows)]
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
            putBrik(tokens[i+1], tokens[i+2])
        else:
           print("KEYWORD '" + tokens[i] + "' IS NOT ACCEPTED") # TEST PRINT

# Putter en brik på koordinatet. Bruger dictionary 'position' til at oversætte f.eks. d3 til [3][3]
def putBrik(brik,coordinat):
    col = position[coordinat[0]]
    row = int(coordinat[1])
    global board
    board[row][col] = brik
    print(np.matrix(board))
    
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