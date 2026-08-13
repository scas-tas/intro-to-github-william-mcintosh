
def count_empty(classroom: list) -> int:
    #loop through each seat in this row and update count
    count = 0
    for row in classroom:
        for seat in row:
            if seat == 0:
                count += 1
    return count
 
def most_empty_row(classroom: list) -> int:
    best_row = 0
    best_count = -1
    for row_index in range(len(classroom)):
        empty_count = 0
        for seat_index in range(len(classroom[row_index])):
            if classroom[row_index][seat_index] == 0:
            #classroom[row_index] picks the row,
            #[seat_index] picks the seat in that row
            #e.g. classroom[2][1] for row 2 seat 1
                empty_count += 1
        if empty_count > best_count:
            best_row = row_index
            best_count = empty_count
    return best_row + 1

def main():
    #classroom = [[1,2,3],[0,0,4],[5,0,0],[1,2,3],[5,5,5,5],[]]
    #classroom = [[1,2],[3,4]]
    #classroom = [[0,0],[0,0]]
    #classroom = [[1,2,0],[0,3,4],[5,0,0]]
    classroom = [[1,2,3],[0,0,4],[5,0,0]]
    #classroom = [[1,2],[3,4]]

    print("Empty seats:", count_empty(classroom))
    print("Most empty row:", most_empty_row(classroom))

main()