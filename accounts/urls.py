from django.urls import path
from . import views

urlpatterns = [
    path('signout/', views.signout, name='signout'),
    path('account/', views.account, name='account'),
    path('account/signin/', views.signin, name='signin'),
    path('account/signup/', views.signup, name='signup'),
]
