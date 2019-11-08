from django.utils.decorators import method_decorator

from login_required_all.decorators import public


class StrongholdPublicMixin:
    @method_decorator(public)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
