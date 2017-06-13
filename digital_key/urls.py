from django.conf.urls import url

from . import views

app_name = 'digital_key'
urlpatterns = [
    url(r'^$', views.show_all, name='all'),
    url(r'^show/(?P<key_id>[0-9]+)$', views.show_by_id, name='show_by_id'),
    url(r'^edit/(?P<key_id>[0-9]+)$', views.edit_by_id, name='edit_by_id'),
    url(r'^remove/(?P<key_id>[0-9]+)$', views.remove_by_id, name='remove_by_id'),
    url(r'^add$', views.create, name='add'),
]