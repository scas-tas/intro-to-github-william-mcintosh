import random

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

