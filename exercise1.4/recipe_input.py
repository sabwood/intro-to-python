import pickle

recipes_list = []
all_ingredients = []

# Function to determine recipe difficulty
def calc_difficulty(cooking_time, ingredients):
    if cooking_time < 10 and len(ingredients) < 4:
        difficulty = 'Easy'
    elif cooking_time < 10 and len(ingredients) >= 4:
        difficulty = 'Medium'
    elif cooking_time >= 10 and len(ingredients) < 4:
        difficulty = 'Intermediate'
    elif cooking_time >= 10 and len(ingredients) >= 4:
        difficulty = 'Hard'
    return difficulty

# Function to take user input for single recipe
def take_recipe():
    name = str(input("Enter your recipe name: "))
    cooking_time = int(input("Enter the cooking time in minutes: "))
    ingredients = list(input("Enter the ingredients, separated by a comma: ").split(", "))
    difficulty = calc_difficulty(cooking_time, ingredients)
    recipe = {
        "name": name,
        "cooking_time": cooking_time,
        "ingredients": ingredients,
        "difficulty": difficulty
    }

    return recipe

file_name = input("Enter the file name to load recipes from (or save to): ")

# Tries to load user-defined file
try:
    file = open(file_name, "rb")
    data = pickle.load(file)
    print("File loaded successfully!")
# If the user-defined file is not found, a new one is created with the data dictionary
except FileNotFoundError:
    print("File with that name not found. Creating new file...")
    data = {"recipes_list": recipes_list, "all_ingredients": all_ingredients}
# If other error occurs, performs same operations as previous except block
except:
    print("Oops! Something went wrong. Try again.")
    data = {"recipes_list": recipes_list, "all_ingredients": all_ingredients}
# Closes file stream
else:
    file.close()
# Extracts values from the data dictionary
finally:
    recipes_list = data["recipes_list"]
    all_ingredients = data["all_ingredients"]

n = int(input("Enter how many recipes you want to make: "))

# Checks given recipes and whether any ingredients should be added to the ingredients list
for i in range(n):
    recipe = take_recipe()
    for ingredient in recipe["ingredients"]:
        if not ingredient in all_ingredients:
            all_ingredients.append(ingredient)
    recipes_list.append(recipe)

# Gathers updated data into a new data dictionary
data = {"recipes_list": recipes_list, "all_ingredients": all_ingredients}

# Opens the user-defined file, writes the new data dictionary to it, and closes the file
updated_file = open(file_name, "wb")
pickle.dump(data, updated_file)
updated_file.close()
print("Recipe file has been updated!")