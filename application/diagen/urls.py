from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.diagen_main, name='diagen_main'),
    url(r'^get-diagram$', views.get_diagram, name='get_diagram'),
    url(r'^generate-diagram$', views.generate_diagram, name='generate_diagram'),
    url(r'^login$', views.autentificate_user, name='autentificate_user'),
    url(r'^load_user_data$', views.load_user_data, name='load_user_data'),
    url(r'^load_user_diagram$', views.load_user_diagram, name='load_user_diagram'),
    url(r'^logout_user$', views.logout_user, name="logout_user"),
    url(r'^registrate_user$', views.registrate_user, name="registrate_user"),
    url(r'^save_diagram_for_user$', views.save_diagram_for_user, name="save_diagram_for_user"),  
    url(r'^delete_user_diagram$', views.delete_user_diagram, name="delete_user_diagram")      
]