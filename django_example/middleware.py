from expressly import Api, api_url
from django_example.settings import EXPRESSLY_API_KEY


class ExpresslyApiMiddleware(object):
    def process_request(self, request):
        if 'expressly/api' in request.META['PATH_INFO']:
            request.expressly_api = Api(EXPRESSLY_API_KEY, api_url)
