from django.db import models


class Category(models.Model):
    # This class defines a Category model, which will be used to categorize recipes
    name = models.CharField(max_length=255)  # A category will have a name field, which is a string

    def __str__(self):
        # This method returns the name of the category when the object is printed
        return self.name


class Recipe(models.Model):
    # This class defines the Recipe model, which will hold the recipe data
    name = models.CharField(max_length=255)  # The name of the recipe
    cooking_time = models.PositiveIntegerField(help_text="Time in minutes")  # The cooking time (in minutes)
    ingredients = models.TextField(help_text="List of ingredients")  # A text field to list ingredients
    categories = models.ManyToManyField(Category, related_name="recipes")  # A recipe can belong to multiple categories

    def __str__(self):
        # This method returns the name of the recipe when the object is printed
        return self.name

    def calculate_difficulty(self):
        """Calculates difficulty based on cooking time and number of ingredients."""
        
        # Split the ingredients list by commas and count how many ingredients there are.
        # Assumes the ingredients are separated by commas (e.g., "salt, pepper, chicken").
        num_ingredients = len(self.ingredients.split(','))

        # Determine difficulty based on cooking time and number of ingredients
        if self.cooking_time <= 20 and num_ingredients <= 5:
            return "Easy"  # If the cooking time is 20 minutes or less and ingredients are 5 or fewer, it's easy
        elif 21 <= self.cooking_time <= 45 and num_ingredients <= 10:
            return "Medium"  # If cooking time is between 21 and 45 minutes and ingredients are 10 or fewer, it's medium
        else:
            return "Hard"  # If the cooking time is greater than 45 minutes or ingredients exceed 10, it's hard
