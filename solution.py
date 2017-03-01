import copy

assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'


def cross(a, b):
    return [s + t for s in a for t in b]


boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
diagonal_units = [[rows[int(i) - 1] + i for i in cols], [rows[len(cols) - int(i)] + i for i in cols]]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values):
    """
    Go through all boxes, find naked twins in each unit and purge peers from those twin values.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    for box in boxes:
        test_val = values[box]
        if len(test_val) == 2:
            for unit in units[box]:
                twin = None
                for peer in unit:
                    if values[peer] == test_val and peer != box:
                        twin = peer
                        break
                if twin is not None:
                    for peer in unit:
                        if peer != box and peer != twin:
                            for digit in test_val:
                                assign_value(values, peer, values[peer].replace(digit, ''))

    return values


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Input: A grid in string form.
    Output: A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))


def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print


def eliminate(values):
    """
    Go through all the boxes, and whenever there is a box with a value, eliminate this value from the values of all its peers.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    for box in values:
        digit = values[box]
        if len(digit) == 1:
            for peer in peers[box]:
                assign_value(values, peer, values[peer].replace(digit, ''))
    return values


def check_units(values, char, box):
    """

    Input: A sudoku in dictionary form, char to search in values of all units, origin box
    Output: True if only possible value found for at least one unit.
            False if char is found in at least one unit
    """
    for unit in units[box]:
        found = False
        for box_of_unit in unit:
            if box_of_unit != box:
                if char in values[box_of_unit]:
                    found = True
                    break

        if not found:
            assign_value(values, box, char)
            return True
    return False


def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    for box in values:
        if len(values[box]) > 1:
            for char in values[box]:
                if check_units(values, char, box):
                    break
    return values


def reduce_puzzle(values):
    """
    Iterate eliminate(), naked_twind() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        values = eliminate(values)
        values = naked_twins(values)
        values = only_choice(values)

        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def is_solved(values):
    """
    Go through all value and check if there are unsolved boxes
    Input: A sudoku in dictionary form.
    Output: True if all boxes are solved.
            False if at least one box is not solved.
    """
    for box in values:
        if len(values[box]) > 1:
            return False
    return True


def search(values):
    """
    Recursive search function. Calls reduce_puzzle() and if sudoku is not solved - branches possible solutions and
    recursively tries to solve them
    Input: A sudoku in dictionary form.
    Output: False if no solution is found
            Or solved sudoku in dictionary form.
    """
    values = reduce_puzzle(values)
    if not values:
        return False
    if is_solved(values):
        return values

    min_box_size = 10
    min_box = None
    for box in values:
        if 1 < len(values[box]) < min_box_size:
            min_box = box
            min_box_size = len(values[box])

    if min_box is None:
        return values

    for possible_solution in values[min_box]:
        cp_values = copy.copy(values)
        cp_values[min_box] = possible_solution
        cp_values = search(cp_values)
        if cp_values is not False and is_solved(cp_values):
            return cp_values

    return False


def solve(grid):
    values = grid_values(grid)
    display(values)
    print()
    return search(values)


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments

        # visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
