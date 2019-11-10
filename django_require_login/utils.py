def is_view_func_public(func):
    """
    Returns whether a view is public or not (ie/ has the REQUIRE_LOGIN_IS_PUBLIC
    attribute set)
    """
    return getattr(func, "REQUIRE_LOGIN_IS_PUBLIC", False)


def set_view_func_public(func):
    """
    Set the REQUIRE_LOGIN_IS_PUBLIC attribute on a given function to True
    """
    func.REQUIRE_LOGIN_IS_PUBLIC = True
