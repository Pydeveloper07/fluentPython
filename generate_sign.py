import hashlib
import json
import time

body = {
    "customerId": "C21018335",
    "accessToken": "baf87a62-4db0-4687-93f6-93e8133276e6",
    "format": "json",
    "signMethod": "MD5",
    "timeZone": "+05",
    "version": "1.0.0",
    "param": {
        # "grantType": "clientCredential"
        "orderCode": "ML0978234091957",
        "orderType": "100",
        "oldExpressNo": "",
        "consignor": "Zeta",
        "consignorAddress": "Tabuk, City: P.O.Box 1799".replace(', ', ',').replace(": ", ":"),
        "consignee": "John Snow",
        "consigneeContact": "Fredy",
        "consigneeMobile": "",
        "consigneePhone": "9254564578",
        "consigneeEmail": "419663405@qq.com",
        "consigneeCountry": "KSA",
        "consigneeProvince": "",
        "consigneeCity": "Jeddah Rabigh",
        "consigneeArea": "test",
        "consigneeSuburb": "EFGH",
        "consigneeZipCode": "80184",
        "consigneeStreet": "Tabuk, City: P.O.Box 1799".replace(', ', ',').replace(": ", ":"),
        "consigneeExternalNo": "100",
        "consigneeInternalNo": "Mp88",
        "consigneeAddress": "Tabuk City P.O.Box 1799",
        "consigneeLongitude": "116.511446",
        "consigneeLatitude": "39.847769",
        "goodsValue": "10",
        "collectingMoney": "30",
        "paymentMethod": "200",
        "totalCount": "1",
        "totalWeight": "3.500",
        "totalVolume": 0,
        "skuTotal": 2,
        "skuName": "test2",
        "skuZh": "鞋子",
        "deliveryRequirements": "",
        "orderDescription": "",
        "buyerId": "",
        "platform": "",
        "isInsurance": 0,
        "pickDate": "",
        "pickType": "0",
        "batterType": "",
        "currency": "Local",
        "isSupportUnpack": 1,
        "consignorJoinFrom": "FC",
        "returnAddressInfo": {
            "contactCompany": "test-company"
        },
        "skuDetailList": [
            {
                "skuName": "vbvvvv",
                "skuNo": "",
                "skuDesc": "",
                "skuQty": "1",
                "skuGoodsValue": "20",
                "skuUrl": ""
            },
            {
                "skuName": "dfasdfds",
                "skuNo": "",
                "skuDesc": "",
                "skuQty": 1,
                "skuGoodsValue": "10",
                "skuUrl": ""
            }
        ]
    }
}

secretKey = "MIICdwIBADANBgkqhkiG9w0BAQEFAASCAmEwggJdAgEAAoGBAIW79Stj/8n3Ze1x"


def md5_zh(password):
    ps = hashlib.md5()
    ps.update(password.encode(encoding='utf-8'))
    return ps.hexdigest().upper()


def _get_body():
    timestamp = time.time()
    print(int(timestamp))
    body["timestamp"] = int(timestamp)
    md5_list = [secretKey]
    keys = sorted([k for k in body.keys() if k not in ['param', 'sign']])
    for i, key in enumerate(keys):
        md5_list.append(key)
        md5_list.append(str(body[key]))
    md5_list.append(str(json.dumps(body["param"], ensure_ascii=False)).replace(': ', ':').replace(', ', ','))
    md5_list.append(secretKey)
    md5_str = ''.join(md5_list)

    sign = md5_zh(md5_str)
    body["sign"] = sign
    return body


if __name__ == "__main__":
    import requests

    url = "https://openapi.52imile.cn/client/order/createOrder"
    # url = "https://openapi.52imile.cn/auth/accessToken/grant"

    body = _get_body()
    response = requests.post(url, json=body)
    print(response.json())
