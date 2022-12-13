import hashlib
import base64
import json
import j_t_order as order_data


PWD_KEY = "RQTWq741"
PRIVATE_KEY = "13a50881019a4082aa46c1e12b99f931"


def _generate_business_signature(customer_code: str,  password: str) -> bytes:
    pwd = hashlib.md5(f"{password}{PWD_KEY}".encode()).hexdigest().upper()
    signature = base64.b64encode(hashlib.md5(f"{customer_code}{pwd}{PRIVATE_KEY}".encode()).digest())
    return signature


def _generate_header_signature(json_data) -> bytes:
    data = f"{json_data}{PRIVATE_KEY}"
    signature = base64.b64encode(hashlib.md5(data.encode()).digest())
    return signature


def _order_create_request():
    business_signature = _generate_business_signature("J0086024173", "Aa123456")
    order_data.order_data["digest"] = business_signature.decode()
    json_data = json.dumps(order_data.order_data)
    header_signature = _generate_header_signature(json_data)
    print(business_signature.decode())
    print(header_signature.decode())
    print(json_data)


def _order_check_request():
    business_signature = _generate_business_signature("J0086024173", "Aa123456")
    order_data.order_check_data["digest"] = business_signature.decode()
    json_data = json.dumps(order_data.order_check_data)
    header_signature = _generate_header_signature(json_data)
    print(business_signature.decode())
    print(header_signature.decode())
    print(json_data)


def _waybill_get_request():
    business_signature = _generate_business_signature("J0086024173", "Aa123456")
    order_data.waybill_get_data["digest"] = business_signature.decode()
    json_data = json.dumps(order_data.waybill_get_data)
    header_signature = _generate_header_signature(json_data)
    print(business_signature.decode())
    print(header_signature.decode())
    print(json_data)


def _order_cancel_request():
    business_signature = _generate_business_signature("J0086024173", "Aa123456")
    order_data.order_cancel_data["digest"] = business_signature.decode()
    json_data = json.dumps(order_data.order_cancel_data)
    header_signature = _generate_header_signature(json_data)
    print(business_signature.decode())
    print(header_signature.decode())
    print(json_data)


def main():
    _order_check_request()


if __name__ == "__main__":
    main()
