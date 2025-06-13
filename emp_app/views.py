from django.shortcuts import render,redirect,get_object_or_404
from .models import Employee, Department, Role
from datetime import datetime
from django import http
from django.http import HttpResponseRedirect, HttpResponse
import csv
from django.db.models import Q
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    """
    Render the home page of the employee application.
    """
    return render(request, 'index.html')  # Ensure this template exists in your templates directory

def All_Employees(request):

    """Render a page displaying all employees.
    """
    # Here you would typically fetch employee data from the database

    emps = Employee.objects.all()  
    context = {'emps': emps}
    return render(request, 'all_Employees.html', context)  # Ensure this template exists in your templates directory
    
    

def Add_Employee(request):
    """Render a page to add a new employee or handle form submission."""
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        department_id = request.POST.get('dept')  # should be ID
        role_id = request.POST.get('role')        # should be ID
        hire_date = request.POST.get('hire_date')

        try:
            department = Department.objects.get(id=department_id)
            role = Role.objects.get(id=role_id)
        except (Department.DoesNotExist, Role.DoesNotExist):
            return HttpResponse("Invalid department or role selected.", status=400)

        new_emp = Employee.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            dept=department,
            role=role,
            hire_date=datetime.strptime(hire_date, '%Y-%m-%d') if hire_date else None
        )
        return redirect('all_Employee')  # Replace with your actual URL name

    elif request.method == 'GET':
        roles = Role.objects.all()
        departments = Department.objects.all()
        return render(request, 'add_Employee.html', {
            'roles': roles,
            'departments': departments
        })

    else:
        return HttpResponse("Method not allowed", status=405)

def Employee_details(request, employee_id):
    employee = get_object_or_404(Employee, Id=employee_id)
    return render(request, 'employee_details.html', {'employee': employee})



def Filter_Employee(request):

    """Render a page to filter employees.
    """
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        dept = request.POST.get('dept')
        role = request.POST.get('role')
        emps = Employee.objects.all()
        if first_name:
            emps = emps.filter(first_name__icontains=first_name) | Q(last_name__icontains=first_name)
        if dept:
            emps = emps.filter(dept__name__icontains=dept)    
        if role:
            emps = emps.filter(role__name__icontains=role)
        context = {'emps': emps}
        return render(request, 'filter_Employee.html', context)  # Ensure this template exists in your templates directory    
    elif request.method == 'GET':
        return render(request, 'filter_Employee.html', {'emps': Employee.objects.all()})  # Ensure this template exists in your templates directory
  
    else:
        return HttpResponse("Method not allowed", status=405)

def remove_employee_page(request):
    """Render the remove employee dropdown page."""
    emps = Employee.objects.all()
    return render(request, 'remove_Employee.html', {'emps': emps})

def remove_employee(request, emp_id):
    """Delete an employee by their ID and redirect to the remove page."""
    emp = get_object_or_404(Employee, Id=emp_id)
    emp.delete()
    return redirect('all_Employee')  # Redirect back to the dropdown page


def upload_csv(request):
    message = ''
    if request.method == 'POST':
        csv_file = request.FILES.get('csv_file')
        if not csv_file or not csv_file.name.endswith('.csv'):
            message = "Invalid file format. Please upload a .csv file."
        else:
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            for row in reader:
                try:
                    dept, _ = Department.objects.get_or_create(name=row['dept'].strip())
                    role, _ = Role.objects.get_or_create(name=row['role'].strip())

                    Employee.objects.create(
                        first_name=row['first_name'].strip(),
                        last_name=row['last_name'].strip(),
                        email=row['email'].strip(),
                        phone=int(row['phone']),  # ✅ Fix here
                        salary=int(row['salary']),  # ✅ Fix here
                        bonus=int(row['bonus']),  # ✅ Fix here
                        dept=dept,
                        role=role,
                        hire_date=datetime.strptime(row['hire_date'], "%Y-%m-%d").date() if row['hire_date'] else None
                    )
                except Exception as e:
                    message += f"Error in row: {row}. Error: {str(e)}\n"

            if not message:
                message = "CSV uploaded and employees saved successfully."

    return render(request, 'upload_csv.html', {'message': message})
    

def create_superuser(request):
    username = "admin"
    email = "admin@example.com"
    password = "AdminPassword123"

    if User.objects.filter(username=username).exists():
        return HttpResponse("Superuser already exists.")
    
    User.objects.create_superuser(username=username, email=email, password=password)
    return HttpResponse(f"Superuser '{username}' created successfully with password '{password}'.")
