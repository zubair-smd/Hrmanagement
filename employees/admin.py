from django.contrib import admin
from .models import Employee, UserProfile

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'name', 'department', 'position', 'salary', 'hire_date', 'email')
    search_fields = ('employee_id', 'name', 'email')
    list_filter = ('department', 'position')
    ordering = ('name',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'emp_id')
    search_fields = ('name', 'emp_id')
    ordering = ('name',)