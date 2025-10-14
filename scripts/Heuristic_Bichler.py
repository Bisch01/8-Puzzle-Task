
#declare start-state

start_state = [
    [7, 2, 4],
    [5, 0, 6],
    [8, 3, 1]
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

goal_state = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8]
]









print_start_state()
checkIfSolveable()

# debugging
print(one_dimensional_list)
print(invertation_counter)
