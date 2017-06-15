from django.conf.urls import url
from . import views

app_name = 'key_manual'

urlpatterns = [
    url(r'^all$', views.show_all, name='all'),
    url(r'^show/(?P<pk>\d+)$', views.show_by_id, name='show_by_id'),
    url(r'^get/(?P<pk>\d+)$', views.get_by_id, name='get_by_id')
]
