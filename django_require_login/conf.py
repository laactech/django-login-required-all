import re

from django.conf import settings
from django.urls import NoReverseMatch, reverse

from .exceptions import NamedUrlNoReverseMatch

REQUIRE_LOGIN_PUBLIC_URLS = getattr(settings, "REQUIRE_LOGIN_PUBLIC_URLS", ())
REQUIRE_LOGIN_DEFAULTS = getattr(settings, "REQUIRE_LOGIN_DEFAULTS", True)
REQUIRE_LOGIN_PUBLIC_NAMED_URLS = getattr(settings, "REQUIRE_LOGIN_PUBLIC_NAMED_URLS", ())


def is_authenticated(user):
    """ make compatible with django 1 and 2 """
    try:
        return user.is_authenticated()
    except TypeError:
        return user.is_authenticated


REQUIRE_LOGIN_USER_TEST_FUNC = getattr(
    settings, "REQUIRE_LOGIN_USER_TEST_FUNC", is_authenticated
)
if settings.DEBUG:
    # In Debug mode we serve the media urls as public by default as a
    # convenience. We make no other assumptions
    static_url = getattr(settings, "STATIC_URL", None)
    media_url = getattr(settings, "MEDIA_URL", None)

    if static_url:
        REQUIRE_LOGIN_PUBLIC_URLS += (r"^{}.+$".format(static_url),)

    if media_url:
        REQUIRE_LOGIN_PUBLIC_URLS += (r"^{}.+$".format(media_url),)

# named urls can be unsafe if a user puts the wrong url in. Right now urls that
# dont reverse are just ignored with a warning. Maybe in the future make this
# so it breaks?
named_urls = []
for named_url in REQUIRE_LOGIN_PUBLIC_NAMED_URLS:
    try:
        url = reverse(named_url)
        named_urls.append(url)
    except NoReverseMatch:
        raise NamedUrlNoReverseMatch(
            "Reverse match for {} could not be found. Make sure it is in your urlpatterns".format(
                named_url
            )
        )


REQUIRE_LOGIN_PUBLIC_URLS += tuple(["^{}$".format(url) for url in named_urls])

if REQUIRE_LOGIN_PUBLIC_URLS:
    REQUIRE_LOGIN_PUBLIC_URLS = [re.compile(v) for v in REQUIRE_LOGIN_PUBLIC_URLS]
