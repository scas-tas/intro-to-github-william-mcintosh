ingredients_dictionary = {}

while True: 
  ing = input("Ingredient: ")
  if not ing:
    break
  try:
    ingredients_dictionary[ing] = int(input("Quantity: "))
  except:
    print("Please enter a valid number")
print("Total ingredients collected:")
for i, n in ingredients_dictionary.items():
  print(f"{i}: {n}")