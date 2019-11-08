def is_view_func_public(func):
    """
    Returns whether a view is public or not (ie/ has the LRA_IS_PUBLIC
    attribute set)
    """
    return getattr(func, "LRA_IS_PUBLIC", False)


def set_view_func_public(func):
    """
    Set the LRA_IS_PUBLIC attribute on a given function to True
    """
    func.LRA_IS_PUBLIC = True
