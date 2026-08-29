"""
定义Http客户端
IO/网络传输 使用异步
同步,异步
"""
from httpx import AsyncClient

http_client: AsyncClient | None = None

def init_http_client():
    global http_client
    http_client = AsyncClient(timeout=120)

async def dispose_http_client():
    await http_client.aclose()


if __name__ == "__main__":
    init_http_client()
    dispose_http_client()



