from functools import wraps
from flask import request


def pageable_content(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        page_id = int(request.args.get("page", 1))

        return f(page_id, *args, **kwargs)
    return decorated_function
