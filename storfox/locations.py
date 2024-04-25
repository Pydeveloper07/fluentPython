import random

from storfox.client import storfox_client, StorfoxClient
import utils


@storfox_client
async def create_locations(n: int, client: StorfoxClient):
    warehouse = await client.get_default_warehouse()
    areas = await client.get_areas(query={"warehouse_id": warehouse["id"]})
    futures = []
    for i in range(n):
        area = random.choice(areas)
        data = {
            "warehouse": {"guid": warehouse["guid"]},
            "area": {"guid": area["guid"]},
            "aisle": str(random.randint(1, 999)),
            "bay": str(random.randint(1, 999)),
            "level": str(random.randint(1, 999)),
            "bin": str(random.randint(1, 999)),
            "location_type": "picking",
            "allowed_operations": ["picking", "putaway"],
            "status": "active",
        }
        futures.append(client.create_location(data))

    await utils.gather_futures(futures)
    return len(futures)
