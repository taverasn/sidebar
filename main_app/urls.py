from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('dashboard/accounts/', views.AccountCreate.as_view(), name='account_create'),
    path('dashboard/accounts/<int:account_id>/', views.account_dashboard, name='account_dashboard'),
    path('topics/', views.topics_index, name='topics_index'),
]