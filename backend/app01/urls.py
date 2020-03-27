from django.urls import path
from app01 import views


urlpatterns = [
    path('login', views.AuthLogin.as_view()),
    path('verify', views.TokenVerify.as_view()),
    path('users', views.Users.as_view()),
    path('menu', views.Menu.as_view()),
    path('users/<int:id>/state/<type>',views.SetState.as_view()),
    path('users/<username>', views.UpdateUsers.as_view()),
]