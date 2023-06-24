from django.urls import path
from . import views
urlpatterns = [
    path('LiveEcg',views.LiveEcg_page,name="LiveEcg"),
]