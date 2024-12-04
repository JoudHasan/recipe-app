from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required  # For FBV authentication
from .models import Recipe  # Import the Recipe model

# Function-Based Views (FBVs)
def home(request):
    """Render the homepage."""
    return render(request, 'recipes/recipes_home.html')

# Protect recipe_list with @login_required
@login_required
def recipe_list(request):
    """Render the list of recipes."""
    # Fetch all recipes from the database
    recipes = Recipe.objects.all()
    return render(request, 'recipes/recipes_list.html', {'recipes': recipes})

# Protect recipe_detail with @login_required
@login_required
def recipe_detail(request, pk):
    """Render details of a specific recipe."""
    # Fetch a specific recipe using its primary key
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})
