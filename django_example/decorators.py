import re
from functools import wraps
from django.http import HttpResponse


def require_authorization():
    def decorator(f):
        @wraps(f)
        def inner(request, *args, **kwargs):
            authorization = request.META.get('HTTP_AUTHORIZATION')
            if authorization is None:
                return HttpResponse(status=401)

            m = re.compile('Basic (?P<token>\w+)').match(authorization)
            if request.expressly_api.api_key != m.groupdict()['token']:
                return HttpResponse(status=401)

            return f(request, *args, **kwargs)

        return inner

    return decorator
