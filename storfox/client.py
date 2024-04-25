from connection import Connection
from models import Credentials


def storfox_client(func):
    async def wrapper(*args, **kwargs):
        try:
            assert kwargs.get("credentials")
            client = StorfoxClient(kwargs.pop("credentials"))
            return await func(*args, **kwargs, client=client)
        except Exception:
            print(client.connection.request_body)
            raise

    return wrapper


class StorfoxClient(object):
    PRODUCT_CREATE_URL = "/v1/products/create/"
    PRODUCT_UPDATE_URL = "/v1/products/update/{id}/"
    PRODUCT_LIST_URL = "/v1/products/list/"
    VARIANT_LIST_URL = "/v1/variants/list/"
    CONDITION_LIST_URL = "/v1/conditions/list/"
    WAREHOUSE_LIST_URL = "/v1/warehouses/list/"
    AREA_LIST_URL = "/v1/areas/list/"
    LOCATION_LIST_URL = "/v1/locations/list/"
    LOCATION_CREATE_URL = "/v1/locations/create/"
    ADJUSTMENT_CREATE_URL = "/v1/stock/adjustments/create/"
    ADJUSTMENT_CREATE_AND_COMPLETE_URL = "/v1/stock/adjustments/create-and-complete/"
    ADJUSTMENT_REASON_LIST_URL = "/v1/stock/adjustment-reasons/list/"
    CUSTOMER_LIST_URL = "/v1/orders/customers/list/"
    SALE_ORDER_CREATE_URL = "/v1/orders/create/"

    def __init__(self, credentials: dict):
        self.connection = Connection()
        self.credentials = Credentials(**credentials)

    async def create_product(self, data: dict):
        resp = await self.connection.post(
            path=self.PRODUCT_CREATE_URL,
            body=data,
            credentials=self.credentials
        )
        return resp

    async def update_product(self, data: dict):
        resp = await self.connection.put(
            path=self.PRODUCT_UPDATE_URL.format(id=data["id"]),
            body=data,
            credentials=self.credentials
        )
        return resp

    async def create_adjustments(self, data: dict):
        resp = await self.connection.post(
            path=self.ADJUSTMENT_CREATE_URL,
            body=data,
            credentials=self.credentials
        )
        return resp

    async def create_and_complete_adjustments(self, data: dict):
        resp = await self.connection.post(
            path=self.ADJUSTMENT_CREATE_AND_COMPLETE_URL,
            body=data,
            credentials=self.credentials
        )
        return resp

    async def create_location(self, data: dict):
        resp = await self.connection.post(
            path=self.LOCATION_CREATE_URL,
            body=data,
            credentials=self.credentials
        )
        return resp

    async def create_order(self, data: dict):
        resp = await self.connection.post(
            path=self.SALE_ORDER_CREATE_URL,
            body=data,
            credentials=self.credentials
        )
        return resp

    async def get_products(self, query: dict = None, page: int = 1, limit: int = 10):
        _query = {
            "page": page,
            "limit": limit,
        }
        if query:
            _query.update(query)

        resp = await self.connection.get(
            path=self.PRODUCT_LIST_URL,
            query=_query,
            credentials=self.credentials
        )
        return resp["results"]

    async def get_customers(self, query: dict = None, page: int = 1, limit: int = 10):
        _query = {
            "page": page,
            "limit": limit,
        }
        if query:
            _query.update(query)

        resp = await self.connection.get(
            path=self.CUSTOMER_LIST_URL,
            query=_query,
            credentials=self.credentials
        )
        return resp["results"]

    async def get_areas(self, query: dict = None, page: int = 1, limit: int = 10):
        _query = {
            "page": page,
            "limit": limit,
        }
        if query:
            _query.update(query)

        resp = await self.connection.get(
            path=self.AREA_LIST_URL,
            query=_query,
            credentials=self.credentials
        )
        return resp["results"]

    async def get_variants(self, query: dict = None, page: int = 1, limit: int = 10):
        _query = {
            "page": page,
            "limit": limit,
        }
        if query:
            _query.update(query)

        resp = await self.connection.get(
            path=self.VARIANT_LIST_URL,
            query=_query,
            credentials=self.credentials
        )
        return resp["results"]

    async def get_default_condition(self):
        resp = await self.connection.get(
            path=self.CONDITION_LIST_URL,
            query={
                "is_default": "true"
            },
            credentials=self.credentials
        )
        return resp["results"][0]

    async def get_default_warehouse(self):
        resp = await self.connection.get(
            path=self.WAREHOUSE_LIST_URL,
            query={
                "is_default": "true"
            },
            credentials=self.credentials
        )
        return resp["results"][0]

    async def get_locations(
            self, query: dict = None, page: int = 1, limit: int = 10
    ):
        _query = {
            "page": page,
            "limit": limit,
        }
        if query:
            _query.update(query)

        resp = await self.connection.get(
            path=self.LOCATION_LIST_URL,
            query=_query,
            credentials=self.credentials
        )
        return resp["results"]

    async def get_adjustment_reasons(self, query: dict = None, page: int = 1, limit: int = 10):
        _query = {
            "page": page,
            "limit": limit,
        }
        if query:
            _query.update(query)

        resp = await self.connection.get(
            path=self.ADJUSTMENT_REASON_LIST_URL,
            query=_query,
            credentials=self.credentials
        )
        return resp["results"]
