from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.recipes.models import Recipe
from .forms import SearchForm, RecipeForm
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io, base64

# Chart Generation Functions
def generate_bar_chart(data):
    plt.figure(figsize=(10, 6))
    ax = data.plot(kind='bar', x='name', y='cooking_time', legend=True)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    plt.title('Cooking Time Comparison')
    plt.xlabel('Recipes')
    plt.ylabel('Cooking Time (minutes)')
    plt.tight_layout()
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    chart = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()
    return chart

def generate_line_chart(data):
    plt.figure(figsize=(10, 6))
    data.plot(kind='line', x='name', y='cooking_time', marker='o', legend=False)
    plt.title('Cooking Time Comparison (Line)')
    plt.xlabel('Recipe')
    plt.ylabel('Cooking Time (minutes)')
    plt.tight_layout()
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    chart = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()
    return chart

def generate_pie_chart(data):
    plt.figure(figsize=(8, 8))
    plt.pie(data['cooking_time'], labels=data['name'], autopct='%1.1f%%', startangle=140)
    plt.title('Cooking Time Distribution (Pie)')
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    chart = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()
    return chart

# Views
def home(request):
    return render(request, 'recipes/recipes_home.html')

@login_required
def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipes/recipes_list.html', {'recipes': recipes})

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
        if min_time:
            recipes = recipes.filter(cooking_time__gte=min_time)
        if max_time:
            recipes = recipes.filter(cooking_time__lte=max_time)
        if difficulty:
            recipes = [recipe for recipe in recipes if recipe.difficulty == difficulty]

    bar_chart = line_chart = pie_chart = None
    if recipes:
        data = [{'name': r.name, 'cooking_time': r.cooking_time} for r in recipes]
        df = pd.DataFrame(data)
        if not df.empty:
            bar_chart = generate_bar_chart(df)
            line_chart = generate_line_chart(df)
            pie_chart = generate_pie_chart(df)

    return render(request, 'recipes/search.html', {
        'form': form,
        'recipes': recipes,
        'bar_chart': bar_chart,
        'line_chart': line_chart,
        'pie_chart': pie_chart,
    })

@login_required
def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})

@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('recipes:recipe_list')
    else:
        form = RecipeForm()
    return render(request, 'recipes/add_recipe.html', {'form': form})
