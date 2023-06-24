from django.urls import path
from . import views
urlpatterns = [
    path('login',views.login_page,name="home"),
    path('signup',views.signup_page,name="home"),
    path('logout',views.logout_page,name="logout")
]