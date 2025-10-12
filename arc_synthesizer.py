testGrid = [[0, 2, 0], [0, 0, 0], [0, 0, 0]]

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
            grid = [[grid[len(grid)-1-j][i] for j in range(len(grid))]
            for i in range(len(grid[0]))]
        # TODO: Implement 180 and 270 degree rotations

    elif program.op == "Scale2x2":
        # TODO: Implement 2x2 scaling
        pass
    elif program.op == "Scale3x3":
        # TODO: Implement 3x3 scaling
        pass
    # TODO: Implement other operations (Scale2x1, Scale1x2, PositionalShift,etc.)

    elif program.op == "Sequence":
     # Apply left program first, then right program
        grid = apply_program(grid, program.left)
        grid = apply_program(grid, program.right)
    return grid

#Grid Displaying
def grid_display(grid):
    for i in grid:
        print("|")
        for j in i:
            print(j, end=" ")


grid_display(testGrid)