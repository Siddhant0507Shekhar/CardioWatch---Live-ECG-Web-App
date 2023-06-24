from django.urls import path
from . import views
urlpatterns = [
    path('receive_data',views.receive_array,name='api_receive'),
    path('get_health_status/<str:date>',views.get_health_status,name="api_get_health"),
    path('get_ecg_image/<str:date>/<str:time>',views.get_ecg_image,name='api_get_ecg'),
    path('get_live_data',views.get_live_data,name='api_live_data')
    # path('signup',views.signup_page,name="home"),
    # path('logout',views.logout_page,name="logout")
]