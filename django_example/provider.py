from abc import ABCMeta
from datetime import datetime
from expressly.provider import ProviderBase
from expressly.route_responses import BatchInvoiceResponse, BatchCustomerResponse, CustomerResponse


class ExpresslyProvider(metaclass=ABCMeta):
    def customer_register(self, customer) -> bool:
        return True

    def customer_login(self, customer_id) -> bool:
        return True

    def customer_add_cart(self, customer_id, product_id=None, coupon_code=None) -> bool:
        return True

    def customer_send_password_email(self, customer_id) -> bool:
        return True

    def get_customer(self, email) -> CustomerResponse:
        return CustomerResponse(
            raw_data={
                'data': {
                    'email': email,
                    'user_reference': '43',
                    'customer_data': {
                        'first_name': 'Sam',
                        'last_name': 'Pratt',
                        'gender': 'M',
                        'company': 'Expressly',
                        'emails': [
                            {
                                'email': email,
                                'alias': 'default'
                            }
                        ],
                        'phones': [
                            {
                                'type': 'M',
                                'number': '07951234567'
                            }
                        ],
                        'addresses': [
                            {
                                'first_name': 'Sam',
                                'last_name': 'Pratt',
                                'address1': '19 Eastbourne Tr',
                                'companyName': 'Expressly',
                                'zip': 'W2 6LG',
                                'city': 'London',
                                'country': 'GBR',
                                'phone': 0
                            }
                        ]
                    }
                }
            }
        )

    def get_customer_invoices(self, customers) -> BatchInvoiceResponse:
        date_time = datetime.utcnow().isoformat('T')

        return BatchInvoiceResponse(raw_data={
            'invoices': [
                {
                    'email': c['email'],
                    'orderCount': 1,
                    'preTaxTotal': "100.01",
                    'tax': "10.00",
                    'orders': [
                        {
                            'id': 8301,
                            'date': date_time,
                            'itemCount': 1,
                            'preTaxTotal': "100.01",
                            'tax': "10.00"
                        }
                    ]
                } for c in customers]
        })

    def get_customer_statuses(self, customers) -> BatchCustomerResponse:
        return BatchCustomerResponse(raw_data={
            'existing': customers,
            'deleted': [],
            'pending': []
        })


ExpresslyProvider.register(ProviderBase)
