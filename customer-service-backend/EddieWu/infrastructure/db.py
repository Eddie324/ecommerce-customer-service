"""
操作数据库的session会话
引擎 session (session.execute())
"""
import asyncio
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, async_sessionmaker, create_async_engine
from EddieWu.config.settings import settings

engine:AsyncEngine | None = None

session_factory: async_sessionmaker[AsyncSession] | None = None

def init_db_engine():
    """
    expire_on_commit:True 提交后自动过期

    update user set user.name="Eddie" where user.id="1001"

    commit--刷盘

    user.name(读)---->查询数据库获取最新的,需要在同步环境下
    await user.name---->报错
    :return:
    """
    global engine
    engine = create_async_engine(settings.database_url, echo=True)

    session_factory = async_sessionmaker(engine, expire_on_commit=False) # 不过期,从内存中获取数据

async def dispose_engine():
     await engine.dispose()

async def main():
    await init_db_engine()
    async with session_factory() as session:
         result = await session.execute(text("select 1")) # 防止sql注入
         print(result.fetchone())


if __name__ == "__main__":
    asyncio.run(main())
