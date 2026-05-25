import random
def first_try():
    #  N_rows & N_squares
    print("How many rows (1 - 5)?")
    rows = int(input())
    while rows > 5 or rows < 1:
        print("Invalid input.")
        print("How many rows (1 - 5)?")
        rows = int(input())
    squares_total  = rows * 5

    if rows == 5:
        num_x = 15
    else:
    #  Random number of X's between 1 and the smaller of 15,squares_total
    #  Prevents mores X's than squares
        num_x = random.randint(1, min(15, squares_total))
    #  Chooses (num_x) values from (squares_total)
    position = random.sample(range(squares_total), num_x)

    grid = [" "] * squares_total

    for p in position:
        grid[p] = "X"

    for r in range(rows):
    #  Converts the long list into 5 long rows for print
    #  E.g. r=2, grid[10:15] --> index 10,11,12,13,14
        row = grid[r*5 : (r+1)*5]
        print(("|" + "|".join(row) + "|"))



def second_try():
    grid = []
    for row in range(5):
        row_list = []
        for col in range(5):
            row_list.append(" ")
        grid.append(row_list)
    print(grid)
    
    for row in range(5):
        random_col = random.randint(0, 4)
        grid[row][random_col] = "X"
        print(f"Row {row}: placed X at column {random_col}")
    
    for row in range(5):
        print("|", end="")
        for col in range(5):
            print(f" {grid[row][col]} |", end="")









def third_try():
    grid = []
    for row in range(5):
        row_list = []
        for col in range(5):
            row_list.append(" ")
        grid.append(row_list)

    placed_x = 0
    while placed_x < 15:
        row = random.randint(0, 4)
        col = random.randint(0, 4)
        if grid[row][col] == " ":
            grid[row][col] = "X"
            placed_x += 1

    for row in grid:
        line = "|"
        for cell in row:
            line += " " + cell + " |"
        print(line)



def fourth_try():
    # Create empty 3x3 grid
    grid = [
    [' ', ' ', ' '],
    [' ', ' ', ' '],
    [' ', ' ', ' ']
    ]


    def draw_grid():
        for row in grid:
            print('|'.join(row))
            print('-----')

    # Mainline
    counter = 0  # lives outside the loop so it persists

    while True:
        draw_grid()
        
        row = int(input("Which row? (0-2): "))
        col = int(input("Which column? (0-2): "))
        
        counter += 1
        
        if counter % 2 == 0:
            grid[row][col] = 'X'
        elif counter % 2 != 0:
            grid[row][col] = 'O'
        else: 
            print("Invalid input")






fourth_try()




# choice = input("first try[a], second try[b]?\n")
# if choice == "a":
#     first_try()
# if choice == "b":
#     second_try()
# else:
#     print("invalid")