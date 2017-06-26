from employee.models import Employee, EmployeeGroup


def create_employee(name):
    return Employee.objects.create(name=name)


def create_group(name):
    return EmployeeGroup.objects.create(name=name)