import copy
import time
import random
import statistics
import tracemalloc #memory usage tracking
import heapq  #for astar
import math  #for astar
from itertools import count

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
def generateRandomStates(count):
    states = []
    for _ in range(count):
        numbers = list(range(9)) #neue Listen generieren
        random.shuffle(numbers) #liste durchmischen
        random_state = []
        #Liste wird zur 3x3 Matrix
        for i in range (0,9,3): # von 0 bis 8 in Schritten von 3
            row = [numbers[i], numbers[i+1], numbers[i+2]] # zeilen generieren
            random_state.append(row)
        states.append(random_state)
    return states
#test for 100 random states
def testHundredRandomStates():
    states = generateRandomStates(100)
    solvable_count = 0
    unsolvable_count = 0
    for state in states:
        if checkIfSolveable(state):
            solvable_count += 1
        else:
            unsolvable_count += 1
    print("Lösbare Zustände:", solvable_count)
    print("Unläsbare Zustände:", unsolvable_count)
    return states

class Node:

    def __init__(self, state, parent=None, g=0, h=0):
        self.state = state
        self.parent = parent
        self.g = g
        self.h = h
        self.f = g + h

    def __lt__(self, other):
        # Vergleichsfunktion für die Prioritätswarteschlange (heapq)
        return self.f < other.f

    def __eq__(self, other):
        # Vergleichsfunktion, um Zustände im 'set' zu prüfen
        return self.state == other.state

    def __hash__(self):
        # Erzeugt einen Hash-Wert für den Zustand (Listen sind nicht hashbar)
        return hash(tuple(map(tuple, self.state)))

def reconstruct_path(node):

    #Verfolgt den Pfad vom Zielknoten rückwärts bis zum Startknoten.

    path = []
    current = node
    while current is not None:
        path.append(current.state)
        current = current.parent
    return path[::-1] # Pfad umdrehen (Start -> Ziel)


def solve_puzzle(start_state, goal_state, heuristic_function):


    start_time = time.perf_counter()  # Zeitmessung starten
    nodes_expanded = 0  # Zähler für Speicheraufwand

    # Startknoten initialisieren
    start_h = heuristic_function(start_state)
    start_node = Node(state=start_state, parent=None, g=0, h=start_h)

    # Open List (Prioritätswarteschlange) und Closed List (Set)
    open_list = []
    heapq.heappush(open_list, start_node)

    closed_set = set()

    #Haupt-Schleife des A*-Algorithmus
    while open_list:

        # Den besten Knoten (den mit dem kleinsten f-Wert) holen
        current_node = heapq.heappop(open_list)

        # Diesen Knoten als "expandiert" zählen
        nodes_expanded += 1

        # Ziel erreicht?
        if current_node.state == goal_state:
            end_time = time.perf_counter()
            path = reconstruct_path(current_node)  # Nutzt die Funktion deines Kollegen
            return (path, nodes_expanded, end_time - start_time)

        # Knoten zur Closed List hinzufügen
        closed_set.add(current_node)

        # Alle Nachbarn generieren (nutzt deine generateMoves)
        for neighbor_state in generateMoves(current_node.state):

            neighbor_g = current_node.g + 1  # Kosten sind 1 Zug mehr
            neighbor_h = heuristic_function(neighbor_state)

            neighbor_node = Node(
                state=neighbor_state,
                parent=current_node,
                g=neighbor_g,
                h=neighbor_h
            )

            # Nachbarn überspringen, wenn er schon in der Closed List ist
            if neighbor_node in closed_set:
                continue

            # Prüfen, ob der Nachbar in der Open List ist
            heapq.heappush(open_list, neighbor_node)

    # Schleife beendet, ohne das Ziel zu finden
    end_time = time.perf_counter()
    return (None, nodes_expanded, end_time - start_time)


def run_experiments(count=15):
    solvable_states = generateSolvableStates(count)
    #solvable_states = [s for s in states if checkIfSolveable(s)] #list comprehension syntax for loop mit einem if
    print(f"{len(solvable_states)}/{count} sind lösbar")
    #Listen für die Messdaten anlegen
    hamming_times = []
    hamming_nodes = []
    manhattan_times = []
    manhattan_nodes = []

    #Haupt-Schleife über alle 100 Zustände
    for i, state in enumerate(solvable_states):
        print(f"Test {i + 1}/{len(solvable_states)}...", end=" ")
        path_h, nodes_h, time_h = solve_puzzle(state, goal_state, hamming)
        hamming_times.append(time_h)
        hamming_nodes.append(nodes_h)
        print(f"Hamming: {nodes_h} Knoten, {time_h:.4f}s")

        # Lauf 2: Manhattan
        path_m, nodes_m, time_m = solve_puzzle(state, goal_state, manhattan)
        manhattan_times.append(time_m)
        manhattan_nodes.append(nodes_m)
        print(f"Manhattan: {nodes_m} Knoten, {time_m:.4f}s")


    print(f"\nAlle {count} Experimente abgeschlossen.")

    #Statistik berechnen und ausgeben (VEREINFACHTE VERSION)

    print("FINALE ERGEBNISSE (Mittelwert & Standardabweichung)")


    # Hamming
    mean_time_h = statistics.mean(hamming_times)
    stdev_time_h = statistics.stdev(hamming_times)
    mean_nodes_h = statistics.mean(hamming_nodes)
    stdev_nodes_h = statistics.stdev(hamming_nodes)

    # Manhattan
    mean_time_m = statistics.mean(manhattan_times)
    stdev_time_m = statistics.stdev(manhattan_times)
    mean_nodes_m = statistics.mean(manhattan_nodes)
    stdev_nodes_m = statistics.stdev(manhattan_nodes)

    # Einfache Ausgabe der Statistik
    print("\n--- Hamming-Distanz ---")
    print(f"Laufzeit - Mittelwert: {mean_time_h:.4f}s")
    print(f"Laufzeit - Standardabw.: {stdev_time_h:.4f}s")
    print(f"Expandierte Knoten - Mittelwert: {mean_nodes_h:.2f}")
    print(f"Expandierte Knoten - Standardabw.: {stdev_nodes_h:.2f}")

    print("\n--- Manhattan-Distanz ---")
    print(f"Laufzeit - Mittelwert: {mean_time_m:.4f}s")
    print(f"Laufzeit - Standardabw.: {stdev_time_m:.4f}s")
    print(f"Expandierte Knoten - Mittelwert: {mean_nodes_m:.2f}")
    print(f"Expandierte Knoten - Standardabw.: {stdev_nodes_m:.2f}")

def generateSolvableStates(count):
    #erstellt lösbare Zustände mit dem count parameter (z.B. 100)
    solvable_states = []
    print(f"Generiere {count} lösbare Zufallszustände...")
    while len(solvable_states) < count:
        state_list = generateRandomStates(1)
        state = state_list[0]
        if checkIfSolveable(state):
            solvable_states.append(state)
        if len(solvable_states) % 10 == 0 and len(solvable_states) > 0:
            print(f"... {len(solvable_states)} Zustände gefunden.")
    print(f"{count} lösbare Zustände generiert.\n")
    return solvable_states


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
#memoryUsage()
run_experiments(100)
#DEBUGGING
#print(one_dimensional_list)
#print(invertation_counter)

