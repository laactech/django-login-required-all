# Django Require Login

[![Build Status](https://travis-ci.org/laactech/django-require-login.svg?branch=master)](https://travis-ci.org/laactech/django-require-login)
[![codecov](https://codecov.io/gh/laactech/django-require-login/branch/master/graph/badge.svg)](https://codecov.io/gh/laactech/django-require-login)
[![PyPI](https://img.shields.io/pypi/v/django-require-login)](https://pypi.org/project/django-require-login/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://github.com/laactech/django-require-login/blob/master/LICENSE.md)

Forked from [django-stronghold](https://github.com/mgrouchy/django-stronghold)

Require login on all your django URLs by default

## Supported Versions

* Python 3.10, 3.11, 3.12
* Django 4.2, 5.0

## Installation and Setup

Install via pip.

```sh
pip install django-require-login
```

Then add the middleware to your MIDDLEWARE in your Django settings file

```python
MIDDLEWARE = [
    #...
    "django_require_login.middleware.LoginRequiredMiddleware",
]

```

After adding the middleware, all your Django views will default to login required.

If your `LOGIN_URL` and `LOGOUT_REDIRECT_URL` contain a
[named URL pattern](https://docs.djangoproject.com/en/2.2/topics/http/urls/#naming-url-patterns)
add `REQUIRE_LOGIN_PUBLIC_NAMED_URLS` to your settings file with your `LOGIN_URL` and
`LOGOUT_REDIRECT_URL`

```python
REQUIRE_LOGIN_PUBLIC_NAMED_URLS = (LOGIN_URL, LOGOUT_REDIRECT_URL)
```

If your `LOGIN_URL` and `LOGOUT_REDIRECT_URL` don't contain a named URL pattern add 
`REQUIRE_LOGIN_PUBLIC_URLS` to your settings file with your `LOGIN_URL` and
`LOGOUT_REDIRECT_URL`

```python
REQUIRE_LOGIN_PUBLIC_URLS = (LOGIN_URL, LOGOUT_REDIRECT_URL)
```

## Usage

To make a view public again you can use the public decorator:

### For function based views
```python
from django_require_login.decorators import public
from django.http import HttpResponse


@public
def my_view(request):
    return HttpResponse("Public")

```

### For class based views (decorator)

```python
from django.utils.decorators import method_decorator
from django_require_login.decorators import public
from django.views.generic import View
from django.http import HttpResponse


class SomeView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Public view")
    
    @method_decorator(public)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
```

### For class based views (mixin)

```python
from django_require_login.mixins import PublicViewMixin
from django.views.generic import View


class SomeView(PublicViewMixin, View):
	pass
```

## Configuration (optional)

You can add a tuple of url regexes in your settings file with the
`REQUIRE_LOGIN_PUBLIC_URLS` setting. Any url that matches against these patterns
 will be made public without using the `@public` decorator.


### REQUIRE_LOGIN_PUBLIC_URLS

**Default**:
```python
REQUIRE_LOGIN_PUBLIC_URLS = ()
```

#### Development Defaults
If `DEBUG` is True, `REQUIRE_LOGIN_PUBLIC_URLS` contains:
```python
from django.conf import settings

(
    r'{}.+$'.format(settings.STATIC_URL),
    r'{}.+$'.format(settings.MEDIA_URL),
)

```
This is additive to your settings to support serving static files and media files from
the development server. It does not replace any settings you may have in
`REQUIRE_LOGIN_PUBLIC_URLS`.

> Note: Public URL regexes are matched against 
>[HttpRequest.path_info](https://docs.djangoproject.com/en/dev/ref/request-response/#django.http.HttpRequest.path_info).

### REQUIRE_LOGIN_PUBLIC_NAMED_URLS
You can add a tuple of url names in your settings file with the
`REQUIRE_LOGIN_PUBLIC_NAMED_URLS` setting. Names in this setting will be reversed using
`django.urls.reverse` and any url matching the output of the reverse
call will be made public without using the `@public` decorator:

**Default**:
```python
REQUIRE_LOGIN_PUBLIC_NAMED_URLS = ()
```

### REQUIRE_LOGIN_USER_TEST_FUNC
Optionally, set REQUIRE_LOGIN_USER_TEST_FUNC to a callable to limit access to users
that pass a custom test. The callback receives a `User` object and should
return `True` if the user is authorized. This is equivalent to decorating a
view with `user_passes_test`.

**Example**:

```python
REQUIRE_LOGIN_USER_TEST_FUNC = lambda user: user.is_staff
```

**Default**:

```python
REQUIRE_LOGIN_USER_TEST_FUNC = lambda user: user.is_authenticated
```

## Integration with Django REST Framework

Django REST Framework is not part of Django and uses its own authentication system.
For this reason, you need to make all of your DRF views public and rely on DRF's
authentication system.

### Example

Assuming all your DRF views live under `/api/` you can make them all public using a regex:

```python
REQUIRE_LOGIN_PUBLIC_URLS = (r"^/api/.*",)
```

## Security

If you believe you've found a bug with security implications, please do not disclose this
issue in a public forum.

Email us at [support@laac.dev](mailto:support@laac.dev)

## Contribute

See [CONTRIBUTING.md](https://github.com/laactech/django-require-login/blob/master/CONTRIBUTING.md)
