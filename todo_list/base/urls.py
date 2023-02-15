from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_page, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('create_task/', views.create_task, name='create'),
    path('delete_task/<int:task_id>', views.delete_task, name='delete'),
    path('is_done/<int:task_id>', views.is_done, name='done'),
    path('update/<int:task_id>', views.update_task, name='update'),
    path('view/<int:task_id>', views.view_task, name='view'),
]
