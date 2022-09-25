
from django.urls import path

from .views import RegisterView, ProfileView, ChangeProfileView, ChangePasswordView, logout_view, login_view

app_name = "accounts"

urlpatterns = [
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('registration/', RegisterView.as_view(), name="registration"),
    path('<int:pk>/', ProfileView.as_view(), name="profile"),
    path('<int:pk>/change/', ChangeProfileView.as_view(), name="change_profile"),
    path('change/password/', ChangePasswordView.as_view(), name="change_password"),
]
