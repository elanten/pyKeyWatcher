from django.shortcuts import render, get_object_or_404

# Create your views here.
from cert_center.models import CertificationCenter, CertRequirements
from digital_key.models import DigitalKey


class KeyWrapper:
    def __init__(self, key: DigitalKey):
        self.key = key

    def get_label_class(self):
        delta = self.key.days_before_renewal()
        if delta < 14:
            return 'danger'
        elif delta < 30:
            return 'warning'
        else:
            return 'success'


def show_by_id(request, pk):
    cert_center = get_object_or_404(CertificationCenter, pk=pk)
    requirements = cert_center.certrequirements_set.all()
    keys = cert_center.digitalkey_set.all()
    return render(request, 'cert_center/center_detail.html', {
        'cert_center': cert_center,
        'requirements': requirements,
        'keys': (KeyWrapper(key) for key in keys)
    })


def show_all(request):
    centers = CertificationCenter.objects.all()
    return render(request, 'cert_center/center_list.html', {
        'centers': centers
    })


def show_req_by_id(request, pk):
    requirement = get_object_or_404(CertRequirements, pk=pk)
    return render(request, 'cert_center/req_detail.html', {
        'requirement': requirement
    })
