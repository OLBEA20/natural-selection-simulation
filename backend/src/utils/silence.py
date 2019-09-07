def silence(function):
    def decorator(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception:
            pass

    return decorator
