# ide/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import submit_problem, problem_list # Import views correctly

urlpatterns = [
    path('', views.index, name='home'),
    path('submit_code/', views.submit_code, name='submit_code'),
    path('user-management/', views.user_management, name='user_management'),  # Correct view function name
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),  # Ensure you have a register view and template
    path('problems/', views.problem_list, name='problem_list'),
    path('submit/', views.submit_problem, name='submit_problem'),
    path('problem-list/', views.problem_list, name='problem_list'),
    path('problems/create/', views.create_problem, name='create_problem'),
    path('problems/<int:pk>/update/', views.update_problem, name='update_problem'),
    path('problems/<int:pk>/delete/', views.delete_problem, name='delete_problem'),
    path('problems/<int:problem_id>/', views.problem_detail, name='problem_detail'),
    path('submit_code/', views.submit_code, name='submit_code'),
]
