# Heuristic

from copy import deepcopy

# Initialize a matrix called puzzle to represent the initial configuration
initial = []
  
#taking input from the user for the initial configuration
#for loop for row entries
for i in range(3):
    #stores a row           
    a =[]
    #a for loop for the column entries
    for j in range(3):      
         a.append(int(input()))
    initial.append(a)

# Initialize a matrix called final to represent the final configuration
final= []
  
#taking input from the user for the final configuration
#a for loop for row entries
for i in range(3):
    #stores a row         
    b=[]
    #a for loop for column entries
    for j in range(3):     
         b.append(int(input()))
    final.append(b)

#we compare the final and initial configurations and if they come out to be equal then we print the number of steps required as 0
if (initial == final):
    print("# of steps: 0")
    exit()

#Used the inversion count invariant of the 8 piece puzzle and defined a function which returns the number of inversions in the given matrix compared to goal state
def inversions(initial, final):
    initial = [j for sub in initial for j in sub]
    final = [j for sub in final for j in sub]

    mapping = {}
    for i in range(0, 9):
        mapping[final[i]] = i

    inv_count = 0
    for i in range(0, 9):
        for j in range(i+1, 9):
            if initial[i] != 0 and initial[j] != 0 and mapping[initial[i]] > mapping[initial[j]]:
                inv_count += 1

    return inv_count

#we define a linear search function which takes its input as a 2D array and a target value and it returns to us the coordinates of the target value in the given array
def linearSearch(arr, target):
    # a for loop which traverses through all the rows
    for i in range(len(arr)):
        #a for loop which traverses through the entries of the given row
        for j in range(len(arr[i])):
            if (arr[i][j] == target):
                return [i, j]
    return [-1, -1]

#find the location of the empty space i the initial configuration given to us
initial_empty = linearSearch(initial,0)

#defining the cost function which takes as input the current puzzle configuration and the level of the configuration
def cost(puzzle, level):
    global final
    #initializing cost as 0
    c = 0
    #initializing m, the number of misplaced tiles as 0
    m = 0
    #for each elememt of the puzzle, we find its location in the final configuration
    for i in range(0, 3):
        for j in range(0, 3):
            #if not empty space
            if not puzzle[i][j] == 0:
                pos = linearSearch(final, puzzle[i][j])
                #if the tile is misplaced we increase the number of misplaced tiles
                if(pos!=[i,j]):
                        m=m+1
                #we add the absolute difference between the position of the tile in initial and final configuration to our cost
                c += (abs(pos[0]-i) + abs(pos[1]-j))
            else:
                empty = linearSearch(final,0)
                c += abs(i-empty[0]) + abs(j-empty[1])
    #we return cost as the sum of the absolute difference between the position of the tile in initial and final configuration, 
    # the number of misplaced tiles and the level of the configuration
    return c+m+level

#defining a function for priniting a 2-D matrix
def print_puzzle(puzzle):
    for i in puzzle:
        for j in i:
            print(j, end=" ")
        print()

#we initialize a list which will essentially stored all the visited configurations in a list
already = [initial]

#we define a function which will join the elements of a 2D array into a string separated by commas
def list_to_string(puzzle):
    l = [str(j) for sub in puzzle for j in sub]
    return ", ".join(l)

moves = []

def next(puzzle, pos, steps):
    global already
    global final
    #defining a list called cost which will store tuples each containing the cost of a puzzle as the first element and the puzzle itself as the second element
    costs = []

    #a dictionary which has basically the puzzles as keys and the positions of empty tile in it as values
    poss = {}
    #if the puzzle we obtain by making the move is equal to the final one given to us, we exit the code
    if (puzzle == final):
        print("The final configuration is as above")
        exit()
    #the possible new positions of the coordinates of the empty tile where pos is the position of the empty tile in the puzzle stored in a list
    possible = [[pos[0]+1, pos[1]], [pos[0], pos[1]+1],
                [pos[0]-1, pos[1]], [pos[0], pos[1]-1]]
    #for a given puzzle, finding out all the possible next configurations using a for loop traversing over the list possible defined above
    for index, i in enumerate(possible):
        if i[0] >= 0 and i[0] <= 2 and i[1] >= 0 and i[1] <= 2:
            puz = deepcopy(puzzle)
            #when we change the positions of empty tile, then we swap the puzzle given to us with this
            puz[pos[0]][pos[1]], puz[i[0]][i[1]] = puz[i[0]][i[1]], puz[pos[0]][pos[1]]
            #if the obtained configuration is not in the list already then we add it to the list already and the list cost, poss as shown below
            if (puz not in already):
                already.append(puz)
                costs.append((cost(puz,steps), puz))
                poss[list_to_string(puz)] = i
    if (len(costs) == 0):
        print("solvable but in more than 50 steps")
        exit()
    #we print the puzzle among the all obtained configurations at this level that has the minimum cost according to the function defined above and then call next function again on it, till we find our final configuration
    currMin = costs[0][0]
    currPuz = costs[0][1]
    for i in costs:
        if (currMin > i[0]):
            currPuz = i[1]
            currMin = i[0]
    moves.append(puzzle)
    print_puzzle(currPuz)
    print()
    next(currPuz, poss[list_to_string(currPuz)],steps+1)
    if len(moves) <= 50:
        for move in moves:
            print_puzzle(move)
    else:
        print("solvable but in more than 50 steps")
        exit()

#checking if the puzzle is solvable or not
x=inversions(initial,final);
if(x%2==1):
    print("puzzle given to us is not solvable")

elif(x%2==0):
#printing the intial configuartion and calling next function on it
    print_puzzle(initial)
    print()
    next(initial, initial_empty,0)