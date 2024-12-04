from django.shortcuts import render, redirect

# django authentication libraries
from django.contrib.auth import authenticate, login, logout

# django form authentication
from django.contrib.auth.forms import AuthenticationForm

from django.contrib import messages

# define function that takes request from user
def login_view(request):
    # initialize error message to none
    error_message = None
    # form object with username and password fields
    form = AuthenticationForm()

    # POST request generated when user hits login button
    if request.method == "POST":
        # read data sent by form via POST request
        form = AuthenticationForm(data=request.POST)

        # check if form is valid
        if form.is_valid():
            # read form
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            # use Django authenticate to validate user
            user = authenticate(username=username, password=password)
            # if authenticated
            if user is not None:
                # use Django login function to login
                login(request, user)
                return redirect("recipes:recipe_list")  # Adjusted URL name to match folder structure
        # error handling
        else:
            error_message = "Oops...something went wrong"

    context = {
        # send form
        "form": form,
        # send error message
        "error_message": error_message,
    }

    # load the login page using "context" information
    return render(request, "auth/login.html", context)  # Adjusted to match templates/auth/login.html


# define function that takes request from user
def logout_view(request):
    # use predefined Django logout function
    logout(request)
    # navigate user to login form after logging out
    return render(request, "auth/success.html")  # Adjusted to match templates/auth/success.html
