from cert_center.models import CertificationCenter, CertRequirement


def create_cert_center(name):
    return CertificationCenter.objects.create(name=name)


def create_cert_requirement(name, center=None):
    if not center:
        center = create_cert_center('TEST CENTER FOR ' + name)
    return CertRequirement.objects.create(name=name, center=center)