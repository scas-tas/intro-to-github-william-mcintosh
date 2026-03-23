
FILE = "William_McIntosh_Assessment_1/recipe.txt"
def cleaning(recipes):
    return [r.strip() for r in recipes if r.strip() != ""]
    # Removes any emtpy entries from a list
    # returns a new list.


def load_recipes():
    try:
        with open(FILE, "r") as x:
            content = x.read().strip()
            if not content:
                return []
            recipes = content.split("\n\n")
            return cleaning(recipes)
    except FileNotFoundError:
        return []
    

def save_recipe(recipes):
    try:
        recipes = cleaning(recipes)
        with open(FILE, "w") as x:
            x.write("\n\n".join(recipes))
    except Exception as e:
        print("Error Saving:", e)


def create_recipe():
    recipes = load_recipes()
    recipe_name = input("Recipe name: ")

    ingredients_list = []
    while True:
        ingredient = input("Ingredient: ")
        if ingredient == "":
            break
        ingredients_list.append(ingredient)
    ingredients = "\n".join(ingredients_list)

    recipe = (
        f"Recipe name: {recipe_name}\n"
        f"Ingredients: \n{ingredients}\n"
        )
    recipes.append(recipe)
    save_recipe(recipes)
    print("Recipe saved\n")


def see_recipe():
    recipes = load_recipes()
    if not recipes:
        print("No recipes found.\n")
        return
    for recipe in recipes:
        print(f"{recipe}\n")


def modify_recipe():
    recipes = load_recipes()
    recipe_name = input("Enter recipe name to modify: ").lower()
    new_recipes = []
    found = False

    for recipe in recipes:
        name_line = recipe.split("\n")[0]
        # splits the recipe string at every \n
        # produces a list of lines
        # the [0] thats the first item in the list
        actual_name = name_line.replace("Recipe name: ","").strip().lower()
        #removes the "recipe name" part and random whitespace
        if actual_name == recipe_name:
            print("Recipe found. Enter new details")
            new_name = input("New name: ")

            new_ingredients_list = []
            while True:
                ingredient = input("Ingredient: ")
                if ingredient == "":
                    break
                new_ingredients_list.append(ingredient)
            ingredients = "\n".join(new_ingredients_list)

            new_recipe = (
                f"Recipe name: {new_name}\n"
                f"Ingredients: \n{ingredients}\n"
            )
            new_recipes.append(new_recipe)
            found = True
        else:
            new_recipes.append(recipe)
            
    if not found:
        print("Recipe not found.")
    else:
        print("Recipe modified.")
    save_recipe(new_recipes)


def delete_recipe():
    recipes = load_recipes()
    recipe_name = input("Enter recipe name to delete: ")
    new_recipes = []
    found = False

    for recipe in recipes:
        name_line = recipe.split("\n")[0]
        actual_name = name_line.replace("Recipe name: ","").strip().lower()
        if actual_name == recipe_name:
            found = True
        else:
            new_recipes.append(recipe)
    if not found:
        print("Recipe not found.")
    else:
        print("Recipe deleted.")
    save_recipe(new_recipes)


def reset():
    confirm = input("CONFIRM FACTORY RESET [YES / NO]\n\n").lower()
    if confirm == "yes":
        save_recipe([])
        print("\nAll recipes deleted.")
    else:
        print("\nReset Cancelled.")


def main():
    # the dictionary maps user commands to functions
    actions = {
        "new": create_recipe,
        "view": see_recipe,
        "modify": modify_recipe,
        "delete": delete_recipe,
        "reset": reset
    }
    while True:
        print("~"*30,"\n")
        choice = input("New, View, Modify, Delete, Reset, Quit\n\n").lower()
        if choice == "quit":
            break
        elif choice in actions:
            print("\n","~"*30,"\n")
            actions[choice]()
        else:
            print("Invalid input")


if __name__ == "__main__":
    main()

    