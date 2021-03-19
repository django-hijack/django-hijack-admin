![No longer maintained](https://img.shields.io/badge/Maintenance-OFF-red.svg)
### [DEPRECATED] django-hijack-admin is no longer maintained
> After the [changes](https://github.com/django-hijack/django-hijack/pull/235) in [django-hijack](https://github.com/django-hijack/django-hijack) version 3.0, the integration of the admin is part of it.
> 
> The changes made in django-hijack are fully focused on security and at the moment there is no objective reasons to keep the admin integration in a separate package.



# django-hijack-admin

Django admin integration for Django Hijack (https://github.com/arteria/django-hijack/)

[![Build Status](https://travis-ci.org/arteria/django-hijack-admin.svg?branch=master)](https://travis-ci.org/arteria/django-hijack-admin)
[![Coverage Status](https://coveralls.io/repos/arteria/django-hijack-admin/badge.svg?branch=master&service=github)](https://coveralls.io/github/arteria/django-hijack-admin?branch=master)
[![PyPI](https://img.shields.io/pypi/v/django-hijack-admin.svg)](https://pypi.python.org/pypi/django-hijack-admin)

![Screenshot of django-hijack in action on the admin site.](docs/admin-screenshot.png)


## Installation

Follow the instructions on http://django-hijack.readthedocs.org/en/stable/#installation to install django-hijack.

Get the latest stable release from PyPi:

    pip install django-hijack-admin

In your ``settings.py``, add ``hijack_admin`` to your installed apps:

```python
INSTALLED_APPS = (
    ...,
    'hijack_admin',
)
```

For the admin integration to work, you must explicitly set `HIJACK_ALLOW_GET_REQUESTS = True` in your project settings.
Please be aware that users can now be hijacked not only using POST requests, but also using GET requests, which could facilitate CSRF attacks.

## Configuration

### `HIJACK_BUTTON_TEMPLATE`
Path to the template for the "Hijack" buttons. Default: `'hijack_admin/admin_button.html'`

### `HIJACK_REGISTER_ADMIN`
Whether the user model should be registered with `HijackUserAdmin` automatically. Default: `True`

### `HIJACK_USER_ADMIN_CLASS_NAME`

Adds the possibility to configure the admin class name.

## Custom user admins
Custom user admins are supported. Just set `HIJACK_REGISTER_ADMIN = False` and
modify your custom admin class as shown in this example:

```python
# admin.py
from hijack_admin.admin import HijackUserAdminMixin

class MyUserAdmin(UserAdmin, HijackUserAdminMixin):
    list_display = (
        ...
        'hijack_field',  # Hijack button
    )
```

## Models with ForeignKey to User
You can also add the hijack field to a model that is related to the User
model with the `HijackRelatedAdminMixin`.

```python
#admin.py
from django.contrib import Admin
from hijack_admin.admin import HijackRelatedAdminMixin

class MyCustomerAdmin(HijackRelatedAdminMixin, admin.ModelAdmin)
    list_display = ('user', 'hijack_field')
```


# Contributing
Anyone and everyone is welcome to contribute. Please take a moment to review the [guidelines for contributing](CONTRIBUTING.md).


| django-hijack-admin is free software. If you find it useful and would like to give back, please consider to make a donation using [Bitcoin](https://blockchain.info/payment_request?address=1AJkbQdcNkrHzxi91mB1kkPxh4t4BJ4hu4) or [PayPal](https://www.paypal.me/arteriagmbh). Thank you! |
| ----- |
