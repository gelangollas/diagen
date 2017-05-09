from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.diagen_main, name='diagen_main'),
    url(r'^get-diagram$', views.get_diagram, name='get_diagram'),
    url(r'^generate-diagram$', views.generate_diagram, name='generate_diagram')
]