from django.contrib.auth.decorators import user_passes_test

from login_required_all import conf, utils

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object


class LoginRequiredMiddleware(MiddlewareMixin):
    """
    Restrict access to users that for which LRA_USER_TEST_FUNC returns
    True. Default is to check if the user is authenticated.

    View is deemed to be public if the @public decorator is applied to the view

    View is also deemed to be Public if listed in in django settings in the
    LRA_PUBLIC_URLS dictionary
    each url in LRA_PUBLIC_URLS must be a valid regex

    """

    def __init__(self, *args, **kwargs):
        if MiddlewareMixin != object:
            super().__init__(*args, **kwargs)
        self.public_view_urls = getattr(conf, "LRA_PUBLIC_URLS", ())

    def process_view(self, request, view_func, view_args, view_kwargs):
        if (
            conf.LRA_USER_TEST_FUNC(request.user)
            or utils.is_view_func_public(view_func)
            or self.is_public_url(request.path_info)
        ):
            return None

        decorator = user_passes_test(conf.LRA_USER_TEST_FUNC)
        return decorator(view_func)(request, *view_args, **view_kwargs)

    def is_public_url(self, url):
        return any(public_url.match(url) for public_url in self.public_view_urls)
