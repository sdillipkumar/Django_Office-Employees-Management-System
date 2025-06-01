import os
import pytest
from django.utils import timezone
from emp_app.models import Department, Role, Employee

@pytest.mark.django_db
def test_department_str():
    dept = Department.objects.create(name="Engineering")
    assert str(dept) == "Engineering"

@pytest.mark.django_db
def test_role_str():
    role = Role.objects.create(name="Python Developer")
    assert str(role) == "Python Developer"

@pytest.mark.django_db
def test_create_employee_and_fields():
    # Create related Department and Role
    dept = Department.objects.create(name="Engineering")
    role = Role.objects.create(name="Python Developer")

    # Create an Employee instance
    emp = Employee.objects.create(
        first_name="John",
        last_name="Doe",
        dept=dept,
        salary=55000,
        bonus=5000,
        role=role,
        phone=9876543210,
        email="john.doe@example.com",
        hire_date=timezone.now().date(),
    )

    # Fetch it back and assert values
    fetched = Employee.objects.get(pk=emp.Id)
    assert fetched.first_name == "John"
    assert fetched.last_name == "Doe"
    assert fetched.dept.name == "Engineering"
    assert fetched.role.name == "Python Developer"
    assert fetched.salary == 55000
    assert fetched.bonus == 5000
    assert fetched.phone == 9876543210
    assert fetched.email == "john.doe@example.com"
    assert fetched.hire_date == emp.hire_date

@pytest.mark.django_db
def test_employee_str_without_last_name():
    dept = Department.objects.create(name="HR")
    role = Role.objects.create(name="HR Manager")

    # last_name is blank
    emp = Employee.objects.create(
        first_name="Alice",
        last_name="",
        dept=dept,
        salary=45000,
        bonus=3000,
        role=role,
        phone=9123456780,
        email="alice@example.com",
        hire_date=timezone.now().date(),
    )
    assert str(emp) == "Alice"
