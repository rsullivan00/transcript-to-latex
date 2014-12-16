from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from .views import *
from scutranscript import settings

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'scutranscript.views.index', name='index'),
    url(r'^transcript', 'scutranscript.views.transcript', name='transcript')
    # url(r'^blog/', include('blog.urls')),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += staticfiles_urlpatterns()
