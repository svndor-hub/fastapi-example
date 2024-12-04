from fastapi import APIRouter, HTTPException, status

from src.auth.models import User
from src.users.schemas import UserCreate, UserRead
from src.database import SessionDep
from src.users.service import *

router = APIRouter()


@router.post("/", response_model=UserRead)
async def create_new_user(user: UserCreate, session: SessionDep):
    db_user = await create_user(session, user)
    return db_user


@router.get("/", response_model=list[UserRead])
async def get_users(session: SessionDep):
    return await get_all_users(session)


@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: int, session: SessionDep):
    user = await get_user_by_id(session, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserRead)
async def update_existing_user(user_id: int, user: UserCreate, session: SessionDep):
    db_user = await update_user(session, user_id, user.model_dump())
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_user(user_id: int, session: SessionDep):
    db_user = await delete_user(session, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
