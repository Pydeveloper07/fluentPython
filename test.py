import json
import typing
from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin
from order_body import SallaOrderData
import warnings

json_str = '{"event": "order.created", "merchant": 1581966835, "created_at": "Tue May 24 2022 09:24:17 GMT+0300", "data": {"id": 112775398, "reference_id": 36095043, "urls": {"customer": "https://salla.sa/dev-dn8hj2i8gowyymog/checkout/lm6bowYMnmA9eyWdLkJza153vyz1dg3qQO0GZ7NxDlVKXB4grqR82jEN", "admin": "https://s.salla.sa/orders/order/klRqD3PJ4yzYaBg40kpW0NALj58ZVQgK"}, "source": "dashboard", "source_device": "desktop", "date": {"date": "2022-05-24 09:24:14.000000", "timezone_type": 3, "timezone": "Asia/Riyadh"}, "first_complete_at": null, "status": {"id": 1473353380, "name": "Awaiting Payment", "slug": "payment_pending"}, "payment_method": "waiting", "currency": "SAR", "amounts": {"sub_total": {"amount": 89, "currency": "SAR"}, "shipping_cost": {"amount": 0, "currency": "SAR"}, "cash_on_delivery": {"amount": 0, "currency": "SAR"}, "tax": {"percent": "0.00", "amount": {"amount": 0, "currency": "SAR"}}, "discounts": [], "total": {"amount": 89, "currency": "SAR"}}, "shipping": {"id": 1458656926, "app_id": null, "company": "TEST", "logo": "", "receiver": {"name": "Del Don", "email": "xdel1010@gmail.com", "phone": "971555555555"}, "shipper": {"name": "Demo", "company_name": "dev-dn8hj2i8gowyymog", "email": "dn8hj2i8gowyymog@email.partners", "phone": "966500000000"}, "pickup_address": {"country": "Saudi Arabia", "country_code": "SA", "city": "Mecca", "shipping_address": "Mecca,Saudi Arabia", "street_number": null, "block": null, "postal_code": null, "geo_coordinates": {"lat": 21.3825905096851, "lng": 39.77319103068542}}, "address": {"country": "SA", "country_code": "SA", "city": "Riyadh Airport", "shipping_address": " \\u0634\\u0627\\u0631\\u0639 test\\u060c \\u0627\\u0644\\u062d\\u064a Test 12121\\u060c, Riyadh Airport, Saudi Arabia", "street_number": "test", "block": "Test", "postal_code": "12121", "geo_coordinates": {"lat": 0, "lng": 0}}, "shipment": {"id": "0", "pickup_id": null, "tracking_link": "0", "label": []}, "policy_options": []}, "can_cancel": false, "can_reorder": false, "is_pending_payment": true, "pending_payment_ends_at": 172796, "checkout_url": "https://salla.sa/dev-dn8hj2i8gowyymog/checkout/lm6bowYMnmA9eyWdLkJza153vyz1dg3qQO0GZ7NxDlVKXB4grqR82jEN", "pending_payment_start_at": {"date": "2022-05-25 09:24:14.000000", "timezone_type": 3, "timezone": "Asia/Riyadh"}, "shipment_branch": [], "customer": {"id": 1550968832, "first_name": "Del", "last_name": "Don", "mobile": 555555555, "mobile_code": "+971", "email": "xdel1010@gmail.com", "urls": {"customer": "https://salla.sa/dev-dn8hj2i8gowyymog/profile", "admin": "https://s.salla.sa/customers/rEwgmvek0zQVGMvOovm18RX9qY7LPNoZ"}, "avatar": "https://s.salla.sa/cp/assets/images/avatar_male.png", "gender": "male", "birthday": {"date": "2022-05-04 00:00:00.000000", "timezone_type": 3, "timezone": "Asia/Riyadh"}, "city": "", "country": "United Arab Emirates", "country_code": null, "currency": "SAR", "location": "", "updated_at": {"date": "2022-05-24 09:24:07.000000", "timezone_type": 3, "timezone": "Asia/Riyadh"}}, "items": [{"id": 1392610480, "name": "\\u0628\\u0644\\u0648\\u0632\\u0629", "sku": "15504463-10000031180-", "quantity": 1, "currency": "SAR", "weight": 0.25, "amounts": {"price_without_tax": {"amount": 89, "currency": "SAR"}, "total_discount": {"amount": 0, "currency": "SAR"}, "tax": {"percent": "0.00", "amount": {"amount": 0, "currency": "SAR"}}, "total": {"amount": 89, "currency": "SAR"}}, "notes": "", "product": {"id": 90887484, "type": "product", "promotion": {"title": null, "sub_title": null}, "status": "sale", "is_available": true, "sku": "15504463-10000031180-", "name": "\\u0628\\u0644\\u0648\\u0632\\u0629", "price": {"amount": 89, "currency": "SAR"}, "sale_price": {"amount": 89, "currency": "SAR"}, "currency": "SAR", "url": "https://salla.sa/dev-dn8hj2i8gowyymog/\\u0628\\u0644\\u0648\\u0632\\u0629/p90887484", "thumbnail": "https://salla-dev.s3.eu-central-1.amazonaws.com/nWzD/zbgJtlRIcJ81ExBMmNZX8X3KVZVPM2Hzmi4vleMI.jpg", "has_special_price": true, "regular_price": {"amount": 179, "currency": "SAR"}, "calories": null, "mpn": null, "gtin": null, "favorite": null}, "options": [{"id": 215685696, "product_option_id": 1525854233, "name": "\\u0627\\u0644\\u0645\\u0642\\u0627\\u0633", "type": "radio", "value": {"id": 677096036, "name": "44 - XL", "price": {"amount": 0, "currency": "SAR"}}}], "images": [], "codes": [], "files": []}], "bank": null, "tags": []}}'


def number_of_fields(data: dict) -> typing.Tuple[int, typing.Set]:
    total = 0
    keys = set()
    for key, value in data.items():
        keys.add(key)
        total += 1
        if isinstance(value, dict):
            total_temp, keys_temp = number_of_fields(value)
            total += total_temp
            keys.update(keys_temp)
    return total, keys


def number_of_fields_data_class(data: object) -> typing.Tuple[int, typing.Set]:
    total = 0
    keys = set()
    for key, value in data.__dict__.items():
        total += 1
        keys.add(key)
        type_ = None
        try:
            value.__dict__
            type_ = 'object'
        except Exception:
            pass
        if type_ == 'object':
            total_temp, keys_temp = number_of_fields_data_class(value)
            total += total_temp
            keys.update(keys_temp)
    return total, keys


def convert(data):
    data_dict = json.loads(data)
    order_body = SallaOrderData.from_json(data, infer_missing=True)
    no_keys, keys = number_of_fields_data_class(order_body)
    no_keys_1, keys_1 = number_of_fields(data_dict)
    keys_diff = keys_1 - keys
    print(keys_diff)
    print(len(keys_diff))


if __name__ == "__main__":
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        convert(json_str)
