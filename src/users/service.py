from fastapi import HTTPException, status

from src.database import SessionDep
from src.auth.models import User
from src.auth.service import get_password_hash
from src.users.schemas import UserRead, UserCreate

from sqlalchemy import select

async def create_user(session: SessionDep, user_data: UserCreate) -> UserRead:
    user_in_db = await session.execute(select(User).where(User.username == user_data.username))
    user_in_db = user_in_db.scalar_one_or_none()
    if user_in_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    
    hashed_password = get_password_hash(user_data.password)
    user_dict = user_data.model_dump()
    user_dict["hashed_password"] = hashed_password
    user_dict["disabled"] = False  # Default to active user
    del user_dict["password"]
    
    new_user = User(**user_dict)
    session.add(new_user)
    await session.commit()
    return new_user


async def get_all_users(session: SessionDep):
    users = await session.execute(select(User))
    return users.scalars().all()


async def get_user_by_id(session: SessionDep, user_id: int):
    return await session.get(User, user_id)


async def update_user(session: SessionDep, user_id: int, user_data: dict):
    user = await get_user_by_id(session, user_id)
    if user:
        for key, value in user_data.items():
            setattr(user, key, value)
        await session.commit()
    return user


async def delete_user(session: SessionDep, user_id: int):
    user = await get_user_by_id(session, user_id)
    if user:
        await session.delete(user)
        await session.commit()
    return user