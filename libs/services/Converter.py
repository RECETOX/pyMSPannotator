from aiohttp.client_exceptions import ServerDisconnectedError
import requests
from libs.utils.Errors import DataNotRetrieved, ConversionNotSupported


class Converter:
    async def query_the_service(self, service, args, session, method='GET', data=None):
        """
        Make get request to given service with arguments.
        Raises ConnectionError if service is not available.

        :param service: requested service to be queried
        :param args: additional query arguments
        :param method: GET (default) or POST
        :param data: data for POST request
        :return: obtained response
        """
        try:
            result = await self.execute_request(self.services[service] + args, method, data, session)
            return result
        except requests.exceptions.ConnectionError:
            raise ConnectionError(f'Service {service} is not available')

    async def execute_request(self, url, method, data, session, depth=10):
        """
        Execute request with type depending on specified method.

        :param url: service URL
        :param method: GET/POST
        :param data: given arguments for POST request
        :return: obtained response
        """
        try:
            if method == 'GET':
                async with session.get(url=url) as response:
                    result = await response.text()
                    if response.ok:
                        return result
                    elif response.status == 503:
                        if depth > 0:
                            return await self.execute_request(url, method, data, session, depth - 1)
            else:
                async with session.post(url=url, data=data) as response:
                    result = await response.text()
                    if response.ok:
                        return result
                    elif response.status == 503:
                        if depth > 0:
                            return await self.execute_request(url, method, data, session, depth - 1)
        except ServerDisconnectedError:
            if depth > 0:
                return await self.execute_request(url, method, data, session, depth - 1)

    async def convert(self, source, target, data, session):
        """
        Converts specified {source} attribute (provided in {data}) to {target} attribute.

        :param source: given attribute name
        :param target: required attribute name
        :param data: given attribute value
        :param session: current aiohttp session
        :return: obtained value of target attribute
        """
        try:
            result = await getattr(self, f'{source}_to_{target}')(data, session)
            if result:
                return result
            raise DataNotRetrieved(f'Target attribute {target} not available.')
        except AttributeError:
            raise ConversionNotSupported(f'Target attribute {target} is not supported.')
