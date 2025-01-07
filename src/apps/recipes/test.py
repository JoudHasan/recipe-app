from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from apps.recipes.models import Recipe, Category
from apps.recipes.forms import RecipeForm

# Test Models
class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Desserts")

    def test_category_name(self):
        self.assertEqual(self.category.name, "Desserts")

    def test_category_str_method(self):
        self.assertEqual(str(self.category), "Desserts")


class RecipeModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.category = Category.objects.create(name="Drinks")
        self.recipe = Recipe.objects.create(
            name="Lemonade",
            cooking_time=5,
            ingredients="Lemon, sugar",
        )
        self.recipe.categories.add(self.category)

    def test_recipe_name(self):
        self.assertEqual(self.recipe.name, "Lemonade")

    def test_recipe_ingredients(self):
        self.assertIn("Lemon", self.recipe.ingredients)

    def test_get_absolute_url(self):
        expected_url = reverse('recipes:recipe_detail', kwargs={'pk': self.recipe.pk})
        self.assertEqual(self.recipe.get_absolute_url(), expected_url)

    def test_recipe_category(self):
        self.assertIn(self.category, self.recipe.categories.all())

    def test_recipe_difficulty_easy(self):
        self.assertEqual(self.recipe.difficulty, "Easy")


# Test Forms
class RecipeFormTest(TestCase):
    def test_valid_recipe_form(self):
        form = RecipeForm(data={
            'name': 'Fruit Salad',
            'ingredients': 'Fruits, honey, mint',
            'cooking_time': 15
        })
        self.assertTrue(form.is_valid())

    def test_invalid_recipe_form(self):
        form = RecipeForm(data={})
        self.assertFalse(form.is_valid())


# Test Views
class RecipeViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='password')
        cls.category = Category.objects.create(name="Snacks")
        for i in range(15):
            recipe = Recipe.objects.create(
                name=f"Recipe {i}",
                cooking_time=15,
                ingredients="Test ingredient"
            )
            recipe.categories.add(cls.category)

    def setUp(self):
        self.client = Client()
        self.client.login(username='testuser', password='password')

    def test_authenticated_search_view(self):
        response = self.client.get(reverse('recipes:search'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_detail_view(self):
        recipe = Recipe.objects.first()
        response = self.client.get(reverse('recipes:recipe_detail', args=[recipe.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, recipe.name)


# Test URLs
class RecipeURLTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='password')
        cls.recipe = Recipe.objects.create(
            name="Lemonade",
            cooking_time=10,
            ingredients="Lemon, sugar, water"
        )

    def test_home_url(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse("recipes:home"))
        self.assertEqual(response.status_code, 200)

    def test_recipe_list_url(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse("recipes:recipe_list"))
        self.assertEqual(response.status_code, 200)

    def test_recipe_detail_url(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse("recipes:recipe_detail", args=[self.recipe.pk]))
        self.assertEqual(response.status_code, 200)

    def test_invalid_recipe_detail_url(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse("recipes:recipe_detail", args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_login_redirect_for_protected_views(self):
        self.client.logout()
        response = self.client.get(reverse('recipes:search'))
        self.assertRedirects(response, '/login/?next=/recipes/search/')
