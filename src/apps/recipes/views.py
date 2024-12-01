from django.shortcuts import render, get_object_or_404
from .models import Recipe  # Import the Recipe model

def home(request):
    return render(request, 'recipes/recipes_home.html')

def recipe_list(request):
    # Fetch all recipes from the database
    recipes = Recipe.objects.all()
    return render(request, 'recipes/recipes_list.html', {'recipes': recipes})

def recipe_detail(request, pk):
    # Fetch a specific recipe using its primary key
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})
