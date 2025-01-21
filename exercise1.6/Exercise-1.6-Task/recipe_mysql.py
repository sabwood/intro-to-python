import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='cf-python',
    passwd='password'
)

cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")

cursor.execute("USE task_database")

cursor.execute('''CREATE TABLE IF NOT EXISTS Recipes(
    id              INT PRIMARY KEY AUTO_INCREMENT,
    name            VARCHAR(50),
    ingredients     VARCHAR(255),
    cooking_time    INT,
    difficulty      VARCHAR(20)
)''')

def calculate_difficulty(cooking_time, ingredients):
    if cooking_time < 10 and len(ingredients) < 4:
        difficulty = "Easy"
    elif cooking_time < 10 and len(ingredients) >= 4:
        difficulty = "Medium"
    elif cooking_time >= 10 and len(ingredients) < 4:
        difficulty = "Intermediate"
    elif cooking_time >= 10 and len(ingredients) >= 4:
        difficulty = "Hard"
    return difficulty

def main_menu(conn, cursor):
    def create_recipe(conn, cursor):
        ingredients_list = []

        name = str(input("\nEnter recipe name: "))
        cooking_time = int(input("\nEnter cooking time (in minutes): "))
        ingredients = input("Enter ingredients, separated by a comma: ")

        ingredients_list.append(ingredients)
        ingredients_str = ", ".join(ingredients_list)

        difficulty = calculate_difficulty(cooking_time, ingredients_list)

        sql = 'INSERT INTO Recipes (name, ingredients, cooking_time, difficulty) VALUES (%s, %s, %s, %s)'
        val = (name, ingredients_str, cooking_time, difficulty)
        cursor.execute(sql, val)
        conn.commit()

        print("\nRecipe successfully created!")

    def search_recipe(conn, cursor):
        all_ingredients = []

        cursor.execute("SELECT ingredients FROM Recipes")
        results = cursor.fetchall()

        for ingredients_list in results:
            for ingredient in ingredients_list:
                if not ingredient in all_ingredients:
                    split_ingredients = ingredient.split(", ")
                    all_ingredients.extend(split_ingredients)

        numbered_ingredients = list(enumerate(all_ingredients))

        print("\nIngredients Available Acress All Recipes")
        print("\n----------------------------------------")
        for index, ingredient in enumerate(numbered_ingredients):
            print(str(ingredient[0] + 1) + ". " + ingredient[1])

        try:
            num = int(input("Enter the number corresponding to the ingredient you want to search: "))
            true_index = num - 1
            search_ingredient = numbered_ingredients[true_index][1]
        
        except ValueError:
            print("\nInvalid input. Please enter a valid number.")

        else:
            cursor.execute('SELECT * FROM Recipes WHERE ingredients LIKE %s', ('%' + search_ingredient + '%',))
            result = cursor.fetchall()

            if result:
                print("\nHere are the recipe(s) containing the ingredient you searched: ")
                for recipe in result:
                    print("\nID: ", recipe[0])
                    print("\nName: ", recipe[1])
                    print("\nIngredients: ", recipe[2])
                    print("\nCooking Time (in minutes): ", recipe[3])
                    print("\nDifficulty: ", recipe[4])
                    print()
            else:
                print("\nNo recipes found with the ingredient you searched.") 
    
    def update_recipe(conn, cursor):
        cursor.execute("SELECT * FROM Recipes")
        result = cursor.fetchall()

        print("\nRecipes you can update: ")
        for recipe in result:
            ingredients_list = recipe[2].split(", ")
            ingredients_str = ", ".join(ingredients_list)

            print("\nID: ", recipe[0])
            print("\nName: ", recipe[1])
            print("\nIngredients: ", ingredients_str)
            print("\nCooking Time (in minutes): ", recipe[3])
            print("\nDifficulty: ", recipe[4])
            print()
        
        try:
            recipe_choice = int(input("\nEnter the ID of the recipe you want to update: "))

            print("\nWhich column do you want to update? ")
            print("\n1. Name")
            print("\n2. Cooking Time")
            print("\n3. Ingredients")
            column_choice = int(input("\nEnter the number corresponding to your choice: "))

            if column_choice == 1:
                column_name = "name"
            elif column_choice == 2:
                column_name = "cooking_time"
            elif column_choice == 3:
                column_name = "ingredients"
            else:
                print("\nInvalid input. Please enter a valid number.")
            
            if column_name == "name":
                updated_name = str(input("Enter the new name for your recipe: "))

                sql = 'UPDATE Recipes SET name = %s WHERE id = %s'
                val = (updated_name, recipe_choice)
                cursor.execute(sql, val)
                conn.commit()

                print("\nRecipe name updated successfully!")

            elif column_name == "cooking_time":
                cooking_time_input = int(input("Enter the new cooking time (in minutes) for your recipe: "))
                cursor.execute("UPDATE Recipes SET cooking_time = %s WHERE id = %s", (cooking_time_input, recipe_choice))
                print("Recipe cooking time updated successfully!")

                cursor.execute("SELECT * FROM Recipes WHERE id = %s", (recipe_choice,))
                result = cursor.fetchall()
                ingredients_str = result[0][2]
                ingredients = ingredients_str.split(", ")
                updated_cooking_time = result[0][3]

                updated_difficulty = calculate_difficulty(updated_cooking_time, ingredients)

                sql_difficulty = 'UPDATE Recipes SET difficulty = %s WHERE id = %s'
                val_difficulty = (updated_difficulty, recipe_choice)
                cursor.execute(sql_difficulty, val_difficulty)

                conn.commit()
                
            elif column_name == "ingredients":
                ingredients_input = input("Enter the new ingredients for this recipe, separated by a comma: ")
                cursor.execute("UPDATE Recipes SET ingredients = %s WHERE id = %s", (ingredients_input, recipe_choice))
                print("Recipe ingredients updated successfully!")

                cursor.execute("SELECT * FROM Recipes WHERE id = %s", (recipe_choice,))
                result = cursor.fetchall()
                cooking_time = result[0][3]
                ingredients_str = result[0][2]
                ingredients = ingredients_str.split(", ")
                
                updated_difficulty = calculate_difficulty(cooking_time, ingredients)

                sql_difficulty = 'UPDATE Recipes SET difficulty = %s WHERE id = %s'
                val_difficulty = (updated_difficulty, recipe_choice)
                cursor.execute(sql_difficulty, val_difficulty)

                conn.commit()

        except ValueError:
            print("Invalid input. Please enter a valid number.")
    
    def delete_recipe(conn, cursor):
        cursor.execute("SELECT * FROM Recipes")
        result = cursor.fetchall()

        print("\nRecipes you can delete: ")
        for recipe in result:
            ingredients_list = recipe[2].split(", ")
            ingredients_str = ", ".join(ingredients_list)

            print("\nID: ", recipe[0])
            print("\nName: ", recipe[1])
            print("\nIngredients: ", ingredients_str)
            print("\nCooking Time (in minutes): ", recipe[3])
            print("\nDifficulty: ", recipe[4])
            print()
        
        try:
            recipe_choice = int(input("\nEnter the ID of the recipe you want to delete: "))

            sql = 'DELETE FROM Recipes WHERE id = %s'
            val = (recipe_choice,)
            cursor.execute(sql, val)

            conn.commit()

            print("Recipe deleted successfully!")
        except:
            print("Something went wrong! Please try again.")
    
    choice = ""
    while(choice != 'quit'):
        print("\n     Welcome to the Recipes Database!     ")
        print("\n------------------------------------------")
        print("\n--------------- Main Menu: ---------------")
        print("\nWhat would you like to do? Pick a choice! ")
        print("\n1. Create a recipe")
        print("\n2. Search for a recipe")
        print("\n3. Update a recipe")
        print("\n4. Delete a recipe")
        print("\n5. Exit (Type 'quit' to exit the program)")
        choice = input("Enter your choice: ")

        if choice == '1':
            create_recipe(conn, cursor)
        elif choice == '2':
            search_recipe(conn, cursor)
        elif choice == '3':
            update_recipe(conn, cursor)
        elif choice == '4':
            delete_recipe(conn, cursor)
        elif choice == '5':
            conn.commit()
            conn.close()
    
    print("\nThe user chose: " + str(choice))


main_menu(conn, cursor)