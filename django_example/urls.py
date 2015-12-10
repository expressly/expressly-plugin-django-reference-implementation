from django.conf.urls import patterns, include, url
from django.contrib import admin
from expressly import routes
from django_example import views

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'django_example.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^%s$' % routes['ping'].regex, views.ping),
    url(r'^%s$' % routes['registered'].regex, views.registered),
    url(r'^%s$' % routes['user'].regex, views.user),
    url(r'^%s$' % routes['migration_popup'].regex, views.migration_popup),
    url(r'^%s$' % routes['migration_user'].regex, views.migration_user),
    url(r'^%s$' % routes['batch_customer'].regex, views.batch_customer),
    url(r'^%s$' % routes['batch_invoice'].regex, views.batch_invoice),
)
