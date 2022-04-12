"""URLs to run the tests."""
from from django.urls import include, re_path

from django.contrib import admin

from hijack_admin.admin import HijackRelatedAdminMixin
from hijack_admin.tests.test_app.models import RelatedModel


@admin.register(RelatedModel)
class RelatedModelAdmin(HijackRelatedAdminMixin, admin.ModelAdmin):
    list_display = ('user', 'hijack_field')


admin.autodiscover()

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^hijack/', include('hijack.urls', namespace='hijack')),
    re_path(r'^hello/', include('hijack.tests.test_app.urls', namespace='test_app'))
]
