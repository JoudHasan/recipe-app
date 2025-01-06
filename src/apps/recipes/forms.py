from django import forms
from django.forms import ModelForm, TextInput, NumberInput, FileInput
from .models import Recipe

class SearchForm(forms.Form):
    search_term = forms.CharField(
        required=False,
        label="Search by name",
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter part of a recipe name (e.g., Cake)',
            'class': 'form-control'
        })
    )
    ingredient = forms.CharField(
        required=False,
        label="Search by ingredient",
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter ingredients',
            'class': 'form-control'
        })
    )
    difficulty = forms.ChoiceField(
        choices=[('', 'Any Difficulty'), ('Easy', 'Easy'), ('Medium', 'Medium'), ('Intermediate', 'Intermediate'), ('Hard', 'Hard')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    min_cooking_time = forms.IntegerField(
        required=False,
        label="Minimum cooking time",
        widget=forms.NumberInput(attrs={'placeholder': 'e.g., 10', 'class': 'form-control'})
    )
    max_cooking_time = forms.IntegerField(
        required=False,
        label="Maximum cooking time",
        widget=forms.NumberInput(attrs={'placeholder': 'e.g., 60', 'class': 'form-control'})
    )

class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'ingredients', 'cooking_time', 'pic']
