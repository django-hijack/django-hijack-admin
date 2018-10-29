# -*- coding: utf-8 -*-
from compat import get_user_model
from django import VERSION
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.template.loader import get_template
from django.utils.translation import ugettext_lazy as _

from hijack import settings as hijack_settings

from hijack_admin import settings as hijack_admin_settings

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse


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

        return button_template.render(button_context)

    hijack_field.short_description = _('Hijack user')


class HijackRelatedAdminMixin(HijackUserAdminMixin):

    def hijack_field(self, obj):
        user = getattr(obj, 'user', '')
        if not user:
            for field in obj._meta.get_fields():
                if (field.one_to_one or field.many_to_one) and getattr(field, 'related_model') == get_user_model():
                    user = getattr(obj, field.name)
        return super(HijackRelatedAdminMixin, self).hijack_field(user)


class HijackUserAdmin(HijackUserAdminMixin, UserAdmin):
    list_display = UserAdmin.list_display + ('hijack_field', )


if hijack_admin_settings.HIJACK_REGISTER_ADMIN:
    UserModel = get_user_model()
    admin.site.unregister(UserModel)
    admin.site.register(UserModel, HijackUserAdmin)
