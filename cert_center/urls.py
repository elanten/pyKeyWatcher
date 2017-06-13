from django.conf.urls import url
from . import views

app_name = 'cert_center'
urlpatterns = [
    url(r'^show/(?P<pk>\d+)$', views.show_by_id, name='show_by_id'),
    url(r'^show_req/(?P<pk>\d+)$', views.show_req_by_id, name='show_req_by_id'),
    url(r'^all$', views.show_all, name='all'),
]
