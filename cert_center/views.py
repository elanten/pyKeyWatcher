from django.shortcuts import render, get_object_or_404

# Create your views here.
from cert_center.models import CertificationCenter, CertRequirement
from digital_key.models import DigitalKey
from digital_key.support import DigitalKeyWrapper


def show_by_id(request, pk):
    cert_center = get_object_or_404(CertificationCenter, pk=pk)
    requirements = cert_center.certrequirement_set.all()
    keys = cert_center.digitalkey_set.all()
    return render(request, 'cert_center/center_detail.html', {
        'cert_center': cert_center,
        'requirements': requirements,
        'keys': (DigitalKeyWrapper(key) for key in keys)
    })


def show_all(request):
    centers = CertificationCenter.objects.all()
    return render(request, 'cert_center/center_list.html', {
        'centers': centers
    })


def show_req_by_id(request, pk):
    requirement = get_object_or_404(CertRequirement, pk=pk)
    return render(request, 'cert_center/req_detail.html', {
        'requirement': requirement
    })
