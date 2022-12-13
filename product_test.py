import time
from concurrent import futures
from copy import deepcopy

import requests as requests

body = {
  "barcode": "123456789",
  "barcoding_strategy": "each",
  "description": "description of a product",
  "height": 1,
  "images": [
    {
      "image_path": "https://i.picsum.photos/id/1035/200/300.jpg?hmac=744aBtkMLjfDyn2TzkMxsFzw2T0L57TMlNGFlX-Qgq0",
      "is_default": True
    }
  ],
  "length": 1,
  "maximum_retail_price": 1.5,
  "name": "product_name",
  "retail_price": 1,
  "sku": "KS93528TUT",
  "strategy": "fifo",
  "supply_price": 0.8,
  "tags": [
    "tag1",
    "tag2"
  ],
  "track_expiry_dates": True,
  "track_serial_numbers": True,
  "type": "physical",
  "unit_of_measurement": "unit",
  "variants": [
    {
      "barcode": "123456789",
      "barcoding_strategy": "each",
      "description": "description of the variant",
      "enabled": True,
      "height": 1,
      "images": [
        {
          "image_path": "https://i.picsum.photos/id/1035/200/300.jpg?hmac=744aBtkMLjfDyn2TzkMxsFzw2T0L57TMlNGFlX-Qgq0",
          "is_default": True
        }
      ],
      "length": 1,
      "maximum_retail_price": 1.5,
      "name": "variant_name",
      "options": [
        {
          "name": "color",
          "option": "red"
        }
      ],
      "reorder_point": 1,
      "reorder_quantity": 10,
      "retail_price": 1,
      "sku": "KS93528TUT",
      "supply_price": 0.8,
      "unit_of_measurement": "unit",
      "weight": 1,
      "width": 1
    }
  ],
  "weight": 1,
  "width": 1
}

# url = f'https://api-dev.storfox.com/v1/orders/create/'
url = f'https://api-stg.storfox.com/v1/products/create/'
# url = f'https://api.storfox.com/v1/orders/create/'

headers = {
    # "Authorization": "Jc-finV3YYL2bgvP"
    "Authorization": "e_FxT0siMACLHnDG"
    # "Authorization": "JICvPTgO7FYEkVkg"
}


def _create_order(a):
    # time.sleep(a)
    json_body = deepcopy(body)
    json_body.update(barcode=f'test000006-{a}')
    json_body.update(sku=f'test000006-{a}')
    json_body["variants"][0].update(barcode=f'test000006-{a}')
    json_body["variants"][0].update(sku=f'test000006-{a}')
    response = requests.post(url=url, headers=headers, json=json_body)
    print(response.json())
    return response


with futures.ThreadPoolExecutor() as executor:
    executor.map(_create_order, list(range(20)))
