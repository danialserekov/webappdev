from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),
    path('', views.profiles, name='profiles'),
    path('profile/<str:pk>/', views.profilePage, name='profile-page'),
    path('account/', views.UserAccount, name='account'),
    path('account/edit/', views.editAccount, name='edit-account'),
    path('account/add-interest', views.addInterest, name='add-interest'),
    path('account/update-interest/<uuid:pk>/', views.updateInterest, name='update-interest'),
    path('account/delete-interest/<uuid:pk>/', views.deleteInterest, name='delete-interest'),
    path('inbox/', views.inbox, name='inbox'),
    path('inbox/message/<str:pk>/', views.viewMessage, name='message'),
]