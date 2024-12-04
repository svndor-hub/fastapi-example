from typing import Any, AsyncGenerator, Annotated

from sqlalchemy import (
    CursorResult,
    Insert,
    Select,
    Update,
)

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.exc import SQLAlchemyError

from src.config import settings

from fastapi import Depends

DATABASE_URL = str(settings.DATABASE_ASYNC_URL)

engine = create_async_engine(
    DATABASE_URL,
    pool_size=settings.DATABASE_POOL_SIZE,
    pool_recycle=settings.DATABASE_POOL_TTL,
    pool_pre_ping=settings.DATABASE_POOL_PRE_PING,
)

async_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def fetch_one(
    select_query: Select | Insert | Update,
    connection: AsyncSession,
    commit_after: bool = False,
) -> dict[str, Any] | None:
    cursor = await _execute_query(select_query, connection, commit_after)
    if cursor is None:
        return None
    result = cursor.scalar_one_or_none()
    return result._asdict() if result else None


async def fetch_all(
    select_query: Select | Insert | Update,
    connection: AsyncSession,
    commit_after: bool = False,
) -> list[dict[str, Any]]:
    cursor = await _execute_query(select_query, connection, commit_after)
    if cursor is None:
        return []
    rows = cursor.scalars.all()
    return [r._asdict() for r in rows] if rows else []


async def execute(
    query: Insert | Update,
    connection: AsyncSession,
    commit_after: bool = False,
) -> None:
    await _execute_query(query, connection, commit_after)


async def _execute_query(
    query: Select | Insert | Update,
    connection: AsyncSession,
    commit_after: bool = False,
) -> CursorResult:
    try:
        result = await connection.execute(query)
        if commit_after:
            await connection.commit()
        return result
    except SQLAlchemyError as e:
        print(f"Error executing query: {e}")
        return None  # Return None if there's an error


async def get_db_connection() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_db_connection)]
