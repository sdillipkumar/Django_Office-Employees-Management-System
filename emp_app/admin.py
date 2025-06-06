from django.contrib import admin
from emp_app.models import *
# Register your models here.
"""Registering the models with the Django admin site allows for easy management of these models through "
"the admin interface."""
admin.site.register(Department)
admin.site.register(Role)
admin.site.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'dept', 'role', 'phone', 'email', 'hire_date')
