from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard_index, name='dashboard_index'),
    path('dashboard/accounts/create/', views.AccountCreate.as_view(), name='account_create'),
    path('dashboard/accounts/', views.account_dashboard, name='account_dashboard'),
    path('dashboard/accounts/<int:pk>/update/', views.AccountUpdate.as_view(), name='account_update'),
    path('dashboard/accounts/<int:pk>/delete/', views.AccountDelete.as_view(), name='account_delete'),
    path('topics/', views.topics_index, name='topics_index'),
]