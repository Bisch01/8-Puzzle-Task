import copy
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
    for row in range(len(state)): # gehe Zeilen durch
        for column in range(len(state[row])): # gehe Spalten durch
            if state[row][column] == 0: #prüfe ob beides 0 ist (mit Zugriffsoperator)
                return row, column

#Moves
# Funktion erhät Board-Status und gib eine Liste von neuen möglich Status zurück
def generateMoves(state):
    possibleStates = []
    # current state of zero
    zero_row, zero_col = findPositionOfZero(state)
    # possible moves
    moves = [
        (-1, 0), #Up
        (1, 0), # Down
        (0, -1), # Left
        (0, 1) # Right
    ]

    # loop threw possible moves
    for r , c in moves:
        #calculate potential new coordinates
        new_row = zero_row + r
        new_col = zero_col + c
        # checck if coordinates are valid
        if 0 <= new_row <= 2 and 0 <= new_col <= 2:
            # if move is valid, create deep copy of current copy
            new_state = copy.deepcopy(state)
            # swap positions
            new_state[zero_row][zero_col], new_state[new_row][new_col] = new_state[new_row][new_col], new_state[zero_row][zero_col]
            # add new created board state to list of possible states
            possibleStates.append(new_state)
            # after checking all four directions return list of valid new board states
    return possibleStates







#FUNCTIONS
print_start_state()
checkIfSolveable()
findPositionOfZero(start_state)
generateMoves(start_state)

#DEBUGGING
#print(one_dimensional_list)
#print(invertation_counter)

