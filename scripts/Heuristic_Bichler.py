
#declare start-state

start_state = [
    [7, 2, 4],
    [5, 0, 6],
    [8, 3, 1]
]

# declare goal-state
goal_state = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8]
]

def print_start_state():
    for row in start_state:
        print(' '.join((map(str, row))))

# check if solveable
invertation_counter = 0
one_dimensional_list = []
coordinates = []

def checkIfSolveable():
    global invertation_counter
    global one_dimensional_list
    for xs in start_state:
        for x in xs:
            if x != 0:
                one_dimensional_list.append(x) #Alle 0 entfernen

    for x in range (len(one_dimensional_list)):  # Index vorgehende Zahl
        for y in range (x + 1, len(one_dimensional_list)): # Index folgende Zahlen
            if one_dimensional_list[x] > one_dimensional_list[y]: # Check ob Wert kleiner ist
                invertation_counter = invertation_counter + 1 # Counter erhöhen


# Funktion um die Position für 0 zu ermitteln
# wird später benötigt, um die möglichen Schitte zu ermitteln
def findPositionOfZero(state):
    global coordinates
    for row in range(len(state)): # gehe Zeilen durch
        for column in range(len(state[row])): # gehe Spalten durch
            if state[row][column] == 0: #prüfe ob beides 0 ist (mit Zugriffsoperator)
                coordinates.append(row)
                coordinates.append(column)
                print("Coordinates: ", coordinates)
                zero_row = coordinates[0]
                zero_column = coordinates[1]
                print("zero row: ", zero_row, " zero column: ", zero_column)
                return zero_row, zero_column

#Moves
def generateMoves(state):
    findPositionOfZero(state)
    zero_row, zero_column = findPositionOfZero(state)
    move_up = [zero_row - 1, zero_column]
    move_down = [zero_row + 1, zero_column]
    move_right = [zero_row, zero_column + 1]
    move_left = [zero_row, zero_column - 1]
    valid_moves = [move_up, move_down, move_right, move_left]
    return valid_moves

#TODO
def proofValidMoves(state):
    generateMoves(state)
    valid_moves = generateMoves(state)

    for move in valid_moves:
        if valid_moves[move] < [2, 2] and valid_moves > [0, 0]:




#FUNCTIONS
print_start_state()
checkIfSolveable()
findPositionOfZero(start_state)
generateMoves(start_state)

#DEBUGGING
#print(one_dimensional_list)
#print(invertation_counter)

