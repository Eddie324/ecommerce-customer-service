"""
定义Http客户端
IO/网络传输 使用异步
同步,异步
"""
import asyncio
from httpx import AsyncClient

http_client: AsyncClient | None = None

def init_http_client():
    global http_client
    http_client = AsyncClient(timeout=120)

async def dispose_http_client():
    await http_client.aclose()

async def main():
    init_http_client()

    response = await http_client.get(url="https://192.168.200.120:18081/orders/A20260410001")

    data = response.json()

    print(data)

if __name__ == "__main__":
    asyncio.run(main())



