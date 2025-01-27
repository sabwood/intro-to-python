import pickle

def display_recipe(recipe):
    print("Recipe: ", recipe['name'])
    print("Cooking Time (min): ", recipe['cooking_time'])
    print("Ingredients: ")
    for ingredient in recipe["ingredients"]:
        print(ingredient)
    print("Difficulty Level: ", recipe['difficulty'])

def search_ingredients(data):
    all_ingredients = enumerate(data["all_ingredients"])
    numbered_ingredients = list(all_ingredients)
    
    print("Ingredients Available Acress All Recipes")
    print("----------------------------------------")
    for ingredient in numbered_ingredients:
        print(ingredient[0], ingredient[1])
    
    try:
        num = int(input("Enter the number corresponding to the ingredient you want to search: "))
        ingredient_searched = numbered_ingredients[num][1]
    except:
        print("Invalid input. Please enter a valid number.")
    else:
        for recipe in data["recipes_list"]:
            if ingredient_searched in recipe["ingredients"]:
                display_recipe(recipe)

file_name = input("Enter the name of the file that contains your recipe(s). ")

try:
    file = open(file_name, "rb")
    data = pickle.load(file)
    print("File loaded successfully!")
except FileNotFoundError:
    print("File with that name not found. Please try again.")
except:
    print("Oops! Something went wrong. Try again.")
else:
    file.close()
    search_ingredients(data)