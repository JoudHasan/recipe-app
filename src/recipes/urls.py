from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('recipes.urls', namespace='recipes')),  # The namespace is tied to the app_name
]
