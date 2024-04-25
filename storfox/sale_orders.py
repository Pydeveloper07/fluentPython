import random
from typing import List, Dict

import utils
from storfox.client import storfox_client, StorfoxClient
import settings


@storfox_client
async def create_sale_orders(n: int, client: StorfoxClient):
    futures = []
    warehouse = await client.get_default_warehouse()
    condition = await client.get_default_condition()
    customer = (await client.get_customers(page=1, limit=1))[0]
    variant_generator = utils.variant_generator(3, client, True)
    for i in range(n):
        print(f"Preparing data for {i+1}/{n}")
        variants = list(await variant_generator.__anext__())
        data = {
            "company": {"guid": settings.COMPANY_GUID},
            "warehouse": {"guid": warehouse["guid"]},
            "customer": {"guid": customer["guid"]},
            "payment_type": random.choice(["cash", "card"]),
            "reference_number": utils.random_str(10),
            "reference_id": utils.random_str(20),
            "billing_address": _get_address(customer["billing_addresses"][0]),
            "delivery_address": _get_address(customer["delivery_addresses"][0]),
            "line_items": _generate_line_items(variants, condition),
        }
        futures.append(client.create_order(data))
    await utils.gather_futures(futures, 7)
    return len(futures)


def _get_address(address_data: Dict):
    return {
        "address": address_data["address"],
        "city": address_data["city"],
        "country": {
            "guid": address_data["country"]["guid"]
        },
        "first_name": address_data["first_name"],
        "last_name": address_data["last_name"],
        "mobile": address_data["mobile"],
        "region": address_data["region"],
        "zipcode": address_data["zipcode"]
    }


def _generate_line_items(variants: List[Dict], condition: Dict):
    results = []
    for variant in variants:
        data = {
            "condition": {"guid": condition["guid"]},
            "discount": random.randint(0, 10),
            "price": random.randint(1000, 10000),
            "quantity": random.randint(1, 3),
            "tax": random.randint(0, 10),
            "variant": {
                "type": "variant",
                "guid": variant["guid"],
                "sku": variant["sku"],
            },
        }
        results.append(data)
    return results
