from django.conf.urls import url
from . import views
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^new/$', views.new, name='new'),
    url(r'^create/$', views.create, name='create'),
    url(r'^(?P<objId>\d+)/$', views.show, name='show'),
    url(r'^(?P<objId>\d+)/edit/$', views.edit, name='edit'),
    url(r'^(?P<objId>\d+)/update/$', views.update, name='update'),
    url(r'^(?P<objId>\d+)/destroy/$', views.destroy, name='destroy'),
    url(r'^(?P<objId>\d+)/like/$', views.create_like, name='create_like'),
]
