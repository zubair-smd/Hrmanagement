from django.contrib.auth.views import LoginView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods, require_POST, require_GET, require_safe
from django.db import transaction
from django.urls import reverse_lazy
from .models import Employee
from .forms import EmployeeForm
from .constants import EmployeeConstants as EC
import logging

logger = logging.getLogger(__name__)

class CustomLoginView(LoginView):
   template_name = 'employees/login.html'
   redirect_authenticated_user = True

   def get_success_url(self):
       return reverse_lazy('employees:employee_list')

@login_required
@require_safe
def employee_list(request):
   """View to display list of employees."""
   try:
       employees = Employee.objects.all().order_by('name')
       return render(request, EC.TEMPLATE_LIST, {'employees': employees})
   except Exception as e:
       logger.error(f"Error fetching employee list: {str(e)}")
       messages.error(request, EC.MSG_FETCH_ERROR)
       return redirect(EC.URL_EMPLOYEE_LIST)

@login_required
@require_GET
def employee_create_form(request):
   """View to display the employee creation form."""
   try:
       form = EmployeeForm()
       return render(request, EC.TEMPLATE_FORM, {
           'form': form,
           'action': EC.ACTION_ADD
       })
   except Exception as e:
       logger.error(f"Error displaying employee creation form: {str(e)}")
       messages.error(request, EC.MSG_FORM_DISPLAY_ERROR)
       return redirect(EC.URL_EMPLOYEE_LIST)

@login_required
@require_POST
def employee_create(request):
   """View to handle employee creation form submission."""
   try:
       form = EmployeeForm(request.POST)
       if form.is_valid():
           with transaction.atomic():
               employee = form.save(commit=False)
               employee.created_by = request.user
               employee.save()
               messages.success(request, EC.MSG_CREATE_SUCCESS)
               return redirect(EC.URL_EMPLOYEE_LIST)
       else:
           messages.error(request, EC.MSG_FORM_ERRORS)
           return render(request, EC.TEMPLATE_FORM, {
               'form': form,
               'action': EC.ACTION_ADD
           })
   except Exception as e:
       logger.error(f"Error creating employee: {str(e)}")
       messages.error(request, EC.MSG_CREATE_ERROR)
       return redirect(EC.URL_EMPLOYEE_LIST)

@login_required
@require_GET
def employee_update_form(request, pk):
   """View to display the employee update form."""
   try:
       employee = get_object_or_404(Employee, pk=pk)
       form = EmployeeForm(instance=employee)
       return render(request, EC.TEMPLATE_FORM, {
           'form': form,
           'employee': employee,
           'action': EC.ACTION_UPDATE
       })
   except Employee.DoesNotExist:
       messages.error(request, EC.MSG_NOT_FOUND)
       return redirect(EC.URL_EMPLOYEE_LIST)
   except Exception as e:
       logger.error(f"Error displaying update form for employee {pk}: {str(e)}")
       messages.error(request, EC.MSG_UPDATE_FORM_ERROR)
       return redirect(EC.URL_EMPLOYEE_LIST)

@login_required
@require_POST
def employee_update(request, pk):
   """View to handle employee update form submission."""
   try:
       employee = get_object_or_404(Employee, pk=pk)
       form = EmployeeForm(request.POST, instance=employee)
       if form.is_valid():
           with transaction.atomic():
               employee = form.save(commit=False)
               employee.updated_by = request.user
               employee.save()
               messages.success(request, EC.MSG_UPDATE_SUCCESS)
               return redirect(EC.URL_EMPLOYEE_LIST)
       else:
           messages.error(request, EC.MSG_FORM_ERRORS)
           return render(request, EC.TEMPLATE_FORM, {
               'form': form,
               'employee': employee,
               'action': EC.ACTION_UPDATE
           })
   except Employee.DoesNotExist:
       messages.error(request, EC.MSG_NOT_FOUND)
       return redirect(EC.URL_EMPLOYEE_LIST)
   except Exception as e:
       logger.error(f"Error updating employee {pk}: {str(e)}")
       messages.error(request, EC.MSG_UPDATE_ERROR)
       return redirect(EC.URL_EMPLOYEE_LIST)

@login_required
@require_GET
def employee_delete_confirm(request, pk):
   """View to display delete confirmation page."""
   try:
       employee = get_object_or_404(Employee, pk=pk)
       return render(request, EC.TEMPLATE_DELETE, {
           'employee': employee
       })
   except Employee.DoesNotExist:
       messages.error(request, EC.MSG_NOT_FOUND)
       return redirect(EC.URL_EMPLOYEE_LIST)
   except Exception as e:
       logger.error(f"Error displaying delete confirmation for employee {pk}: {str(e)}")
       messages.error(request, EC.MSG_DELETE_CONFIRM_ERROR)
       return redirect(EC.URL_EMPLOYEE_LIST)

@login_required
@require_POST
def employee_delete(request, pk):
   """View to handle employee deletion."""
   try:
       employee = get_object_or_404(Employee, pk=pk)
       with transaction.atomic():
           employee.delete()
           messages.success(request, EC.MSG_DELETE_SUCCESS)
           return redirect(EC.URL_EMPLOYEE_LIST)
   except Employee.DoesNotExist:
       messages.error(request, EC.MSG_NOT_FOUND)
       return redirect(EC.URL_EMPLOYEE_LIST)
   except Exception as e:
       logger.error(f"Error deleting employee {pk}: {str(e)}")
       messages.error(request, EC.MSG_DELETE_ERROR)
       return redirect(EC.URL_EMPLOYEE_LIST)