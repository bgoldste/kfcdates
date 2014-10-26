from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ncog.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'core.views.login', name='login'),
    url(r'^logout/$', 'core.views.logout', name='logout'),
    url(r'^home/$', 'core.views.home', name='home'),
	url(r'^index/$', 'core.views.index', name='home'),
	url(r'^users', 'core.views.test_users', name='home'),
	url(r'^proposals', 'core.views.proposals', name='home'),
    url(r'^slots', 'core.views.slots', name='home'),
    url(r'^dates', 'core.views.dates', name='home'),
    #Facebook

	url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^admin/', include(admin.site.urls)),
)
