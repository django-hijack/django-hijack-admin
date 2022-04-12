# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
import django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from hijack_admin.admin import HijackUserAdmin
from hijack.tests.utils import SettingsOverride

if django.VERSION < (1, 7):
    pass
else:
    from django.conf import settings
    from django.core.checks import Error, Warning
    from django.test import TestCase, override_settings

    from hijack import settings as hijack_settings

    from hijack_admin import checks
    from hijack_admin.apps import HijackAdminConfig

    class ChecksTests(TestCase):

        def test_check_get_requests_allowed(self):

            self.assertTrue(hijack_settings.HIJACK_ALLOW_GET_REQUESTS)
            errors = checks.check_get_requests_allowed(HijackAdminConfig)
            self.assertFalse(errors)

            with SettingsOverride(hijack_settings, HIJACK_ALLOW_GET_REQUESTS=False):
                errors = checks.check_get_requests_allowed(HijackAdminConfig)
                expected_errors = [
                    Error(
                        'Hijack GET requests must be allowed for django-hijack-admin to work.',
                        hint='Set HIJACK_ALLOW_GET_REQUESTS to True.',
                        obj=None,
                        id='hijack_admin.E001',
                    )
                ]
                self.assertEqual(errors, expected_errors)

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
