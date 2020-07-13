class Decorator():
    def default_expected_code(status_code):
        def decorator(func):
            def wrapper(*args, **kwargs):
                if ("expected_status_code" in kwargs):
                    if (kwargs["expected_status_code"] is None):
                        kwargs["expected_status_code"] = status_code
                else:
                    kwargs["expected_status_code"] = status_code
                return func(*args, **kwargs)
            return wrapper
        return decorator