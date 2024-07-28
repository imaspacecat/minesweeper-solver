import sympy as sp

# FLAG = -1
# UNCOVERED = <=-2
number_of_flags = 0

# EASY MINES: 10
# MEDIUM MINES: 40
# HARD MINES: 99
number_of_mines = 5


def clear_flags(gameboard):
    global number_of_flags
    number_of_flags = 0
    for i in range(len(gameboard)):
        for j in range(len(gameboard[0])):
            if gameboard[i][j] == -1:
                number_of_flags += 1
                for coords in valid_adjacent(i, j, len(gameboard) - 1, len(gameboard[0]) - 1):
                    if gameboard[coords[0]][coords[1]] > 0:
                        gameboard[coords[0]][coords[1]] -= 1


# this function is unnecessary, there should be a column in the matrix for every single unrevealed tile
def number_of_potential_tiles(gameboard):
    total_tiles = 0
    valid_tiles = 0
    for i in range(len(gameboard)):
        for j in range(len(gameboard[0])):
            if gameboard[i][j] < -1:
                total_tiles += 1
                for coord in valid_adjacent(i, j, len(gameboard) - 1, len(gameboard[0]) - 1):
                    if gameboard[coord[0]][coord[1]] > 0:
                        valid_tiles += 1
                        break
    return total_tiles, valid_tiles


# optimization: use bfs to traverse the gameboard, separate different clumps of uncovered squares into separate matrices
def create_matrix(gameboard):
    total_tiles, row_length = number_of_potential_tiles(gameboard)
    mat = []
    tile_locations = {}

    mat.append([1] * total_tiles + [number_of_mines - number_of_flags])

    for i in range(len(gameboard)):
        for j in range(len(gameboard[0])):
            if gameboard[i][j] > 0:
                mat.append(mat_row(i, j, gameboard, tile_locations, total_tiles))
    return mat, tile_locations


def mat_row(x, y, gameboard, tile_locations, length):
    row = [0] * length
    row.append(gameboard[x][y])
    for coord in valid_adjacent(x, y, len(gameboard) - 1, len(gameboard[0]) - 1):
        if gameboard[coord[0]][coord[1]] < -1:
            if coord not in tile_locations:
                tile_locations[coord] = len(tile_locations)
            row[tile_locations[coord]] = 1
    return row


def valid_adjacent(x, y, x_boundary, y_boundary):
    valid_positions = []
    if x > 0: valid_positions.append((x - 1, y))
    if y > 0: valid_positions.append((x, y - 1))
    if x > 0 and y > 0: valid_positions.append((x - 1, y - 1))
    if y < y_boundary: valid_positions.append((x, y + 1))
    if x < x_boundary: valid_positions.append((x + 1, y))
    if x > 0 and y < y_boundary: valid_positions.append((x - 1, y + 1))
    if x < x_boundary and y > 0: valid_positions.append((x + 1, y - 1))
    if x < x_boundary and y < y_boundary: valid_positions.append((x + 1, y + 1))
    return valid_positions


def find_mines(mat, tile_locations):
    mine_locations = []
    confirmed_tiles = [False] * len(tile_locations)
    tile_locations = list(tile_locations)

    m = sp.Matrix(mat)
    m_rref, pivots = m.rref()
    m_rref = m_rref.tolist()

    for row in m_rref:
        *tiles, number = row
        if tiles.count(1) == number:
            for i in range(len(tiles)):
                if tiles[i] == 1:
                    confirmed_tiles[i] = True
        if tiles.count(-1) == -number:
            for i in range(len(tiles)):
                if tiles[i] == -1:
                    confirmed_tiles[i] = True

    for i in range(len(confirmed_tiles)):
        if confirmed_tiles[i]:
            mine_locations.append(tile_locations[i])

    return mine_locations


def find_safe_tiles(mine_locations, gameboard):
    safe_numbers = []
    safe_tiles = []
    for mine in mine_locations:
        for coords in valid_adjacent(mine[0], mine[1], len(gameboard) - 1, len(gameboard[0]) - 1):
            if gameboard[coords[0]][coords[1]] > 0:
                gameboard[coords[0]][coords[1]] -= 1
                if gameboard[coords[0]][coords[1]] == 0:
                    safe_numbers.append(coords)

    for mine in mine_locations:
        gameboard[mine[0]][mine[1]] = -1

    for number in safe_numbers:
        for coords in valid_adjacent(number[0], number[1], len(gameboard) - 1, len(gameboard[0]) - 1):
            if gameboard[coords[0]][coords[1]] < -1:
                gameboard[coords[0]][coords[1]] = 0
                safe_tiles.append(coords)
    return list(set(safe_tiles))



# TESTING!!!
board = [[ 0,  0,  0,  0,  1, -2, -2, -2, -2, -2],
         [ 1,  1,  0,  0,  1,  1,  1, -2, -2, -2],
         [-1,  2,  1,  0,  0,  0,  1, -2, -2, -2],
         [ 2, -1,  1,  0,  0,  1,  2, -2, -2, -2],
         [ 1,  1,  1,  0,  0,  1, -2, -2, -2, -2],
         [ 0,  0,  0,  0,  0,  1,  1,  1,  3, -2],
         [ 0,  0,  0,  0,  0,  0,  0,  0,  2, -2],
         [ 0,  0,  0,  0,  0,  0,  0,  0,  1, -2]]
# mines: (0, 5), (3, 7), (4, 6), (4, 9), (5, 9), (6, 9)

clear_flags(board)
matrix, loc = create_matrix(board)
m_loc = find_mines(matrix, loc)
print("mines: " + str(m_loc))
print("safe: " + str(find_safe_tiles(m_loc, board)))
matrix, loc = create_matrix(board)
m_loc = find_mines(matrix, loc)
print("mines: " + str(m_loc))
print("safe: " + str(find_safe_tiles(m_loc, board)))