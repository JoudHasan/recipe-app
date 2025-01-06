from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.recipes.models import Recipe
from .forms import SearchForm
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for Matplotlib
import matplotlib.pyplot as plt
import io, base64

## Generate Bar Chart
def generate_bar_chart(data):
    plt.figure(figsize=(10, 6))  # Adjust chart size for better readability

    # Generate bar chart and capture the axes
    ax = data.plot(kind='bar', x='name', y='cooking_time', legend=True)

    # Rotate x-axis labels to prevent text cut-off
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')

    # Set title and labels
    plt.title('Cooking Time Comparison')
    plt.xlabel('Recipes')
    plt.ylabel('Cooking Time (minutes)')

    # Adjust layout to fit everything properly
    plt.tight_layout()

    # Save chart as base64 image
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    chart = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()
    return chart


# Home View
def home(request):
    return render(request, 'recipes/recipes_home.html')

# Recipe List View (with navigation to search)
@login_required
def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipes/recipes_list.html', {'recipes': recipes})

# Search View
@login_required
def search(request):
    form = SearchForm(request.GET or None)
    recipes = Recipe.objects.all()

    if form.is_valid():
        search_term = form.cleaned_data.get('search_term')
        ingredient = form.cleaned_data.get('ingredient')
        difficulty = form.cleaned_data.get('difficulty')
        min_time = form.cleaned_data.get('min_cooking_time')
        max_time = form.cleaned_data.get('max_cooking_time')

        if search_term:
            recipes = recipes.filter(name__icontains=search_term)
        if ingredient:
            recipes = recipes.filter(ingredients__icontains=ingredient)
        if difficulty:
            recipes = [r for r in recipes if r.difficulty == difficulty]
        if min_time:
            recipes = recipes.filter(cooking_time__gte=min_time)
        if max_time:
            recipes = recipes.filter(cooking_time__lte=max_time)

    # Generate Chart
    chart = None
    if recipes.exists():
        data = list(recipes.values('name', 'cooking_time'))
        df = pd.DataFrame(data)
        chart = generate_bar_chart(df)

    return render(request, 'recipes/search.html', {'form': form, 'recipes': recipes, 'chart': chart})

# Recipe Detail View
@login_required
def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})
