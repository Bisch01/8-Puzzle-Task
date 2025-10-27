import copy
import random
import statistics
import tracemalloc #memory usage tracking
import heapq  #for astar
import math  #for astar
"""
TODO
Suchalgorithmus(zb. A*) für nodes
Messdaten vergleichen (expanded nodes, computation time)
"""
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

# Manhattan Heuristic 

def findPositionInGoal(value, goal):     # Findet die Position (Zeile, Spalte) der Zahl 'value' in der Zielmatrix 'goal'.
    for row in range(3):                 # row = Zeile 0..2
        for col in range(3):             # col = Spalte 0..2
            if goal[row][col] == value:  # wenn an (row,col) genau dieser Wert steht
                return row, col          # Position zurückgeben
    return None                          # falls nichts gefunden (sollte nicht passieren)

def manhattan(state):       # Berechnet die Manhattan-Distanz.
                            # Idee: Für jede Kachel (1..8) schauen: Wo steht sie JETZT? Wo steht sie IM ZIEL?
                            # Abstand = |ΔZeile| + |ΔSpalte|
                            # Summe über alle Kacheln (0 ignorieren).

    total = 0                             # Startwert der Summe = 0

    for row in range(3):                  # row = aktuelle Zeile 0..2
        for col in range(3):              # col = aktuelle Spalte 0..2
            value = state[row][col]       # Zahl, die aktuell hier steht
            if value == 0:                # 0 = leeres Feld? (keine Kachel)
                continue                  # dann überspringen

            goal_row, goal_col = findPositionInGoal(value, goal_state)  # wo soll sie hin?
            # Abstand nur in Gitter-Schritten (oben/unten/links/rechts)
            distance = abs(row - goal_row) + abs(col - goal_col)
            total += distance              # zur Summe hinzufügen

    return total                          # am Ende: Gesamtsumme zurückgeben

# Temporärer Testausdruck
#print("Manhattan-Distanz für den Startzustand:", manhattan(start_state))

# Hamming Heuristic
def hamming(state):
    misplaced = 0

    for row in range(3):
        for col in range(3):
            current_value = state[row][col]
            # Skip the empty tile (0)
            if current_value == 0:
                continue

            # Check if the current value is in the correct position according to the goal state
            if current_value != goal_state[row][col]:
                misplaced += 1

    return misplaced

# Test the Hamming distance
#print("Hamming-Distanz für den Startzustand:", hamming(start_state))

def print_start_state():
    for row in start_state:
        print(' '.join((map(str, row))))

# check if solveable
invertation_counter = 0
one_dimensional_list = []


def checkIfSolveable(state):
    invertation_counter = 0
    one_dimensional_list = []
    for xs in state:
        for x in xs:
            if x != 0:
                one_dimensional_list.append(x) #Alle 0 entfernen

    for x in range (len(one_dimensional_list)):  # Index vorgehende Zahl
        for y in range (x + 1, len(one_dimensional_list)): # Index folgende Zahlen
            if one_dimensional_list[x] > one_dimensional_list[y]: # Check ob Wert kleiner ist
                invertation_counter = invertation_counter + 1 # Counter erhöhen

    return invertation_counter % 2 == 0
# Funktion um die Position für 0 zu ermitteln
# wird später benötigt, um die möglichen Schitte zu ermitteln
def findPositionOfZero(state):
    for row in range(len(state)): # gehe Zeilen durch
        for column in range(len(state[row])): # gehe Spalten durch
            if state[row][column] == 0: #prüfe ob beides 0 ist (mit Zugriffsoperator)
                return row, column

#Moves
# Funktion erhält Board-Status und gib eine Liste von neuen möglich Status zurück
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

#Random State Generator
def generateRandomState():
    numbers = list(range(9)) #neue Listen generieren
    random.shuffle(numbers) #liste durchmischen

    random_state = []
    #Liste wird zur 3x3 Matrix
    for i in range (0,9,3): # von 0 bis 8 in Schritten von 3
        row = [numbers[i], numbers[i+1], numbers[i+2]] # zeilen generieren
        random_state.append(row)
    return random_state

#test for 100 random states
def testHundredRandomStates():
    solvable_count = 0
    unsolvable_count = 0
    states = []
    for test in range (100):
        test_state = generateRandomState()
        states.append(test_state)
        if checkIfSolveable(test_state):
            solvable_count += 1
        else:
            unsolvable_count += 1
    print("Lösbare Zustände:", solvable_count)
    print("Unläsbare Zustände:", unsolvable_count)
    return states
def memoryUsagetest():
    tracemalloc.start() #start the memory allocation tracing, everything after this gets tracked
    testHundredRandomStates()
    generateMoves(start_state)
    findPositionOfZero(start_state)
    current, peak = tracemalloc.get_traced_memory() # uses a (current memory, peak memory) format in bytes
    print(current, peak)
    print(f"Current: {current / 1024:.2f} KiB, Peak: {peak / 1024:.2f} KiB") #formats it prettier in Kilobytes
    tracemalloc.stop() # stop the memory allocation tracing
def memoryUsageHamming():
    states = testHundredRandomStates()
    tracemalloc.start()
    for state in states:
        hamming(state)
    current , peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(current, peak)
def memoryUsageManhattan():
    states = testHundredRandomStates()
    tracemalloc.start()
    for state in states:
        manhattan(state)
    current , peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(current, peak)

def memoryUsage():
    states = testHundredRandomStates() #generate the 100 random states and declare them as states
    tracemalloc.start()
    for state in states:
        hamming(state)
    currenthamming, peakhamming = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(currenthamming, peakhamming)
    tracemalloc.start()
    for state in states:
        manhattan(state)
    currentmanhattan, peakmanhattan = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(currentmanhattan, peakmanhattan)
#FUNCTIONS
#print_start_state()
#checkIfSolveable()
#findPositionOfZero(start_state)
#generateMoves(start_state)
#testHundredRandomStates()
#memoryUsagetest()
#memoryUsageHamming()
#memoryUsageManhattan()
memoryUsage()
#DEBUGGING
#print(one_dimensional_list)
#print(invertation_counter)

