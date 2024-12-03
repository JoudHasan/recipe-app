from django.db import models
from django.urls import reverse


class Category(models.Model):
    # This class defines a Category model, which will be used to categorize recipes
    name = models.CharField(max_length=255, unique=True)  # Ensure the name is unique

    def __str__(self):
        # This method returns the name of the category when the object is printed
        return self.name


class Recipe(models.Model):
    # This class defines the Recipe model, which will hold the recipe data
    name = models.CharField(max_length=255)  # The name of the recipe
    cooking_time = models.PositiveIntegerField(help_text="Time in minutes")  # The cooking time (in minutes)
    ingredients = models.TextField(help_text="List of ingredients")  # A text field to list ingredients
    categories = models.ManyToManyField(Category, related_name="recipes")  # A recipe can belong to multiple categories
    pic = models.ImageField(upload_to="recipes", default="recipes/no_picture.jpg", blank=True)

    def __str__(self):
        # This method returns the name of the recipe when the object is printed
        return self.name

    @property
    def difficulty(self):
        """Calculates difficulty based on cooking time and number of ingredients."""
        # Split the ingredients list directly inside the property
        ingredients_list = [ingredient.strip() for ingredient in self.ingredients.split(',')]

        # Apply the same logic four difficulty levels
        if self.cooking_time < 10 and len(ingredients_list) < 4:
            return "Easy"  # Easy if cooking time < 10 minutes and fewer than 4 ingredients
        elif self.cooking_time < 20 and len(ingredients_list) < 6:
            return "Medium"  # Medium if cooking time < 20 minutes and fewer than 6 ingredients
        elif self.cooking_time >= 20 and len(ingredients_list) < 6:
            return "Intermediate"  # Intermediate if cooking time >= 20 minutes and fewer than 6 ingredients
        else:
            return "Hard"  # Hard for all other cases

    def get_absolute_url(self):
        """Returns the URL to access the detail page for this recipe."""
        return reverse('recipes:recipe_detail', kwargs={'pk': self.pk})
