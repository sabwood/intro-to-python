recipes_list = []
ingredients_list = []

def take_recipe():
    name = str(input("Enter your recipe name: "))
    cooking_time = int(input("Enter the cooking time in minutes: "))
    ingredients = list(input("Enter the ingredients, separated by a comma: ").split(", "))
    recipe = {
        "name": name,
        "cooking_time": cooking_time,
        "ingredients": ingredients
    }

    return recipe

n = int(input("Enter how many recipes you want to make: "))

for i in range(n):
    recipe = take_recipe()
    for ingredient in recipe["ingredients"]:
        if not ingredient in ingredients_list:
            ingredients_list.append(ingredient)
    recipes_list.append(recipe)

for recipe in recipes_list:
    if recipe['cooking_time'] < 10 and len(recipe['ingredients']) < 4:
        recipe['difficulty'] = 'Easy'
    elif recipe['cooking_time'] < 10 and len(recipe['ingredients']) >= 4:
        recipe['difficulty'] = 'Medium'
    elif recipe['cooking_time'] >= 10 and len(recipe['ingredients']) < 4:
        recipe['difficulty'] = 'Intermediate'
    elif recipe['cooking_time'] >= 10 and len(recipe['ingredients']) >= 4:
        recipe['difficulty'] = 'Hard'
    
    print("Recipe: ", recipe['name'])
    print("Cooking Time (min): ", recipe['cooking_time'])
    print("Ingredients: ")
    for position, ingredient in enumerate(recipe['ingredients']):
        print(str(position + 1) + ", " + ingredient)
    ingredients_list.sort()
    print("Difficulty Level: ", recipe['difficulty'])

def all_ingredients():
    print("Ingredients Available Acress All Recipes")
    print("----------------------------------------")
    ingredients_list.sort()
    for ingredient in ingredients_list:
        print(ingredient)

all_ingredients()