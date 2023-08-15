from django.urls import path
from . import views

# URLs for https connection
urlpatterns = [
    path("", views.index, name="home"),
    path('process_image/', views.process_image, name='process_image')
]