from django.urls import path
from .views import LoginView, RegisterView, ChangePasswordView, LogoutView

app_name = "accounts"

urlpatterns = [
    path('login/', LoginView.as_view(), name= 'login'),
    path('logout/', LogoutView.as_view(), name=  'logout'),
    path('register/', RegisterView.as_view(), name= 'register'),
    path('changepassword/', ChangePasswordView.as_view(), name= 'changepassword'),
]
