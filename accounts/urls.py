from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.userRegistrationView.as_view(),name="register_page"),
    path('login/', views.user_login_view.as_view(),name="login_page"),
    # path('logout/', views.user_logout_view.as_view(),name="logout_page"),
    path('logout/', views.user_logout,name="logout_page"),
    path('profile/', views.UserBankAccountUpdateView.as_view(),name="profile"),
    
]

