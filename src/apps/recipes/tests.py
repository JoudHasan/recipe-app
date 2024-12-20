from django.test import TestCase
from django.urls import reverse
from .models import Recipe, Category


class RecipeModelTest(TestCase):
    def setUp(self):
        # Create Categories
        self.desserts = Category.objects.create(name="Desserts")
        self.beverages = Category.objects.create(name="Beverages")

        # Create Recipes
        self.recipe1 = Recipe.objects.create(
            name="Fruit Salad",
            cooking_time=20,
            ingredients="Mixed fruits, sugar, mint",
        )
        self.recipe1.categories.add(self.desserts)

        self.recipe2 = Recipe.objects.create(
            name="Lemonade",
            cooking_time=10,
            ingredients="Lemon, sugar, water",
        )
        self.recipe2.categories.add(self.beverages)

    def test_difficulty_property(self):
        # Test difficulty calculation for each recipe
        self.assertEqual(self.recipe1.difficulty, "Intermediate")
        self.assertEqual(self.recipe2.difficulty, "Easy")

    def test_recipe_category(self):
        # Test category association
        self.assertIn(self.desserts, self.recipe1.categories.all())
        self.assertIn(self.beverages, self.recipe2.categories.all())

    def test_recipe_name(self):
        # Test recipe name
        self.assertEqual(self.recipe1.name, "Fruit Salad")

    def test_ingredient_field(self):
        # Test ingredients field content
        self.assertIn("sugar", self.recipe1.ingredients)
        self.assertIn("Lemon", self.recipe2.ingredients)

    def test_get_absolute_url(self):
        # Test the get_absolute_url method
        expected_url = reverse('recipes:recipe_detail', kwargs={'recipe_name': self.recipe1.name})
        self.assertEqual(self.recipe1.get_absolute_url(), expected_url)


class RecipeViewsTest(TestCase):
    def setUp(self):
        # Create Categories
        self.beverages = Category.objects.create(name="Beverages")

        # Create Recipes
        self.recipe = Recipe.objects.create(
            name="Lemonade",
            cooking_time=10,
            ingredients="Lemon, sugar, water",
        )
        self.recipe.categories.add(self.beverages)

    def test_home_view(self):
        # Test home view renders correct template
        response = self.client.get(reverse("recipes:home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/recipes_home.html")

    def test_recipe_list_view(self):
        # Test recipe list view renders correct template
        response = self.client.get(reverse("recipes:recipe_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/recipes_list.html")
        self.assertContains(response, "Lemonade")  # Ensure recipe is listed

    def test_empty_recipe_list_view(self):
        # Test when no recipes exist
        Recipe.objects.all().delete()
        response = self.client.get(reverse("recipes:recipe_list"))
        self.assertContains(response, "No recipes available", status_code=200)

    def test_recipe_detail_view(self):
        # Test recipe detail view renders correct template
        response = self.client.get(reverse("recipes:recipe_detail", args=["Lemonade"]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/recipe_detail.html")
        self.assertContains(response, "Lemonade")  # Ensure recipe name is displayed
        self.assertContains(response, "10 minutes")  # Ensure cooking time is displayed

    def test_invalid_recipe_detail_view(self):
        # Test invalid recipe detail view
        response = self.client.get(reverse("recipes:recipe_detail", args=["InvalidRecipe"]))
        self.assertEqual(response.status_code, 404)


class RecipeURLTest(TestCase):
    def setUp(self):
        # Create a Recipe
        self.recipe = Recipe.objects.create(
            name="Lemonade",
            cooking_time=10,
            ingredients="Lemon, sugar, water",
        )

    def test_home_url(self):
        response = self.client.get(reverse("recipes:home"))
        self.assertEqual(response.status_code, 200)

    def test_recipe_list_url(self):
        response = self.client.get(reverse("recipes:recipe_list"))
        self.assertEqual(response.status_code, 200)

    def test_recipe_detail_url(self):
        response = self.client.get(reverse("recipes:recipe_detail", args=["Lemonade"]))
        self.assertEqual(response.status_code, 200)

    def test_absolute_url_integration(self):
        # Test that the URL generated by get_absolute_url works with the detail view
        response = self.client.get(self.recipe.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Lemonade")

    def test_invalid_recipe_detail_url(self):
        # Test accessing a recipe that does not exist
        response = self.client.get(reverse("recipes:recipe_detail", args=["InvalidRecipe"]))
        self.assertEqual(response.status_code, 404)
