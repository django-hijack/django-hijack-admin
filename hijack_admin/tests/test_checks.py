# -*- coding: utf-8 -*-
from compat import get_user_model
import django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from hijack_admin.admin import HijackUserAdmin

if django.VERSION < (1, 7):
    pass
else:
    from django.conf import settings
    from django.core.checks import Warning
    from django.test import TestCase, override_settings

    from hijack_admin import checks
    from hijack_admin.apps import HijackAdminConfig

    class ChecksTests(TestCase):

        def test_check_default_user_model(self):
            warnings = checks.check_custom_user_model(HijackAdminConfig)
            self.assertFalse(warnings)

        @override_settings(AUTH_USER_MODEL='test_app.BasicModel')
        def test_check_custom_user_model(self):
            # Django doesn't re-register admins when using `override_settings`,
            # so we have to do it manually in this test case.
            admin.site.register(get_user_model(), HijackUserAdmin)

            warnings = checks.check_custom_user_model(HijackAdminConfig)
            self.assertFalse(warnings)

            admin.site.unregister(get_user_model())

        @override_settings(AUTH_USER_MODEL='test_app.BasicModel')
        def test_check_custom_user_model_default_admin(self):
            # Django doesn't re-register admins when using `override_settings`,
            # so we have to do it manually in this test case.
            admin.site.register(get_user_model(), UserAdmin)

            warnings = checks.check_custom_user_model(HijackAdminConfig)
            expected_warnings = [
                Warning(
                    'django-hijack-admin does not work out the box with a custom user model.',
                    hint='Please mix HijackUserAdminMixin into your custom UserAdmin.',
                    obj=settings.AUTH_USER_MODEL,
                    id='hijack_admin.W001',
                )
            ]
            self.assertEqual(warnings, expected_warnings)

            admin.site.unregister(get_user_model())

        @override_settings(AUTH_USER_MODEL='test_app.BasicModel')
        def test_check_custom_user_model_custom_admin(self):
            class CustomAdminSite(admin.AdminSite):
                pass

            _default_site = admin.site
            admin.site = CustomAdminSite()
            admin.autodiscover()

            admin.site.register(get_user_model(), HijackUserAdmin)

            warnings = checks.check_custom_user_model(HijackAdminConfig)
            self.assertFalse(warnings)

            admin.site.unregister(get_user_model())
            admin.site = _default_site
