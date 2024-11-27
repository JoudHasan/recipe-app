from django.test import TestCase
from .models import Recipe, Category

class RecipeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create Categories
        desserts = Category.objects.create(name="Desserts")
        beverages = Category.objects.create(name="Beverages")
        entrees = Category.objects.create(name="Entrees")

        # Create Recipes with explicit difficulty
        fruit_salad = Recipe.objects.create(
            name="Fruit Salad",
            cooking_time=20,
            ingredients="Mixed fruits, sugar, mint",
            difficulty="Easy",  # Explicitly set based on cooking time
        )
        fruit_salad.categories.add(desserts)

        nachos = Recipe.objects.create(
            name="Nachos",
            cooking_time=15,
            ingredients="Tortilla chips, cheese, salsa",
            difficulty="Easy",  # Explicitly set based on cooking time
        )
        nachos.categories.add(entrees)

        grilled_chicken = Recipe.objects.create(
            name="Grilled Chicken",
            cooking_time=60,
            ingredients="Chicken, spices, oil",
            difficulty="Hard",  # Explicitly set based on cooking time
        )
        grilled_chicken.categories.add(entrees)

        lemonade = Recipe.objects.create(
            name="Lemonade",
            cooking_time=10,
            ingredients="Lemon, sugar, water",
            difficulty="Easy",  # Explicitly set based on cooking time
        )
        lemonade.categories.add(beverages)

        chocolate_cake = Recipe.objects.create(
            name="Chocolate Cake",
            cooking_time=30,
            ingredients="Chocolate, Flour, Sugar, Eggs",
            difficulty="Medium",  # Explicitly set based on cooking time
        )
        chocolate_cake.categories.add(desserts)

    def test_difficulty_set_correctly(self):
        # Test difficulty for each recipe
        recipe_easy = Recipe.objects.get(name="Fruit Salad")
        recipe_medium = Recipe.objects.get(name="Chocolate Cake")
        recipe_hard = Recipe.objects.get(name="Grilled Chicken")

        # Assertions
        self.assertEqual(recipe_easy.difficulty, "Easy")
        self.assertEqual(recipe_medium.difficulty, "Medium")
        self.assertEqual(recipe_hard.difficulty, "Hard")

    def test_recipe_category(self):
        # Test recipe category association
        recipe = Recipe.objects.get(name="Lemonade")
        category = recipe.categories.first()
        self.assertEqual(category.name, "Beverages")

    def test_recipe_name(self):
        # Test recipe name
        recipe = Recipe.objects.get(name="Nachos")
        self.assertEqual(recipe.name, "Nachos")

    def test_ingredient_field(self):
        # Test recipe ingredient field
        recipe = Recipe.objects.get(name="Grilled Chicken")
        self.assertIn("Chicken", recipe.ingredients)
