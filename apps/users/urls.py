from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^login/$', views.show_login, name='disp_login'),
    url(r'^login/process/$', views.login, name='do_login'),
    url(r'^logout/$', views.logout, name='do_logout'),
    url(r'^combined/', views.show_register_login, name='disp_reg_login'),
    url(r'^register/', views.show_register, name='disp_reg'),
    url(r'^users/create/', views.create, name='create'),
    url(r'^users/list/$', views.show_users_list, name='disp_users'),
    url(r'^users/(?P<userId>\d+)/$', views.show, name='show'),
    url(r'^users/(?P<userId>)/edit/', views.edit, name='edit'),
    url(r'^users/(?P<userId>)/update/', views.edit, name='update'),
    url(r'^users/(?P<userId>)/destroy/', views.destroy, name='destroy'),
]
