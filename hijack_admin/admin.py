# -*- coding: utf-8 -*-
from compat import get_user_model, reverse
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.template.loader import get_template
from django.utils.translation import ugettext_lazy as _
from django import VERSION

from hijack import settings as hijack_settings
from hijack_admin import settings as hijack_admin_settings

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse

if VERSION < (1, 8):
    from django.template import Context


class HijackUserAdminMixin(object):

    def hijack_field(self, obj):
        hijack_attributes = hijack_settings.HIJACK_URL_ALLOWED_ATTRIBUTES

        if 'user_id' in hijack_attributes:
            hijack_url = reverse('hijack:login_with_id', args=(obj.pk, ))
        elif 'email' in hijack_attributes:
            hijack_url = reverse('hijack:login_with_email', args=(obj.email, ))
        else:
            hijack_url = reverse('hijack:login_with_username', args=(obj.username, ))

        button_template = get_template(hijack_admin_settings.HIJACK_BUTTON_TEMPLATE)
        button_context = {
            'hijack_url': hijack_url,
            'username': str(obj),
        }
        if VERSION < (1, 8):
            button_context = Context(button_context)

        return button_template.render(button_context)

    hijack_field.allow_tags = True
    hijack_field.short_description = _('Hijack user')


class HijackRelatedAdminMixin(HijackUserAdminMixin):

    def hijack_field(self, obj):
        return super(HijackRelatedAdminMixin, self).hijack_field(obj.user)


class HijackUserAdmin(HijackUserAdminMixin, UserAdmin):
    list_display = UserAdmin.list_display + ('hijack_field', )


if hijack_admin_settings.HIJACK_REGISTER_ADMIN:
    UserModel = get_user_model()
    admin.site.unregister(UserModel)
    admin.site.register(UserModel, HijackUserAdmin)
