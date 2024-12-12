from django.contrib.auth.views import LoginView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from django.db import transaction
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .models import Employee, UserProfile
from .forms import EmployeeForm, SignUpForm
import logging

logger = logging.getLogger(__name__)

def signup(request):
    """View to handle user signup."""
    if request.user.is_authenticated:
        return redirect('employees:employee_list')
        
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Create User
                    user = User.objects.create_user(
                        username=form.cleaned_data['username'],
                        password=form.cleaned_data['password']
                    )
                    
                    # Create UserProfile
                    UserProfile.objects.create(
                        user=user,
                        name=form.cleaned_data['name'],
                        emp_id=form.cleaned_data['emp_id']
                    )
                    
                    messages.success(request, 'Account created successfully. Please login.')
                    return redirect('employees:login')
            except Exception as e:
                logger.error(f"Error in signup: {str(e)}")
                messages.error(request, 'Error creating account. Please try again.')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = SignUpForm()
    
    return render(request, 'employees/signup.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'employees/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('employees:employee_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        try:
            UserProfile.objects.get(user=self.request.user)
        except UserProfile.DoesNotExist:
            # Create a default UserProfile for the user
            UserProfile.objects.create(
                user=self.request.user,
                name=self.request.user.username,
                emp_id=f"EMP{self.request.user.id:03d}"
            )
        return response

@login_required
def employee_list(request):
    """View to display list of employees."""
    try:
        employees = Employee.objects.all().order_by('-created_at')
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            user_profile = UserProfile.objects.create(
                user=request.user,
                name=request.user.username,
                emp_id=f"EMP{request.user.id:03d}"
            )
        
        context = {
            'employees': employees,
            'user_profile': user_profile
        }
        return render(request, 'employees/employee_list.html', context)
    except Exception as e:
        logger.error(f"Error fetching employee list: {str(e)}")
        messages.error(request, 'Error fetching employee list.')
        return redirect('employees:login')

@login_required
def employee_detail(request, pk):
    """View to display detailed employee information."""
    try:
        employee = get_object_or_404(Employee, pk=pk)
        user_profile = get_object_or_404(UserProfile, user=request.user)
        return render(request, 'employees/employee_detail.html', {
            'employee': employee,
            'user_profile': user_profile
        })
    except Exception as e:
        logger.error(f"Error displaying employee details: {str(e)}")
        messages.error(request, 'Error displaying employee details.')
        return redirect('employees:employee_list')

@login_required
def employee_create_form(request):
    """View to display employee creation form."""
    try:
        form = EmployeeForm()
        user_profile = get_object_or_404(UserProfile, user=request.user)
        return render(request, 'employees/employee_form.html', {
            'form': form,
            'action': 'Add',
            'user_profile': user_profile
        })
    except Exception as e:
        logger.error(f"Error displaying create form: {str(e)}")
        messages.error(request, 'Error displaying create form.')
        return redirect('employees:employee_list')

@login_required
@require_POST
def employee_create(request):
    """View to handle employee creation."""
    try:
        form = EmployeeForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                employee = form.save(commit=False)
                employee.created_by = request.user
                employee.save()
                messages.success(request, 'Employee created successfully.')
                return redirect('employees:employee_list')
        else:
            user_profile = get_object_or_404(UserProfile, user=request.user)
            return render(request, 'employees/employee_form.html', {
                'form': form,
                'action': 'Add',
                'user_profile': user_profile
            })
    except Exception as e:
        logger.error(f"Error creating employee: {str(e)}")
        messages.error(request, 'Error creating employee.')
        return redirect('employees:employee_list')

@login_required
def employee_update_form(request, pk):
    """View to display employee update form."""
    try:
        employee = get_object_or_404(Employee, pk=pk)
        form = EmployeeForm(instance=employee)
        user_profile = get_object_or_404(UserProfile, user=request.user)
        return render(request, 'employees/employee_form.html', {
            'form': form,
            'employee': employee,
            'action': 'Update',
            'user_profile': user_profile
        })
    except Exception as e:
        logger.error(f"Error displaying update form: {str(e)}")
        messages.error(request, 'Error displaying update form.')
        return redirect('employees:employee_list')

@login_required
@require_POST
def employee_update(request, pk):
    """View to handle employee update."""
    try:
        employee = get_object_or_404(Employee, pk=pk)
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            with transaction.atomic():
                employee = form.save(commit=False)
                employee.updated_by = request.user
                employee.save()
                messages.success(request, 'Employee updated successfully.')
                return redirect('employees:employee_list')
        else:
            user_profile = get_object_or_404(UserProfile, user=request.user)
            return render(request, 'employees/employee_form.html', {
                'form': form,
                'employee': employee,
                'action': 'Update',
                'user_profile': user_profile
            })
    except Exception as e:
        logger.error(f"Error updating employee: {str(e)}")
        messages.error(request, 'Error updating employee.')
        return redirect('employees:employee_list')

@login_required
def employee_delete_confirm(request, pk):
    """View to display delete confirmation page."""
    try:
        employee = get_object_or_404(Employee, pk=pk)
        user_profile = get_object_or_404(UserProfile, user=request.user)
        return render(request, 'employees/employee_confirm_delete.html', {
            'employee': employee,
            'user_profile': user_profile
        })
    except Exception as e:
        logger.error(f"Error displaying delete confirmation: {str(e)}")
        messages.error(request, 'Error displaying delete confirmation.')
        return redirect('employees:employee_list')

@login_required
@require_POST
def employee_delete(request, pk):
    """View to handle employee deletion."""
    try:
        employee = get_object_or_404(Employee, pk=pk)
        with transaction.atomic():
            employee.delete()
            messages.success(request, 'Employee deleted successfully.')
            return redirect('employees:employee_list')
    except Exception as e:
        logger.error(f"Error deleting employee: {str(e)}")
        messages.error(request, 'Error deleting employee.')
        return redirect('employees:employee_list')