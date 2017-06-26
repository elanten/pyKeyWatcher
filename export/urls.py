from django.conf.urls import url
from . import views

app_name = 'export'
urlpatterns = [
    url(r'^xlsx$', views.export_key_xlsx, name='xlsx'),
]
