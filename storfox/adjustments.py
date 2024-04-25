import random
from typing import List
import utils
from storfox.client import storfox_client, StorfoxClient
import settings


@storfox_client
async def create_adjustments(client: StorfoxClient):
    condition = await client.get_default_condition()
    warehouse = await client.get_default_warehouse()
    locations = await client.get_locations(
        query={
            "location_type": "picking",
            "warehouse_id": warehouse["id"],
        },
        limit=100
    )
    reasons = await client.get_adjustment_reasons(query={"operation": "add"})
    async for products in utils.product_generator(10, client):
        futures = []
        for product in products:
            variants = await client.get_variants(query={"product_id": product["id"]}, limit=3)
            location = random.choice(locations)
            reason = random.choice(reasons)
            data = {
                "owner": {"id": settings.COMPANY_ID},
                "warehouse": {"id": warehouse["id"]},
                "reason": {"id": reason["id"]},
                "line_items": await _generate_line_items(variants, condition, location, client),
            }
            futures.append(client.create_adjustments(data))
        await utils.gather_futures(futures)
    return


@storfox_client
async def create_and_complete_adjustments(client: StorfoxClient):
    condition = await client.get_default_condition()
    warehouse = await client.get_default_warehouse()
    locations = await client.get_locations(
        query={
            "location_type": "picking",
            "warehouse_id": warehouse["id"],
        },
        limit=100
    )
    reasons = await client.get_adjustment_reasons(query={"operation": "add"})
    async for products in utils.product_generator(10, client):
        futures = []
        for product in products:
            variants = await client.get_variants(query={"product_id": product["id"]}, limit=3)
            location = random.choice(locations)
            reason = random.choice(reasons)
            data = {
                "owner": {"id": settings.COMPANY_ID},
                "warehouse": {"id": warehouse["id"]},
                "reason": {"id": reason["id"]},
                "line_items": await _generate_line_items(variants, condition, location, client),
            }
            futures.append(client.create_and_complete_adjustments(data))
        await utils.gather_futures(futures)
    return


async def _generate_line_items(variants: List[dict], condition: dict, location: dict, client: StorfoxClient):
    results = []
    for variant in variants:
        data = {
            "expires_at": None,
            "price": random.randint(1000, 10000),
            "quantity": random.randint(50, 100),
            "variant": {"id": variant["id"]},
            "location": {"id": location["id"]},
            "units": []
        }
        data["units"].append({
            "unit_number": variant["barcode"],
            "quantity": data["quantity"],
            "condition": {"id": condition["id"]}
        })
        results.append(data)
    return results
