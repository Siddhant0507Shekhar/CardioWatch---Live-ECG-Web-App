from django.urls import path
from . import views
urlpatterns = [
    path('user_report',views.report_page,name="report"),
    # path('signup',views.signup_page,name="home"),
    # path('logout',views.logout_page,name="logout")
]