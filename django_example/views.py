import json

from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from expressly.errors import GenericError
from expressly.route_responses import PingResponse, RegisteredResponse
from django_example.decorators import require_authorization
from django_example.provider import ExpresslyProvider


@require_http_methods('GET')
def ping(request):
    return HttpResponse(PingResponse(), content_type='application/json')


@require_authorization()
@require_http_methods('GET')
def registered(request):
    return HttpResponse(RegisteredResponse(), content_type='application/json')


@require_authorization()
@require_http_methods('GET')
def user(request, email):
    provider = ExpresslyProvider()
    customer = provider.get_customer(email)

    return HttpResponse(str(customer), content_type='application/json')


@require_http_methods('GET')
def migration_popup(request, uuid):
    api = request.expressly_api
    html = api.get_migration_popup(uuid)
    return HttpResponse(html, content_type='text/html')


@require_http_methods('GET')
def migration_user(request, uuid):
    api = request.expressly_api
    provider = ExpresslyProvider()

    customer_response = api.get_migration_customer(uuid)
    email = customer_response.data.email
    customer = customer_response.data.data
    cart = customer_response.data.cart

    if provider.customer_register(customer):
        provider.customer_add_cart(email, cart.product_id, cart.coupon_code)
        provider.customer_send_password_email(email)
        provider.customer_login(email)
        api.send_migration_status(uuid)
    else:
        api.send_migration_status(uuid, True)
        raise GenericError

    return HttpResponseRedirect('/')


@require_authorization()
@require_http_methods('POST')
@csrf_exempt
def batch_customer(request):
    provider = ExpresslyProvider()
    body = json.loads(request.body.decode('utf-8'))

    if 'emails' not in body:
        raise GenericError

    return HttpResponse(str(provider.get_customer_statuses(body['emails'])), content_type='application/json')


@require_authorization()
@require_http_methods('POST')
@csrf_exempt
def batch_invoice(request):
    provider = ExpresslyProvider()
    body = json.loads(request.body.decode('utf-8'))

    if 'customers' not in body:
        raise GenericError

    return HttpResponse(str(provider.get_customer_invoices(body['customers'])), content_type='application/json')
