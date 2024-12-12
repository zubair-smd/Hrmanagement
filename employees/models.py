# employees/models.py
from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    hire_date = models.DateField()
    email = models.EmailField(default='noreply@company.com', null=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']