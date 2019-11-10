from django.contrib.auth.decorators import user_passes_test

from . import conf, utils


class LoginRequiredMiddleware:
    """
    Restrict access to users that for which REQUIRE_LOGIN_USER_TEST_FUNC returns
    True. Default is to check if the user is authenticated.

    View is deemed to be public if the @public decorator is applied to the view

    View is also deemed to be Public if listed in in django settings in the
    REQUIRE_LOGIN_PUBLIC_URLS dictionary
    each url in REQUIRE_LOGIN_PUBLIC_URLS must be a valid regex

    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.public_view_urls = getattr(conf, "REQUIRE_LOGIN_PUBLIC_URLS", ())

    def process_view(self, request, view_func, view_args, view_kwargs):
        if (
            conf.REQUIRE_LOGIN_USER_TEST_FUNC(request.user)
            or utils.is_view_func_public(view_func)
            or self.is_public_url(request.path_info)
        ):
            return None

        decorator = user_passes_test(conf.REQUIRE_LOGIN_USER_TEST_FUNC)
        return decorator(view_func)(request, *view_args, **view_kwargs)

    def is_public_url(self, url):
        return any(public_url.match(url) for public_url in self.public_view_urls)

    def __call__(self, request):
        response = self.get_response(request)
        return response
