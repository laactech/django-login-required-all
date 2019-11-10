from django.utils.decorators import method_decorator

from .decorators import public


class PublicViewMixin:
    @method_decorator(public)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
