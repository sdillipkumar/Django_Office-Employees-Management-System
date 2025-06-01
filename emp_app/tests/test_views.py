import os
import pytest
from django.urls import reverse
from django.utils import timezone
from emp_app.models import Department, Role, Employee

# Test cases for views in emp_app
@pytest.mark.django_db
def test_filter_employee_view(client):
    # 1) Create sample data
    dept = Department.objects.create(name="Sales")
    role = Role.objects.create(name="Sales Agent")

    emp1 = Employee.objects.create(
        first_name="John", last_name="Doe", dept=dept,
        salary=45000, bonus=3000, role=role,
        phone=9000000001, email="john@example.com",
        hire_date=timezone.now().date()
    )
    emp2 = Employee.objects.create(
        first_name="Jane", last_name="Smith", dept=dept,
        salary=50000, bonus=4000, role=role,
        phone=9000000002, email="jane@example.com",
        hire_date=timezone.now().date()
    )

    url = reverse('filter_Employee')
    response = client.get(url)
    assert response.status_code == 200

    content = response.content.decode()
    # The template should contain these first names
    assert "John" in content
    assert "Jane" in content


@pytest.mark.django_db
def test_employee_details_view_valid(client):
    # 1) Create one employee
    dept = Department.objects.create(name="Engineering")
    role = Role.objects.create(name="Python Developer")

    emp = Employee.objects.create(
        first_name="Alice", last_name="Johnson", dept=dept,
        salary=60000, bonus=5000, role=role,
        phone=9000000003, email="alice@example.com",
        hire_date=timezone.now().date()
    )

    url = reverse('employee_details', args=[emp.Id])
    response = client.get(url)
    assert response.status_code == 200

    content = response.content.decode()
    # The details page should show first_name, last_name, department, role, etc.
    assert "Alice" in content
    assert "Johnson" in content
    assert "Engineering" in content
    assert "Python Developer" in content


@pytest.mark.django_db
def test_employee_details_view_invalid(client):
    # No employee with ID=9999
    url = reverse('employee_details', args=[9999])
    response = client.get(url)
    assert response.status_code == 404


@pytest.mark.django_db
def test_add_employee_invalid_post_data(client):
    """Test submitting incomplete data to Add_Employee view."""
    url = reverse('add_Employee')  # use your actual URL name

    # No data sent (empty form)
    response = client.post(url, data={})

    assert response.status_code == 400
    assert b"Invalid department or role selected" in response.content

@pytest.mark.django_db
def test_add_employee_valid_post_data(client):
    dept = Department.objects.create(name="QA")
    role = Role.objects.create(name="Tester")

    url = reverse('add_Employee')
    response = client.post(url, {
        'first_name': 'Alice',
        'last_name': 'Smith',
        'email': 'alice@example.com',
        'phone': '1234567890',
        'dept': dept.id,
        'role': role.id,
        'hire_date': '2024-06-15',
    })

    assert response.status_code == 302  # Redirect after success
    assert Employee.objects.count() == 1

    emp = Employee.objects.first()
    assert emp.first_name == 'Alice'
    assert emp.role.name == 'Tester'

@pytest.mark.django_db
def test_add_employee_get_method(client):
    url = reverse('add_Employee')
    response = client.get(url)

    assert response.status_code == 200
    assert b"Add" in response.content  # assuming the template has "Add" button or heading
