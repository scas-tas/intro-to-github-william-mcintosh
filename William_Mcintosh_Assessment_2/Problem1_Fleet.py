def combine_trucks(trucks, T1, T2):
    # return the total packages in T1 and T2
    return trucks[T1 - 1] + trucks[T2 - 1]

def main_test_cases():
    trucks1 = [4, 7, 2, 6, 9]
    print(combine_trucks(trucks1, 2, 4))    # Expected: 13
    trucks2 = [5, 10, 15, 0, 0]
    print(combine_trucks(trucks2, 1, 3))    # Expected: 20
    trucks3 = [0, 0, 0, 0, 1000]
    print(combine_trucks(trucks3, 5, 5))    # Expected: 2000

main_test_cases() 