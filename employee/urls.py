from django.conf.urls import url

from . import views

app_name = 'employee'
urlpatterns = [
    url(r'^$', views.EmployeeListView.as_view(), name='all'),
    url(r'^show/(?P<cid>[0-9]+)$', views.show_by_id, name='show_by_id'),
    url(r'^show_group/(?P<pk>\d+)$', views.show_group_by_id, name='group_detail'),
    url(r'^json/search$', views.show_all_by_name, name='json_by_name'),
    url(r'^edit/(?P<cid>[0-9]+)$', views.edit_by_id, name='edit_by_id'),
    url(r'^add$', views.create, name='add'),
    url(r'^remove/(?P<cid>[0-9]+)$', views.remove_by_id, name='remove'),

    url(r'^group/all$', views.EmployeeGroupsList.as_view(), name='group_all')

]