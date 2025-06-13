from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
# This file is part of the office_emp_proj project.
from. import views
from .views import insert_dummy_employees

urlpatterns = [
    path('', views.index, name='index'),  # Home page
    path('all_Employee', views.All_Employees, name='all_Employee'),  # View all employees
    path('employee/<int:employee_id>/', views.Employee_details, name='employee_details'),
    path('add_Employee', views.Add_Employee, name='add_Employee'),  # Add a new employee
    path('upload_csv/', views.upload_csv, name='upload_csv'),
    path('filter_Employee', views.Filter_Employee, name='filter_Employee'),  # Filter employees
    path('remove_Employee/', views.remove_employee_page, name='remove_employee_page'),
    path('remove_Employee/<int:emp_id>/', views.remove_employee, name='remove_employee'),
    path('insert-dummy-employees/', insert_dummy_employees),
    
    
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
