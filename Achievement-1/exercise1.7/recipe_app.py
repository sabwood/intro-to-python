from sqlalchemy import create_engine, Column
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# Connects SQLAlchemy to task_database
engine = create_engine("mysql://cf-python:password@localhost/task_database")

# Creates declarative base
Base = declarative_base()

# Creates a Session and initializes the database
Session = sessionmaker(bind=engine)
session = Session()

# Defines Recipe model
class Recipe(Base):
    __tablename__ = "final_recipes"

    #Defines columns in the table
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    # Defines __repr__ method
    def __repr__(self):
        return (
            f"<Recipe ID: {self.id}"
            f" - Name: {self.name}"
            f" - Difficulty: {self.difficulty}>"
        )

    # Defines __str__ method
    def __str__(self):
        ingredients_list = self.ingredients.split(", ")
        ingredients_str = ", ".join(ingredients_list)

        return (
            f"\n------------------------------------------"
            f"\nRecipe ID: {self.id}"
            f"\nName: {self.name}"
            f"\nIngredients: {ingredients_str}" 
            f"\nCooking Time (in minutes): {self.cooking_time}"
            f"\nDifficulty: {self.difficulty}"
            f"\n"
        )

    # Defines method to calculate recipe difficulty
    def calculate_difficulty(self):
        num_ingredients = len(self.return_ingredients_as_list())
        if self.cooking_time < 10 and num_ingredients < 4:
            self.difficulty = "Easy"
        elif self.cooking_time < 10 and num_ingredients >= 4:
            self.difficulty = "Medium"
        elif self.cooking_time >= 10 and num_ingredients < 4:
            self.difficulty = "Intermediate"
        elif self.cooking_time >= 10 and num_ingredients >= 4:
            self.difficulty = "Hard"

    # Defines method to retrieve ingredients string as a list
    def return_ingredients_as_list(self):
        if self.ingredients == "":
            return []
        else:
            return self.ingredients.split(", ")

# Creates all defines tables in the database
Base.metadata.create_all(engine)

# Defines function to create a new recipe
def create_recipe():
    print("\n------------------------------------------")
    print("\n----------- Create New Recipe: -----------")
    print("\n------------------------------------------")
    print("\n")
    name = str(input("\nEnter recipe name: "))

    # Validates user input
    if len(name) >= 50:
        print("Recipe name cannot be longer than 50 characters. Please try again.")
        return None
    elif 1 > len(name):
        print("Recipe name field cannot be empty. Please try again.")
        return None
            
    cooking_time = int(input("\nEnter cooking time (in minutes): "))
        
    # Validates user input
    if 0 > cooking_time:
        print("Cooking time cannot be less than zero. Please try again.")
        return None

    ingredients = []
    number_of_ingredients = int(input("\nHow many ingredients would you like to enter?: "))
        
    for i in range(number_of_ingredients):
        ingredient = input("\nEnter ingredient name: ")
        ingredients.append(ingredient)

    ingredients_str = ", ".join(ingredients)

    # Creates Recipe object
    recipe_entry = Recipe(
        name = name,
        cooking_time = cooking_time,
        ingredients = ingredients_str
    )

    # Calculates and sets recipe difficulty
    recipe_entry.calculate_difficulty()

    session.add(recipe_entry)
    session.commit()
    print("\nRecipe successfully added!")

# Defines function to view all recipes
def view_all_recipes():
    recipes = session.query(Recipe).all()

    if not recipes:
        print("\nThere are no recipes in the database. Returning to main menu...")
        return None
    else:
        for recipe in recipes:
            print(Recipe.__str__(recipe))

# Defines function to search recipes by ingredient(s)
def search_by_ingredients():
    if session.query(Recipe).count() == 0:
        print("\nThere are no recipes in the database. Returning to main menu...")
        return None
    else:
        results = session.query(Recipe.ingredients).all()

        all_ingredients = []

        for result in results:
            split_ingredients = result[0].split(', ')
            for ingredient in split_ingredients:
                if ingredient not in all_ingredients:
                    all_ingredients.append(ingredient)

        numbered_ingredients = list(enumerate(all_ingredients))

        print("\n Ingredients Available Across All Recipes ")
        print("\n------------------------------------------")

        # Displays all ingredients
        for index, ingredient in enumerate(numbered_ingredients):
            print(str(ingredient[0] + 1) + ". " + ingredient[1])
        print("\n")
            
        selected_ingredients = input("Enter the numbers of the ingredients you'd like to search for (separated by spaces): ")

        # Validates user input
        try:
            selected_indices = [int(i) for i in selected_ingredients.split()]
        except:
            print("\nOops, something went wrong! Returning to main menu...")
            return None
        
        if any(i < 1 or i > len(all_ingredients) for i in selected_indices):
            print("\nInvalid selection. Please enter a number (or numbers) from the displayed options.")
            return None

        # Creates list of ingredients to search
        search_ingredients = [all_ingredients[i] for i in selected_indices]

        # Initializes empty list of conditions
        conditions = []

        # Loops through list of ingredients to create like conditions
        for ingredient in search_ingredients:
            like_term = "%" + ingredient + "%"
            conditions.append(Recipe.ingredients.like(like_term))

        # Try-Except block to display search results to user
        try:
            results = session.query(Recipe).filter(*conditions).all()

            if not results:
                print("\nThere are no recipes in the database with the ingredients you selected. Returning to main menu...")
                return None
            else:
                for recipe in results:
                    print(Recipe.__str__(recipe))
        except:
            print("\nOops, something went wrong!")

# Defines function to edit a recipe
def edit_recipe():
    if session.query(Recipe).count() == 0:
        print("\nThere are no recipes in the database. Returning to main menu...")
        return None
    else:
        results = session.query(Recipe.id, Recipe.name, Recipe.difficulty).all()

        print("\n--------- All Available Recipes: ---------")
        print("\n------------------------------------------")

        # Displays all recipes
        for recipe in results:
            print(Recipe.__repr__(recipe))

        # Try-Except block to select and edit a recipe
        try:
            selected_recipe = int(input("\nEnter the ID of the recipe you want to update: "))

            recipe_to_edit = session.query(Recipe).get(int(selected_recipe))

            # Validates user input
            if not recipe_to_edit:
                print("\nThe number you entered is not associated with a recipe. Returning to main menu...")
                return None

            # Displays selectred recipe details
            print("\n-------- Selected Recipe Details: --------")
            print("\n------------------------------------------")
            print("\n1. Name: ", recipe_to_edit.name)
            print("\n2. Cooking Time (in minutes): ", recipe_to_edit.cooking_time)
            print("\n3. Ingredients: ", recipe_to_edit.ingredients)
            print("\n")

            field_choice = int(input("\nEnter the number corresponding to the field you want to edit: "))

            if field_choice == 1:
                field_name = "name"
            elif field_choice == 2:
                field_name = "cooking_time"
            elif field_choice == 3:
                field_name = "ingredients"
            else:
                print("\nInvalid input. Please enter a valid number.")

            # Edits field based on field choice
            if field_name == 'name':
                updated_name = str(input("\nEnter the new name for your recipe: "))

                # Validates user input
                if len(updated_name) >= 50:
                    print("Recipe name cannot be longer than 50 characters. Please try again.")
                elif 1 > len(updated_name):
                    print("Recipe name field cannot be empty. Please try again.")
                elif not updated_name.isalpha():
                    print("Recipe name can only contain letters. Please try again.")
                
                recipe_to_edit.name = updated_name
                print("\nRecipe name updated successfully!")
            elif field_name == 'cooking_time':
                updated_cooking_time = int(input("Enter the new cooking time (in minutes) for your recipe: "))

                # Validates user input
                if 0 > updated_cooking_time:
                    print("Cooking time cannot be less than zero. Please try again.")
                
                recipe_to_edit.cooking_time = updated_cooking_time
                print("\nRecipe cooking time updated successfully!")
            elif field_name == 'ingredients':
                new_ingredients = []
                updated_ingredients = int(input("\nHow many ingredients would you like to enter?: "))
        
                for i in range(updated_ingredients):
                    ingredient = input("\nEnter ingredient name: ")
                    new_ingredients.append(ingredient)

                recipe_to_edit.ingredients = ", ".join(new_ingredients)
                print("\nRecipe ingredients updated successfully!")

            # Recalculates and sets recipe difficulty
            recipe_to_edit.calculate_difficulty()
            session.commit()
        except:
            print("\nOops, something went wrong! Please try again.")

# Defines function to delete a recipe
def delete_recipe():
    if session.query(Recipe).count() == 0:
        print("\nThere are no recipes in the database. Returning to main menu...")
        return None
    else:
        results = session.query(Recipe.id, Recipe.name, Recipe.difficulty).all()

        print("\n--------- All Available Recipes: ---------")
        print("\n------------------------------------------")

        # Displays all recipes
        for recipe in results:
            print(Recipe.__repr__(recipe))

        selected_recipe = int(input("\nEnter the ID of the recipe you want to delete: "))

        recipe_to_delete = session.query(Recipe).get(int(selected_recipe))

        # Validates user input
        if not recipe_to_delete:
            print("\nThe number you entered is not associated with a recipe. Returning to main menu...")
            return None

        confirmation = input(f"\nAre you sure you want to delete the {recipe_to_delete.name} recipe? (y/n): ")

        # Validates user input
        if confirmation == "n":
            print("\nDeletion cancelled. Returning to main menu...")
            return None
        elif confirmation == "y":
            session.delete(recipe_to_delete)
            session.commit()
            print("\nRecipe deleted successfully!")
        else:
            print("\nInvalid input. Please try again.")

# Defines main menu function
def main_menu():
    choice = ""
    while(choice != 'quit'):

        # Displays menu options
        print("\n     Welcome to the Recipes Database!     ")
        print("\n------------------------------------------")
        print("\n--------------- Main Menu: ---------------")
        print("\nWhat would you like to do? Pick a choice! ")
        print("\n1. Create a recipe")
        print("\n2. View all recipes")
        print("\n3. Search for recipes by ingredients")
        print("\n4. Edit a recipe")
        print("\n5. Delete a recipe")
        print("\n6. Exit (Type 'quit' to exit the program)")
        choice = input("Enter your choice: ")

        # Executes corresponding function based on user input
        if choice == '1':
            create_recipe()
        elif choice == '2':
            view_all_recipes()
        elif choice == '3':
            search_by_ingredients()
        elif choice == '4':
            edit_recipe()
        elif choice == '5':
            delete_recipe()
        elif choice == '6':
            session.commit()
            session.close()
    
    print("\nThe user chose: " + str(choice))

main_menu()