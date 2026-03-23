from django.urls import path
from . import views  # importing the views module from this same app
 
urlpatterns = [
 
    # Reporter endpoints
    # Both POST and GET go to the same view function — reporters()
    # Inside views.py, request.method tells us which one it is
    path("api/reporters/", views.reporters),
 
    # Issue endpoints
    # Same pattern — one function handles both POST and GET
    path("api/issues/", views.issues),
 
]