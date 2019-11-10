import functools
import unittest

from django.utils.decorators import method_decorator

from django_require_login import decorators


class LoginRequiredDecoratorTests(unittest.TestCase):
    def test_public_decorator_sets_attr(self):
        @decorators.public
        def function():
            pass

        self.assertTrue(function.REQUIRE_LOGIN_IS_PUBLIC)

    def test_public_decorator_sets_attr_with_nested_decorators(self):
        def stub_decorator(func):
            return func

        @decorators.public
        @stub_decorator
        def inner_function():
            pass

        self.assertTrue(inner_function.REQUIRE_LOGIN_IS_PUBLIC)

    def test_public_decorator_works_with_partials(self):
        def function():
            pass

        partial = functools.partial(function)

        decorators.public(partial)

        self.assertTrue(function.REQUIRE_LOGIN_IS_PUBLIC)

    def test_public_decorator_works_with_method_decorator(self):
        class TestClass:
            @method_decorator(decorators.public)
            def function(self):
                pass

        self.assertTrue(TestClass.function.REQUIRE_LOGIN_IS_PUBLIC)
