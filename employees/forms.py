from django import forms
from django.contrib.auth.models import User
from .models import Employee, UserProfile

class SignUpForm(forms.Form):
    name = forms.CharField(max_length=100)
    emp_id = forms.CharField(max_length=20)
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        username = cleaned_data.get('username')
        emp_id = cleaned_data.get('emp_id')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match!")

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists!")
            
        if UserProfile.objects.filter(emp_id=emp_id).exists():
            raise forms.ValidationError("Employee ID already exists!")

        return cleaned_data

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['employee_id', 'name', 'department', 'position', 'salary', 'email', 'hire_date']
        widgets = {
            'hire_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'salary': forms.NumberInput(attrs={
                'step': '0.01',
                'class': 'form-control'
            }),
            'employee_id': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean_employee_id(self):
        employee_id = self.cleaned_data.get('employee_id')
        if employee_id:
            # Check if employee_id exists, excluding current instance in case of update
            if self.instance.pk:
                if Employee.objects.exclude(pk=self.instance.pk).filter(employee_id=employee_id).exists():
                    raise forms.ValidationError("This Employee ID is already in use.")
            else:
                if Employee.objects.filter(employee_id=employee_id).exists():
                    raise forms.ValidationError("This Employee ID is already in use.")
        return employee_id

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            # Check if email exists, excluding current instance in case of update
            if self.instance.pk:
                if Employee.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
                    raise forms.ValidationError("This email is already in use.")
            else:
                if Employee.objects.filter(email=email).exists():
                    raise forms.ValidationError("This email is already in use.")
        return email