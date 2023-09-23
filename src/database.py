# -*- coding: utf-8 -*-

import os
from sqlalchemy.ext.asyncio import create_async_engine


engine = create_async_engine(
    f"postgresql+asyncpg://{os.getenv('POSTGRES_USER')}:" \
    f"{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}/" \
    f"{os.getenv('POSTGRES_DB')}",
    pool_size=100,
    echo=True)
