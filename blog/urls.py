from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

# URL relies on primary keys to distinguish between different instruments
urlpatterns = [
    url(r'^$', views.instrument_list, name='instrument_list'),
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^instrument/new/$', views.instrument_new, name='instrument_new'),
    url(r'^instrument/(?P<pk>\d+)/edit/$', views.instrument_edit, name='instrument_edit'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^instrument/(?P<pk>\d+)/checkout/$', views.checkout_detail, name='checkout_detail'),
    url(r'^instrument/(?P<pk>\d+)/release/$', views.release_detail, name='release_detail'),
    url(r'^instrument/(?P<pk>\d+)/detail/$', views.instrument_detail, name='instrument_detail'),
    url(r'^instrument/(?P<pk>\d+)/closeconnection/$', views.instrument_close_connection,
        name='instrument_close_connection'),
    url(r'^instrument/(?P<pk>\d+)/openconnection/$', views.instrument_open_connection,
        name='instrument_open_connection'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^confirm/logout/$', views.user_logout_confirm, name='logout_confirm'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^user/settings/$', views.user_settings, name='user_settings'),
    url(r'^password_change/$', views.password_change, name='password_change'),
    url(r'^mass_message/$', views.mass_message, name='mass_message'),
    url(r'^user_message/(?P<pk>\d+)/$', views.user_message, name='user_message'),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
