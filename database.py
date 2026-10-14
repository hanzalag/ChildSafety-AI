from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from config import settings

engine = create_async_engine(
    settings.database_url, 
    echo=settings.debug, 
    connect_args={"check_same_thread": False}
)

async_session_maker = async_sessionmaker(
    engine, 
    expire_on_commit=False,
    class_=AsyncSession
)

class Base(AsyncAttrs, DeclarativeBase):
    pass

async def get_db():
    async with async_session_maker() as session:
        yield session

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)