from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.build_diagram, name='build_diagram')
]