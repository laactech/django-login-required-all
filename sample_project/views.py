from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import View

from django_require_login.decorators import public
from django_require_login.mixins import PublicViewMixin


class ProtectedView(View):
    """A view we want to be private"""

    def get(self, request, *args, **kwargs):
        return HttpResponse("ProtectedView")


class PublicView(View):
    """A view we want to be public"""

    @method_decorator(public)
    def dispatch(self, *args, **kwargs):
        return super(PublicView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return HttpResponse("PublicView")


class PublicView2(PublicViewMixin, View):
    """A view we want to be public, using the PublicViewMixin"""

    def get(self, request, *args, **kwargs):
        return HttpResponse("PublicView")


@public
def public_view3(request):
    """A function view we want to be public"""
    return HttpResponse("PublicView")
