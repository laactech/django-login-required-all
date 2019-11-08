# Django Login Required All

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://github.com/laactech/django-login-required-all/blob/master/LICENSE.md)

Forked from [django-stronghold](https://github.com/mgrouchy/django-stronghold)

Get inside your stronghold and make all your Django views default login_required

Stronghold is a very small and easy to use django app that makes all your Django project default to require login for all of your views.

WARNING: still in development, so some of the DEFAULTS and such will be changing without notice.

## Installation

Install via pip.

```sh
pip install django-login-required-all
```

Then add the middleware to your MIDDLEWARE_CLASSES in your Django settings file

```python
MIDDLEWARE_CLASSES = (
    #...
    'login_required_all.middleware.LoginRequiredMiddleware',
)

```

## Usage

If you followed the installation instructions now all your views are defaulting to require a login.
To make a view public again you can use the public decorator provided in `stronghold.decorators` like so:

### For function based views
```python
from login_required_all.decorators import public


@public
def someview(request):
	# do some work
	#...

```

### For class based views (decorator)

```python
from django.utils.decorators import method_decorator
from login_required_all.decorators import public


class SomeView(View):
	def get(self, request, *args, **kwargs):
		# some view logic
		#...

	@method_decorator(public)
	def dispatch(self, *args, **kwargs):
    	return super(SomeView, self).dispatch(*args, **kwargs)
```

### For class based views (mixin)

```python
from login_required_all.views import StrongholdPublicMixin


class SomeView(StrongholdPublicMixin, View):
	pass
```

## Configuration (optional)


### LRA_DEFAULTS

Use Strongholds defaults in addition to your own settings.

**Default**:

```python
LRA_DEFAULTS = True
```

You can add a tuple of url regexes in your settings file with the
`LRA_PUBLIC_URLS` setting. Any url that matches against these patterns
 will be made public without using the `@public` decorator.


### LRA_PUBLIC_URLS

**Default**:
```python
LRA_PUBLIC_URLS = ()
```

If LRA_DEFAULTS is True LRA_PUBLIC_URLS contains:
```python
(
    r'^%s.+$' % settings.STATIC_URL,
    r'^%s.+$' % settings.MEDIA_URL,
)

```
When settings.DEBUG = True. This is additive to your settings to support serving
Static files and media files from the development server. It does not replace any
settings you may have in `LRA_PUBLIC_URLS`.

> Note: Public URL regexes are matched against 
>[HttpRequest.path_info](https://docs.djangoproject.com/en/dev/ref/request-response/#django.http.HttpRequest.path_info).

### LRA_PUBLIC_NAMED_URLS
You can add a tuple of url names in your settings file with the
`LRA_PUBLIC_NAMED_URLS` setting. Names in this setting will be reversed using
`django.core.urlresolvers.reverse` and any url matching the output of the reverse
call will be made public without using the `@public` decorator:

**Default**:
```python
LRA_PUBLIC_NAMED_URLS = ()
```

If LRA_DEFAULTS is True additionally we search for `django.contrib.auth`
if it exists, we add the login and logout view names to `LRA_PUBLIC_NAMED_URLS`

### LRA_USER_TEST_FUNC
Optionally, set LRA_USER_TEST_FUNC to a callable to limit access to users
that pass a custom test. The callback receives a `User` object and should
return `True` if the user is authorized. This is equivalent to decorating a
view with `user_passes_test`.

**Example**:

```python
LRA_USER_TEST_FUNC = lambda user: user.is_staff
```

**Default**:

```python
LRA_USER_TEST_FUNC = lambda user: user.is_authenticated
```

## Contribute

See CONTRIBUTING.md
