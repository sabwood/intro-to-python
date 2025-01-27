class Recipe:

    all_ingredients = set()

    def __init__(self, name):
        self.name = name
        self.ingredients = []
        self.cooking_time = int(0)
        self.difficulty = ""

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_cooking_time(self):
        return self.cooking_time

    def set_cooking_time(self, cooking_time):
        self.cooking_time = cooking_time

    def add_ingredients(self, *ingredients):
        self.ingredients.extend(ingredients)
        self.update_all_ingredients()

    def get_ingredients(self):
        return self.ingredients

    def calculate_difficulty(self):
        if self.cooking_time < 10 and len(self.ingredients) < 4:
            self.difficulty = "Easy"
        elif self.cooking_time < 10 and len(self.ingredients) >= 4:
            self.difficulty = "Medium"
        elif self.cooking_time >= 10 and len(self.ingredients) < 4:
            self.difficulty = "Intermediate"
        elif self.cooking_time >= 10 and len(self.ingredients) >= 4:
            self.difficulty = "Hard"

    def get_difficulty(self):
        if not self.difficulty:
            self.calculate_difficulty()
        return self.difficulty

    def search_ingredient(self, ingredient):
        if ingredient in self.ingredients:
            return True
        else:
            return False

    def update_all_ingredients(self):
        for ingredient in self.ingredients:
            if not ingredient in self.all_ingredients:
                self.all_ingredients.add(ingredient)

    def __str__(self):
        output = (
            "Name of the recipe: " + self.name
            + "\nCooking Time (in minutes): " + str(self.cooking_time)
            + "\nIngredients: " + str(self.ingredients)
            + "\nDifficulty: " + str(self.difficulty)
        )
        return output

def recipe_search(recipes_list, ingredient):
    data = recipes_list
    search_term = ingredient
    for recipe in data:
        if recipe.search_ingredient(ingredient):
            print(recipe)

recipes_list = []

tea = Recipe("Tea")
tea.add_ingredients("Tea Leaves", "Sugar", "Water")
tea.set_cooking_time(5)
tea.get_difficulty()
print(tea)
recipes_list.append(tea)

coffee = Recipe("Coffee")
coffee.add_ingredients("Coffee Powder", "Sugar", "Water")
coffee.set_cooking_time(5)
coffee.get_difficulty()
print(coffee)
recipes_list.append(coffee)

cake = Recipe("Cake")
cake.add_ingredients("Sugar", "Butter", "Eggs", "Vanilla Essence", "Flour","Baking Powder", "Milk")
cake.set_cooking_time(50)
cake.get_difficulty()
print(cake)
recipes_list.append(cake)

banana_smoothie = Recipe("Banana Smoothie")
banana_smoothie.add_ingredients("Bananas", "Milk", "Peanut Butter", "Sugar", "Ice Cubes")
banana_smoothie.set_cooking_time(5)
banana_smoothie.get_difficulty()
print(banana_smoothie)
recipes_list.append(banana_smoothie)

print("\nRecipes with Water: ")
recipe_search(recipes_list, "Water")

print("\nRecipes with Sugar: ")
recipe_search(recipes_list, "Sugar")

print("\nRecipes with Bananas: ")
recipe_search(recipes_list, "Bananas")