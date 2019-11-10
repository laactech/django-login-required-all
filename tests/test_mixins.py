import unittest

from django.views.generic import View
from django.views.generic.base import TemplateResponseMixin

from django_require_login.mixins import PublicViewMixin


class LoginRequiredMixinsTests(unittest.TestCase):
    def test_public_mixin_sets_attr(self):
        class TestView(PublicViewMixin, View):
            pass

        self.assertTrue(TestView.dispatch.REQUIRE_LOGIN_IS_PUBLIC)

    def test_public_mixin_sets_attr_with_multiple_mixins(self):
        class TestView(PublicViewMixin, TemplateResponseMixin, View):
            template_name = "dummy.html"

        self.assertTrue(TestView.dispatch.REQUIRE_LOGIN_IS_PUBLIC)
