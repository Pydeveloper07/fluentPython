from typing import Dict
from models import Credentials
import aiohttp


class Connection(object):
    TIMEOUT = aiohttp.ClientTimeout(10)
    BASE_URL = "https://dashboard-api-dev.storfox.com"

    async def get(
            self,
            path: str,
            query: Dict = None,
            headers: Dict = None,
            credentials: Credentials = None
    ) -> Dict:
        """
            Make a get request to Postmen
        """
        return await self.__request('get', path, params=query, headers=headers, credentials=credentials)

    async def put(
            self,
            path: str,
            query: Dict = None,
            body: Dict = None,
            headers: Dict = None,
            credentials: Credentials = None
    ) -> Dict:
        """
            Make a put request to Postmen
        """
        return await self.__request(
            'put',
            path,
            body=body,
            params=query,
            headers=headers,
            credentials=credentials
        )

    async def post(
            self,
            path: str,
            query: Dict = None,
            body: Dict = None,
            headers: Dict = None,
            credentials: Credentials = None
    ) -> Dict:
        """
            Make a post request to Postmen
        """
        return await self.__request(
            'post',
            path,
            body=body,
            params=query,
            headers=headers,
            credentials=credentials
        )

    async def delete(
            self,
            path: str,
            query: Dict = None,
            headers: Dict = None,
            credentials: Credentials = None
    ) -> Dict:
        """
            Make a delete request to Postmen
        """
        return await self.__request(
            'delete',
            path,
            params=query,
            headers=headers,
            credentials=credentials
        )

    async def __request(
            self,
            method: str,
            path: str,
            body: Dict = None,
            params: Dict = None,
            headers: Dict = None,
            credentials: Credentials = None
    ):
        headers = self._get_headers(headers, credentials)
        self.request_body = body
        async with aiohttp.ClientSession(timeout=self.TIMEOUT) as session:
            async with getattr(session, method)(
                    url=self.BASE_URL + path,
                    params=params,
                    json=body,
                    headers=headers,
            ) as resp:
                return await self.get_response(resp)

    @staticmethod
    async def get_response(resp: aiohttp.ClientResponse):
        body = await resp.json()
        if resp.status == 400:
            raise Exception(f"Bad request: {body}")
        if resp.status == 500:
            raise Exception(f"Internal Server Error")
        return body

    @staticmethod
    def _get_headers(headers: dict = None, credentials: Credentials = None):
        _headers = {
            "Accept": "application/json",
        }

        if credentials.access_token:
            _headers['Authorization'] = credentials.access_token

        if isinstance(headers, dict) and any(headers):
            _headers.update(headers)

        return _headers
