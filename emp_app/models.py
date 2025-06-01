from django.db import models

# Create your models here.
class Department(models.Model):
    """Model representing a department in the company.
    """
    name = models.CharField(max_length=100, null=False)
    location = models.CharField(max_length=100)


    def __str__(self):
        return self.name
class Role(models.Model):
    """Model representing a role in the company.
    """
    name = models.CharField(max_length=100, null=False)
 

    def __str__(self):
        return self.name    
    
class Employee(models.Model):
    """Model representing an employee in the company.
    """
    Id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100)
    dept = models.ForeignKey(Department, on_delete=models.CASCADE)
    salary = models.PositiveIntegerField()
    bonus = models.PositiveIntegerField()
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    phone = models.BigIntegerField()
    email = models.EmailField(max_length=254, null=True, blank=True)
    hire_date = models.DateField(null=True, blank=True)

    def __str__(self):
        # Only return first_name if last_name is empty/blank
        if not self.last_name:
            return self.first_name
        return f"{self.first_name} {self.last_name}"
