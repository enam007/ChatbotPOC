# src/mcp/client.py
import aiohttp
import os
import ssl
import certifi
import requests
import asyncio

NODE_API_BASE = os.getenv("API_BASE", "https://engagifii-support-crm.azurewebsites.net/api/v1")

class MCPClient:
    def __init__(self, token: str,verify_ssl: bool = True):
        self.token = token
        print("MCP Client initialized with token:", self.token)
        self.verify_ssl = verify_ssl
    async def request(self, method: str, path: str, **kwargs):
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Tenant-code": "accg",
        }
        url = f"{NODE_API_BASE}{path}"
        ssl_context = None
        if not self.verify_ssl:
            ssl_context = ssl._create_unverified_context()

        print(f"MCPClient making {method} request to {url} with headers {headers} and kwargs {kwargs}")
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, headers=headers, **kwargs) as resp:
                resp.raise_for_status()
                print(f"Response status: {resp.status}")
                print(f"Response headers: {resp}")
                print(f"Response content: {await resp.json()}")
                return await resp.json()
    # async def request(self, method: str, path: str, **kwargs):
    #     url = f"{NODE_API_BASE}{path}"
    #     headers = {
    #         "Authorization": f"Bearer {self.token}",
    #         "Content-Type": "application/json",
    #         "Tenant-code": "accg",
    #         "Accept": "*/*",
    #         "Accept-Encoding": "gzip, deflate",
    #         "User-Agent": "Python/3.11 requests/2.x",
    #         "Host": "engagifii-support-crm.azurewebsites.net",
    #     }

    #     # Run synchronous requests call in a separate thread to keep async
    #     def sync_request():
    #         resp = requests.request(
    #             method=method,
    #             url=url,
    #             headers=headers,
    #             verify=self.verify_ssl,
    #             **kwargs
    #         )
    #         resp.raise_for_status()
    #         return resp.json()

    #     try:
    #         result = await asyncio.to_thread(sync_request)
    #         print(f"Response content: {result}")
    #         return result
    #     except requests.HTTPError as e:
    #         print(f"HTTP Error: {e} - {e.response.text}")
    #         return {"error": f"HTTP {e.response.status_code}"}
    #     except requests.RequestException as e:
    #         print(f"Request Exception: {e}")
    #         return {"error": str(e)}
