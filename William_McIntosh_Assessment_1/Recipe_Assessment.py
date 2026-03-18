# ingredients_dictionary = {}

# while True: 
#   ing = input("Ingredient: ")
#   if not ing:
#     break
#   try:
#     ingredients_dictionary[ing] = int(input("Quantity: "))
#   except:
#     print("Please enter a valid number")
# print("Total ingredients collected:")
# for i, n in ingredients_dictionary.items():
#   print(f"{i}: {n}")
# 

def create_new_file():
    try:
        with open("William_McIntosh_Assessment_1/recipe.txt", "w") as output:
            output.write("test new")
    except Exception as e:
            print("Error:", e)

def modify_existing_file():
    print("Modifying file...")
    try:
        with open("William_McIntosh_Assessment_1/recipe.txt", "w") as output:
            output.write("\ntest modify")
    except Exception as e:
        print("Error:", e)

def get_user_input():
    return input("New file, Modify, Quit\n").lower()

def main():

    while True:
        decision = get_user_input()

        if decision in ("", "quit"):
            break
        elif decision in ("new file", "new"):
            create_new_file()
        elif decision == "modify":
            modify_existing_file()
        else:
            print("Invalid input")

if __name__ =="__main__":
    main()