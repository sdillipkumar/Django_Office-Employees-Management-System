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
    

def insert_dummy_employees(request):
    if not request.user.is_superuser:
        return HttpResponse("Unauthorized", status=403)

    # Make sure Departments and Roles with given IDs exist (adjust IDs if needed)
    employees = [
        Employee(first_name='Alice', last_name='Johnson', dept_id=1, salary=55000, bonus=5000, role_id=1, phone=9876543210, email='alice.johnson@example.com', hire_date=date(2022, 3, 15)),
        Employee(first_name='Bob', last_name='Smith', dept_id=2, salary=62000, bonus=6000, role_id=2, phone=9876543211, email='bob.smith@example.com', hire_date=date(2021, 7, 1)),
        Employee(first_name='Carol', last_name='Lee', dept_id=1, salary=58000, bonus=4000, role_id=3, phone=9876543212, email='carol.lee@example.com', hire_date=date(2020, 11, 20)),
        Employee(first_name='David', last_name='Kim', dept_id=3, salary=70000, bonus=8000, role_id=4, phone=9876543213, email='david.kim@example.com', hire_date=date(2023, 1, 10)),
        Employee(first_name='Eve', last_name='Turner', dept_id=2, salary=49000, bonus=3500, role_id=1, phone=9876543214, email='eve.turner@example.com', hire_date=date(2022, 9, 1)),
        Employee(first_name='Frank', last_name='Baker', dept_id=1, salary=53000, bonus=3000, role_id=2, phone=9876543215, email='frank.baker@example.com', hire_date=date(2021, 12, 5)),
        Employee(first_name='Grace', last_name='Wong', dept_id=3, salary=61000, bonus=7000, role_id=3, phone=9876543216, email='grace.wong@example.com', hire_date=date(2020, 6, 18)),
        Employee(first_name='Hank', last_name='Patel', dept_id=1, salary=47000, bonus=2000, role_id=4, phone=9876543217, email='hank.patel@example.com', hire_date=date(2023, 2, 14)),
        Employee(first_name='Ivy', last_name='Nguyen', dept_id=2, salary=66000, bonus=6000, role_id=5, phone=9876543218, email='ivy.nguyen@example.com', hire_date=date(2021, 3, 23)),
        Employee(first_name='Jack', last_name='Miller', dept_id=3, salary=50000, bonus=2500, role_id=2, phone=9876543219, email='jack.miller@example.com', hire_date=date(2022, 7, 11)),
        Employee(first_name='Karen', last_name='Diaz', dept_id=1, salary=59000, bonus=4000, role_id=3, phone=9876543220, email='karen.diaz@example.com', hire_date=date(2020, 10, 22)),
        Employee(first_name='Leo', last_name='Choi', dept_id=2, salary=71000, bonus=7500, role_id=1, phone=9876543221, email='leo.choi@example.com', hire_date=date(2023, 5, 3)),
        Employee(first_name='Mia', last_name='Scott', dept_id=3, salary=53000, bonus=3000, role_id=2, phone=9876543222, email='mia.scott@example.com', hire_date=date(2021, 1, 30)),
        Employee(first_name='Nina', last_name='Reed', dept_id=1, salary=56000, bonus=3500, role_id=3, phone=9876543223, email='nina.reed@example.com', hire_date=date(2022, 8, 25)),
        Employee(first_name='Owen', last_name='Frost', dept_id=2, salary=48000, bonus=2000, role_id=4, phone=9876543224, email='owen.frost@example.com', hire_date=date(2020, 12, 19)),
        Employee(first_name='Pam', last_name='Zhao', dept_id=3, salary=62000, bonus=5000, role_id=5, phone=9876543225, email='pam.zhao@example.com', hire_date=date(2021, 11, 9)),
        Employee(first_name='Quinn', last_name='Ali', dept_id=1, salary=60000, bonus=4500, role_id=1, phone=9876543226, email='quinn.ali@example.com', hire_date=date(2023, 3, 17)),
        Employee(first_name='Raj', last_name='Mehta', dept_id=2, salary=55000, bonus=3000, role_id=2, phone=9876543227, email='raj.mehta@example.com', hire_date=date(2021, 6, 6)),
        Employee(first_name='Sara', last_name='Lopez', dept_id=3, salary=64000, bonus=5500, role_id=3, phone=9876543228, email='sara.lopez@example.com', hire_date=date(2020, 9, 29)),
        Employee(first_name='Tom', last_name='Brown', dept_id=1, salary=49000, bonus=2500, role_id=4, phone=9876543229, email='tom.brown@example.com', hire_date=date(2022, 12, 13)),
    ]
    Employee.objects.bulk_create(employees)
    return HttpResponse("20 dummy employees inserted successfully.")
