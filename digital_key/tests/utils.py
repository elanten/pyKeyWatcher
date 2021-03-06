from digital_key.models import DigitalKey, KeyLocation, WorkSystem, KeyAssignment


def create_key(name):
    return DigitalKey.objects.create(name=name)


def create_location(name):
    return KeyLocation.objects.create(name=name)


def create_work_system(name):
    return WorkSystem.objects.create(name=name)


def create_assignment(name):
    return KeyAssignment.objects.create(name=name)
