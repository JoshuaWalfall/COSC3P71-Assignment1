import Program
from collections import deque
import itertools
import heapq
import pickle
import json

safety_limit = 50000000

def apply_program(input_grid, program):
    """Apply a program to an input grid and return the output grid."""
    if program is None:
        return None

    grid = [row[:] for row in input_grid] # Deep copy
    #grid_display(grid)

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
            grid = [[grid[j][len(grid[0])-1-i] for j in range(len(grid))] for i in range(len(grid[0]))]

    elif program.op == "Scale2x2":
        # TODO: Implement 2x2 scaling
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


def bfs_search (train_data, max_complexity):
    """Breadth-First Search for program synthesis."""
    basic_ops = generateBasics()
    queue = deque(basic_ops)

    toQueue = deque()
    while queue:
        
        current_program = queue.popleft()

        #print("Testing: ", current_program)
        #print("Complexity: ", current_program.complexity)
        
        all_match = True
        for example in train_data:
            
            input_grid = example["input"]
            expected_output = example["output"]
                
            actual_output = apply_program(input_grid, current_program)
                
            if actual_output != expected_output:
                all_match = False
                
                break
            
        if all_match:
            #print("Solution Found: ", current_program)
            return current_program
        
        if (current_program.complexity < max_complexity):
            toQueue.append(current_program) #Right side

        if len(queue) < safety_limit and len(toQueue) > 0:
            toAdd = toQueue.popleft() # Oldest program in toQueue which hasn't created new programs yet
            
            if toAdd:
                if (isinstance(toAdd, int)):
                    cacheLoad = open("cache/cache_"+str(toAdd), 'rb')
                    cacheData = pickle.load(cacheLoad)
                    toQueue.extendleft(cacheData)
                    cacheLoad.close
                    print("Loaded cache_", toAdd, " | Queue Remaining: ", len(queue), " | Queue Pending: ", len(toQueue))
                else:    
                    for basic_op in basic_ops:
                        new_program = Program.Program("Sequence", toAdd, basic_op)
                        if new_program.complexity <= max_complexity:
                            queue.append(new_program)
        if len(toQueue) > safety_limit:
            cache = QueueCache()
            for i in range(int(safety_limit/2)):
                cache.list.append(toQueue.pop) #Pop SPECIFICALLY the youngest programs first (Right side)
            toQueue.append(cache.number)
            print("Loaded to cache_", cache.number, " | Queue Remaining: ", len(queue), " | Queue Pending: ", len(toQueue), " | Current Complexity: ", queue[0].complexity)
            cacheSave = open(cache.name, 'ab')
            pickle.dump(cache, cacheSave)
            cacheSave.close       

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



def mismatched_cells (program, input_grid, expected_output):
    actual_output = apply_program(input_grid, program)
    mismatched_cells = 0
    h = max(len(expected_output), len(actual_output))
    w = max(len(expected_output[0]), len(actual_output[0]))
    for i in range(h):
        for j in range(w):
            if (i > (len(actual_output) -1) or i > (len(expected_output) -1)):
                mismatched_cells += 1
            else:
                #print("here")
                if (j > (len(actual_output[0]) -1) or j > (len(expected_output[0]) -1)):
                    mismatched_cells += 1
                else:
                    #print(actual_output[i][j] != expected_output[i][j])
                    if actual_output[i][j] != expected_output[i][j]:
                        mismatched_cells += 1
    #print("Mismatched Cells:", mismatched_cells)
    return mismatched_cells

#mismatched_cells(Program.Program("Rotate", None, 180), [[1, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 2], [0, 0, 0], [0, 0, 0]])

def heuristic_custom1 (program, input_grid, output_grid):
    actual_output = apply_program(input_grid, program)
    dimension_weight = abs(len(actual_output) - len(output_grid)) + abs(len(actual_output) - len(output_grid))
    #print(dimension_weight)
    color_weight = 0
    for i in range(10):
        if i in itertools.chain(*output_grid) != i in itertools.chain(*actual_output):
            color_weight =+ 1
    return color_weight + 2*dimension_weight
            

def gbfs_search (train_data, max_complexity, heuristic):
    """Greedy Best-First Search for program synthesis using the provided heuristic function."""
    basic_ops = generateBasics()
    
    queue = [HeapWrapper(op, 0) for op in basic_ops] 
    heapq.heapify(queue)
    
    for x in range(max_complexity):
        #print ("Current Complexity:" ,x)
        for current in queue:
            current_program = current.program

            all_match = True
            heuristic_value = 0
            for example in train_data:
                input_grid = example["input"] 
                expected_output = example["output"]
                
                actual_output = apply_program(input_grid, current_program)
                
                if actual_output != expected_output:
                    all_match = False
                    heuristic_value =+ heuristic(current_program, input_grid, expected_output)
                    
                    break
            current.priority = heuristic_value
            if all_match:
                #print("Solution Found: ", current_program, " with priority ", current.priority)
                return current_program
        queue.sort()
        
        temp_solution = queue[0]
        
        for basic_op in basic_ops:
            new_heap = HeapWrapper(Program.Program("Sequence", temp_solution.program, basic_op), temp_solution.priority)
            
            heapq.heappush(queue, new_heap)
        
    return None

def a_star_search (train_data, max_complexity, heuristic):
    """A* search for prgoram syntheisis using the provided heuristic function."""
    basic_ops = generateBasics()
    
    queue = [HeapWrapper(op, 0) for op in basic_ops] 
    heapq.heapify(queue)
    
    for x in range(max_complexity):
        
        for current in queue:
            current_program = current.program

           
            all_match = True
            base_value = current_program.complexity
            for example in train_data:
                input_grid = example["input"] 
                expected_output = example["output"]
                
                actual_output = apply_program(input_grid, current_program)
                
                if actual_output != expected_output:
                    all_match = False
                    base_value =+ heuristic(current_program, input_grid, expected_output)
                    
                    break
            current.priority = base_value
            if all_match:
                #print("Solution Found: ", current_program, " with priority ", current.priority)
                return current_program
        queue.sort()
        
        temp_solution = queue[0]

        for basic_op in basic_ops:
            new_heap = HeapWrapper(Program.Program("Sequence", temp_solution.program, basic_op), temp_solution.priority)
            
            heapq.heappush(queue, new_heap)
        
      
        
    return None
#Used to solely sort programs by their heuristic value, ignoring tie breaker by complexity
class HeapWrapper:
    def __init__(self, program, priority):
        self.program = program
        self.priority = priority
    def __lt__ (self, other):
        return self.priority < other.priority
    def __str__ (self):
        return str(self.program) + " with priority " + str(self.priority)
#Custom class to store cached values during deep BFS search, to ensure that memory didn't overflow
class QueueCache:
    def __init__(self):
        cr = open("cache.json", 'r+')
        test_char = cr .read(1)
        if not test_char:
            master_cache = {"counter": 1,"list": []}
        else:
            cr.seek(0)
            master_cache = json.load(cr)
        self.number = master_cache["counter"]
        self.list = []
        cr.close()
        self.name = "cache/cache_" + str(self.number)
        #print(self.name)
        ce = open("cache.json", "w")
        master_cache["list"].append({str(self.number):self.name})
        master_cache["counter"] = master_cache["counter"] + 1
        ce.write(json.dumps(master_cache, indent=3))
        ce.close()

