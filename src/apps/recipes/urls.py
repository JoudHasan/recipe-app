from django.urls import path
from .views import home, recipe_list, search, recipe_detail

app_name = 'recipes'

urlpatterns = [
    path('', home, name="home"),
    path('recipes/', recipe_list, name="recipe_list"),
    path('recipes/search/', search, name="search"),  # Added search URL
    path('recipes/<int:pk>/', recipe_detail, name="recipe_detail"),
]
