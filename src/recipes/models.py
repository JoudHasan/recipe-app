from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=255)
    cooking_time = models.PositiveIntegerField(help_text="Time in minutes")
    difficulty = models.CharField(max_length=50, blank=True)  # Optional field
    ingredients = models.TextField(help_text="List of ingredients")
    categories = models.ManyToManyField(Category, related_name="recipes")

    def __str__(self):
        return self.name

    def calculate_difficulty(self):
        """Calculates difficulty based on cooking time."""
        if self.cooking_time <= 20:
            return "Easy"
        elif 21 <= self.cooking_time <= 45:
            return "Medium"
        else:
            return "Hard"
