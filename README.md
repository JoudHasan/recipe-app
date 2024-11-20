# recipe-app

## Overview

This project focuses on creating a web application using the Django framework. Django is modularized and developer-friendly, while being powerful enough to run some of the world’s most popular websites. This application allows users to sign up, create, and manage their own recipes, with features to calculate recipe difficulty based on cooking time and ingredients. The app will be deployed using Heroku, with a PostgreSQL database at the backend and HTML/CSS rendering for the frontend.

The application will feature multi-user support, dashboards for statistical data, and visualization charts based on recipe data.

## Features

- **User Authentication**: Secure login and user account management.
- **Recipe Management**: Users can create, view, and manage recipes.
- **Difficulty Calculation**: Automatically calculates the difficulty of recipes based on cooking time and ingredients.
- **Search Functionality**: Users can search for recipes by ingredients.
- **Recipe Details**: Display detailed information on each recipe, including ingredients, cooking time, and difficulty.
- **Admin Dashboard**: Django Admin for managing database entries.
- **Charts and Visualizations**: View statistics on recipe data, including trends and analytics.

## Models

### `Category` Model:

The `Category` model organizes recipes into categories (e.g., "Desserts", "Main Courses"). Each category has a `name` field that is a string of up to 255 characters.

### `Recipe` Model:

The `Recipe` model stores information about individual recipes, including name, ingredients, cooking time, and categories. The difficulty of the recipe is calculated dynamically using the `calculate_difficulty` method based on cooking time and ingredients.

## Usage

### Pages

- **Home**: The homepage shows a welcome message and a login button. Clicking "Login" leads to the login form.
- **Recipes**: Displays all available recipes. Clicking a recipe name or image will show detailed information.
- **Details**: Shows a recipe’s details, including ingredients, cooking time, difficulty, and image.
- **About**: Displays developer contact information and links to portfolio, LinkedIn, GitHub, and email.
- **Search**: A search page to look for recipes by ingredients and visualize data trends.
- **Add Recipe**: A form for adding new recipes, including name, ingredients, cooking time, and image. Difficulty is calculated automatically.

## Installation

1. Clone the repository:https://github.com/JoudHasan/recipe-app.git
2. Create and activate a virtual environment
3. Install dependencies
4. Apply database migrations
5. Run the development server
