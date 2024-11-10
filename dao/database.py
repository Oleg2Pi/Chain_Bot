import logging
from os import getenv

from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

postgres_url = URL.create(
    "postgresql+asyncpg",
    username=getenv('DB.USERNAME'),
    password=getenv('DB.PASSWORD'),
    host="localhost",
    port=5432,
    database=getenv('DB.DATABASE'),
)

async_engine = create_async_engine(postgres_url, echo=True, pool_pre_ping=True)

session_maker = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)
