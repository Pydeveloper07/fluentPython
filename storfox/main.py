import asyncio
from products import create_products, update_products
from locations import create_locations
from adjustments import create_adjustments, create_and_complete_adjustments
from sale_orders import create_sale_orders
from concurrent import futures
import multiprocessing
import utils


CREDENTIALS = {
    "access_token": "S7XhXYBb3dBEJGuu6ng3TIlUEd2OYaftq3h2QmCkjeC75Rg2"
}
PRODUCTS = 500
LOCATIONS = 100
SALE_ORDERS = 1


async def main():
    # print(f"Creating {PRODUCTS} products...")
    # count = await create_products(PRODUCTS, credentials=CREDENTIALS)
    # print(f"Created {count} products!")
    # print(f"Updating {PRODUCTS} products...")
    # count = await update_products(credentials=CREDENTIALS)
    # print(f"Updated {count} products!")
    # print(f"Creating {LOCATIONS} locations...")
    # count = await create_locations(LOCATIONS, credentials=CREDENTIALS)
    # print(f"Created {count} locations!")
    # print(f"Creating Adjustments...")
    # count = await create_adjustments(credentials=CREDENTIALS)
    # print(f"Created and completed {count} adjustments...")
    # print(f"Creating sale orders...")
    # await create_sale_orders(SALE_ORDERS, credentials=CREDENTIALS)
    # await asyncio.gather(
    #     create_sale_orders(SALE_ORDERS, credentials=CREDENTIALS),
    #     create_sale_orders(SALE_ORDERS, credentials=CREDENTIALS),
    #     create_sale_orders(SALE_ORDERS, credentials=CREDENTIALS),
    # )
    print(f"Created {SALE_ORDERS} sale orders...")


if __name__ == "__main__":
    asyncio.run(main())

