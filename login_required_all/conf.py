import re

from django.conf import settings

try:
    from django.urls import reverse, NoReverseMatch
except ImportError:
    from django.core.urlresolvers import reverse, NoReverseMatch

LRA_PUBLIC_URLS = getattr(settings, "LRA_PUBLIC_URLS", ())
LRA_DEFAULTS = getattr(settings, "LRA_DEFAULTS", True)
LRA_PUBLIC_NAMED_URLS = getattr(settings, "LRA_PUBLIC_NAMED_URLS", ())


def is_authenticated(user):
    """ make compatible with django 1 and 2 """
    try:
        return user.is_authenticated()
    except TypeError:
        return user.is_authenticated


LRA_USER_TEST_FUNC = getattr(settings, "LRA_USER_TEST_FUNC", is_authenticated)


if LRA_DEFAULTS:
    if "django.contrib.auth" in settings.INSTALLED_APPS:
        LRA_PUBLIC_NAMED_URLS += ("login", "logout")

    # Do not login protect the logout url, causes an infinite loop
    logout_url = getattr(settings, "LOGOUT_URL", None)
    if logout_url:
        LRA_PUBLIC_URLS += (r"^%s.+$" % logout_url,)

    if settings.DEBUG:
        # In Debug mode we serve the media urls as public by default as a
        # convenience. We make no other assumptions
        static_url = getattr(settings, "STATIC_URL", None)
        media_url = getattr(settings, "MEDIA_URL", None)

        if static_url:
            LRA_PUBLIC_URLS += (r"^%s.+$" % static_url,)

        if media_url:
            LRA_PUBLIC_URLS += (r"^%s.+$" % media_url,)

# named urls can be unsafe if a user puts the wrong url in. Right now urls that
# dont reverse are just ignored with a warning. Maybe in the future make this
# so it breaks?
named_urls = []
for named_url in LRA_PUBLIC_NAMED_URLS:
    try:
        url = reverse(named_url)
        named_urls.append(url)
    except NoReverseMatch:
        # print "Stronghold: Could not reverse Named URL: '%s'. Is it in your
        # `urlpatterns`? Ignoring." % named_url
        # ignore non-matches
        pass


LRA_PUBLIC_URLS += tuple(["^%s$" % url for url in named_urls])

if LRA_PUBLIC_URLS:
    LRA_PUBLIC_URLS = [re.compile(v) for v in LRA_PUBLIC_URLS]
