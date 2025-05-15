from django.urls import path  
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('user/list/', views.user_list, name='user_list'),
    path('user/add/', views.user_add, name='user_add'),
    path('user/edit/<int:user_id>/', views.user_edit, name='user_edit'),
    path('user/delete/<int:user_id>/', views.user_delete, name='user_delete'),

]
