from copy import deepcopy
from functools import reduce

import settings
import utils
import random
from client import storfox_client, StorfoxClient
import itertools


@storfox_client
async def create_products(n: int, client: StorfoxClient):
    futures = []
    for i in range(n):
        data = {
            "company": {"id": settings.COMPANY_ID},
            "name": "TEST-" + utils.random_str(10),
            "sku": "test-" + utils.random_str(10),
            "barcode": "test-" + utils.random_str(10),
            "type": "physical",
            "strategy": "fifo",
            "barcoding_strategy": "set",
            "retail_price": random.randint(1000, 10000),
            "supply_price": random.randint(1000, 10000),
            "maximum_retail_price": random.randint(1000, 10000),
        }
        futures.append(client.create_product(data))

    await utils.gather_futures(futures, chunk_size=15)
    return len(futures)


@storfox_client
async def update_products(client: StorfoxClient):
    all_products = await client.get_products(query=dict(ordering="-id"), limit=500)
    futures = []
    for product in all_products:
        data = {
            "id": product["id"],
            "company": {"id": product["company"]["id"]},
            "name": product["name"],
            "sku": product["sku"],
            "barcode": product["barcode"],
            "type": product["type"],
            "strategy": product["strategy"],
            "retail_price": product["retail_price"],
            "supply_price": product["supply_price"],
            "maximum_retail_price": product["maximum_retail_price"],
            "options": [
                {
                    "name": "Color",
                    "options": ["Red", "Green", "Blue"]
                },
                {
                    "name": "Size",
                    "options": ["S", "M", "L"]
                },
                {
                    "name": "Material",
                    "options": ["Stainless Steel", "Titanium", "Aluminium"]
                }
            ]
        }
        data["variants"] = _generate_variants(product, data)
        futures.append(client.update_product(data))

    await utils.gather_futures(futures, chunk_size=5)
    return len(futures)


def _generate_variants(product: dict, data: dict):
    results = []
    options = deepcopy(data["options"])
    for i, option in enumerate(options):
        new_option = []
        for _option in option["options"]:
            new_option.append(
                {
                    "name": option["name"],
                    "option": _option,
                }
            )
        options[i] = new_option
    combined_options = itertools.product(*options)
    for combination in combined_options:
        variant_data = {
            "name": product["name"] + reduce(lambda x, y: x + y["option"], ["", *combination]),
            "enabled": True,
            "is_cross_docking": False,
            "sku": utils.random_str(20),
            "barcode": utils.random_str(20),
            "retail_price": random.randint(1000, 10000),
            "supply_price": random.randint(1000, 10000),
            "maximum_retail_price": random.randint(1000, 10000),
        }
        results.append(variant_data)
    return results
