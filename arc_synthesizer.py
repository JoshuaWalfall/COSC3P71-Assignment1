import Program
from collections import deque
import itertools

#testF = open("test_output.txt", "w")

def apply_program(input_grid, program):
    """Apply a program to an input grid and return the output grid."""
    if program is None:
        return None

    grid = [row[:] for row in input_grid] # Deep copy

    if program.op == "ColorChange":
        old_color, new_color = program.right
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] == old_color:
                    grid[i][j] = new_color

    elif program.op == "Mirror":
        axis = program.right
        if axis == "horizontal":
            grid = grid[::-1] # Flip vertically
        elif axis == "vertical":
            grid = [row[::-1] for row in grid] # Flip horizontally

    elif program.op == "Rotate":
        degrees = program.right
        if degrees == 90:
            grid = [[grid[len(grid)-1-j][i] for j in range(len(grid))] for i in range(len(grid[0]))]
        # TODO: Implement 180 and 270 degree rotations
        elif degrees == 180:
            grid = [row[::-1] for row in grid[::-1]]
        elif degrees == 270:
            grid = [[grid[j][len(grid)-1-i] for j in range(len(grid))] for i in range(len(grid[0]))]

    elif program.op == "Scale2x2":
        # TODO: Implement 2x2 scaling
        # pass
        new_grid = []
        for row in grid:
            new_row1 = []
            new_row2 = []
            for item in row:
                new_row1.extend([item, item])
                new_row2.extend([item, item])
            new_grid.append(new_row1)
            new_grid.append(new_row2)
        grid = new_grid
    elif program.op == "Scale3x3":
        # TODO: Implement 3x3 scaling
        #pass
        new_grid = []
        for row in grid:
            new_row1 = []
            new_row2 = []
            new_row3 = []
            for item in row:
                new_row1.extend([item, item, item])
                new_row2.extend([item, item, item])
                new_row3.extend([item, item, item])
            new_grid.append(new_row1)
            new_grid.append(new_row2)
            new_grid.append(new_row3)
        grid = new_grid
    # TODO: Implement other operations (Scale2x1, Scale1x2, PositionalShift,etc.)
    elif program.op == "Scale2x1":
        #Horizontal Scaling by 2
        new_grid = []
        for row in grid:
            new_row = []
            for item in row:
                new_row.append(item)
                new_row.append(item)
            new_grid.append(new_row)
        grid = new_grid
    elif program.op == "Scale1x2":
        #Vertical Scaling by 2
        new_grid = []
        for row in grid:
            new_row = []
            for item in row:
                new_row.append(item)
            new_grid.append(new_row)
            new_grid.append(new_row[:]) 
        grid = new_grid
    elif program.op == "ResizeIrregular":
        #Resizes the new grid by scaling it's scaling up the existing content to fix the new dimeinsions
        new_grid = []
        w = program.right[0]
        h = program.right[1]
        for i in range (h):
            new_row = []
            for j in range (w):
                old_i = i * len(grid) // h
                old_j = j * len(grid[0]) // w
                new_row.append(grid[old_i][old_j])
            new_grid.append(new_row)
        grid = new_grid

    elif program.op == "PositionalShift":
        old_color = program.right[0]
        new_color = program.right[1]
        dr = program.right[2] # row shift
        dc = program.right[3] # column shift

        new_grid = [row[:] for row in grid]
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == old_color:
                    new_grid[i][j] = 0
                    new_r = i + dr
                    new_c = j + dc
                    if 0 <= new_r < len(grid) and 0 <= new_c < len(grid[0]):
                        new_grid[new_r][new_c] = new_color
                    
        grid = new_grid
    
    elif program.op == "ColorMapMultiple":
        color_map = program.right
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] in color_map:
                    grid[i][j] = color_map[grid[i][j]]

    elif program.op == "ScaleWithColorMap":
        s = program.right[0]
        color_map = program.right[1]
        new_grid = []
        for i in range(len(grid)):
            for k in range(s):
                new_row = []
                for j in range(len(grid[i])): 
                    mapped_color = grid[i][j]
                    if grid[i][j] in color_map:
                        mapped_color = color_map[grid[i][j]]
                    
                    for l in range(s):
                        new_row.append(mapped_color)
                new_grid.append(new_row)
        grid = new_grid
    elif program.op == "SwapColors":
        color1 = program.right[0]
        color2 = program.right[1]
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] == color1:
                    grid[i][j] = color2
                elif grid[i][j] == color2:
                    grid[i][j] = color1
    elif program.op == "DiagonalReflection":
        new_grid = [row[:] for row in grid]
        old_color = program.right[0]
        new_color = program.right[1]
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] == old_color:
                    new_grid[i][j] = 0
                    if j < len(grid) and i < len(grid[0]):
                        new_grid[j][i] = new_color
        grid = new_grid
                    


    elif program.op == "Sequence":
     # Apply left program first, then right program
        grid = apply_program(grid, program.left)
        grid = apply_program(grid, program.right)
    return grid

#Grid Displaying
def grid_display(grid):
    print("- " *(len(grid[0]) + 2))
    for i in grid:
        print("|", end=" ")
        for j in i:
            print(j, end=" ")
        print("|")
    print("- " *(len(grid[0]) + 2))

def testing():

    
    testGrid = [[0, 2, 0], [0, 0, 0], [0, 0, 0]]
    test2Grid = [[0, ], [0, 1]]

    testColorMap = {
        1 : 2
    }

    test = Program.Program ("DiagonalReflection", None, [1,5])

    grid_display(test2Grid)
    applied_grid = apply_program(test2Grid, test)
    grid_display(applied_grid)

def bfs_search (train_data, max_complexity):
    #Generate basic opps

    #Implement main bfs loop

    #check against training data
    #Generate new probs by sequencing
    basic_ops = generateBasics()
    counter = 0
    queue = deque(basic_ops)
    while queue:
        current_program = queue.popleft()

        #print("Testing :", current_program, file=testF)
        print("Testing: ", current_program)
        print("Complexity: ", current_program.complexity)
        
        all_match = True
        for example in train_data:
            for i in range(len(train_data[example]['train'])):
                input_grid = train_data[example]['train'][i]["input"]
                #print("Input Grid:", file=testF)
                #grid_display(input_grid)
                #print(train_data[example])
                #print(len(train_data[example]))
                expected_output = train_data[example]['train'][i]["output"]
                #print("Expected Output:", file=testF)
                #grid_display(expected_output)

                #print("Actual Output:", file=testF)
                actual_output = apply_program(input_grid, current_program)
                #grid_display(actual_output)
                if actual_output != expected_output:
                    all_match = False
                    print("Left in queue: ", len(queue))

                    break
                else:
                    print("SUCCESS====================================")#, file=testF)
            if all_match == False:
                break
        if all_match:
            return current_program
        
        for basic_op in basic_ops:
            new_program = Program.Program("Sequence", current_program, basic_op)
            if new_program.complexity <= max_complexity:
                queue.append(new_program)

    return None

def generateTestBasics():
    basic_ops = []
    basic_ops.append(Program.Program("ColorChange", None, [1,2]))
    basic_ops.append(Program.Program("Mirror", None, "horizontal"))
    basic_ops.append(Program.Program("Rotate", None, 90))
    basic_ops.append(Program.Program("Scale2x2", None, None))
    return basic_ops

def generateBasics ():
    #Color Changes
    basic_ops = []
    for i in range (10):
        for j in range (10):
            if i != j:
                basic_ops.append(Program.Program("ColorChange", None, [i,j]))
    
    #Mirror
    basic_ops.append(Program.Program("Mirror", None, "horizontal"))
    basic_ops.append(Program.Program("Mirror", None, "vertical"))
    
    #Rotate
    basic_ops.append(Program.Program("Rotate", None, 90))
    basic_ops.append(Program.Program("Rotate", None, 180))
    basic_ops.append(Program.Program("Rotate", None, 270))

    #Scaling
    basic_ops.append(Program.Program("Scale2x2", None, None))
    basic_ops.append(Program.Program("Scale3x3", None, None))
    basic_ops.append(Program.Program("Scale2x1", None, None))
    basic_ops.append(Program.Program("Scale1x2", None, None))

    #ResizeIrregular
    for i in range (1, 11):
        for j in range (1, 11):
            basic_ops.append(Program.Program("ResizeIrregular", None, [i,j]))


    #PositionalShift
    for old_color in range (10):
        for new_color in range (10):
            if old_color != new_color:
                for dr in range (-1, 2):
                    for dc in range (-1, 2):
                        basic_ops.append(Program.Program("PositionalShift", None, [old_color, new_color, dr, dc]))
    
    #ColorMapMultiple and ScaleWithColorMap
    # Running maximally (Unrealistic)
    #f0or i in range(1, 10):
        #colors = list(range(10))
        #for combo in itertools.combinations(colors, i):
            #for perm in itertools.permutations(combo):
                #color_map = {combo[k]: perm[k] for k in range(i) if combo[k] != perm[k]}
                #if color_map:
                    #basic_ops.append(Program.Program("ColorMapMultiple", None, color_map))
                    
                    #basic_ops.append(Program.Program("ScaleWithColorMap", None, [2, {j: i}]))
                    #basic_ops.append(Program.Program("ScaleWithColorMap", None, [3, {j: i}]))

    for i in range (1, 10):
        for j in range (1, 10):
            if i != j:
                basic_ops.append(Program.Program("ColorMapMultiple", None, {j: i}))

                basic_ops.append(Program.Program("ScaleWithColorMap", None, [2, {j: i}]))
                basic_ops.append(Program.Program("ScaleWithColorMap", None, [3, {j: i}]))
    #SwapColors
    for i in range (10):
        for j in range (10):
            if i != j:
                basic_ops.append(Program.Program("SwapColors", None, [i, j]))
    #DiagonalReflection
    for i in range (10):
        for j in range (10):
            if i != j:
                basic_ops.append(Program.Program("DiagonalReflection", None, [i, j]))

    return basic_ops

#testing = generateBasics()
#for i in range(len(testing)):
    #print(testing[i])
