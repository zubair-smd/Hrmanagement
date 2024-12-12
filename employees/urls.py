from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'employees'

urlpatterns = [
    path('', views.employee_list, name='employee_list'),
    path('create/', views.employee_create_form, name='employee_create_form'),
    path('create/submit/', views.employee_create, name='employee_create'),
    path('<int:pk>/edit/', views.employee_update_form, name='employee_update_form'),
    path('<int:pk>/edit/submit/', views.employee_update, name='employee_update'),
    path('<int:pk>/delete/', views.employee_delete_confirm, name='employee_delete_confirm'),
    path('<int:pk>/delete/submit/', views.employee_delete, name='employee_delete')
]