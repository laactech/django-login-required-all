# Django Require Login

[![Build Status](https://travis-ci.org/laactech/django-require-login.svg?branch=master)](https://travis-ci.org/laactech/django-require-login)
[![codecov](https://codecov.io/gh/laactech/django-require-login/branch/master/graph/badge.svg)](https://codecov.io/gh/laactech/django-require-login)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://github.com/laactech/django-require-login/blob/master/LICENSE.md)

Forked from [django-stronghold](https://github.com/mgrouchy/django-stronghold)

Require login on all your django URLs by default

## Supported Versions

* Python 3.5, 3.6, 3.7
* Django 1.11, 2.0, 2.1, 2.2

## Installation

Install via pip.

```sh
pip install django-require-login
```

Then add the middleware to your MIDDLEWARE_CLASSES in your Django settings file

```python
MIDDLEWARE_CLASSES = (
    #...
    "django_require_login.middleware.LoginRequiredMiddleware",
)

```

## Usage

If you followed the installation instructions now all your views are defaulting to require a login.
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

If DEBUG is True, REQUIRE_LOGIN_PUBLIC_URLS contains:
```python
from django.conf import settings

(
    r'{}.+$'.format(settings.STATIC_URL),
    r'{}.+$'.format(settings.MEDIA_URL),
)

```
When settings.DEBUG = True, this is additive to your settings to support serving
Static files and media files from the development server. It does not replace any
settings you may have in `REQUIRE_LOGIN_PUBLIC_URLS`.

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

## Security

If you believe you've found a bug with security implications, please do not disclose this
issue in a public forum.

Email us at [support@laac.dev](mailto:support@laac.dev)

## Contribute

See [CONTRIBUTING.md](https://github.com/laactech/django-require-login/blob/master/CONTRIBUTING.md)
