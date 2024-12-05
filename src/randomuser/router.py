from fastapi import APIRouter, HTTPException
import httpx

from src.database import SessionDep
from src.users.schemas import UserCreate
from src.users.service import create_user

API_URL = "https://randomuser.me/api/"

router = APIRouter()

@router.get("/test")
async def test():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(API_URL)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/save")
async def save_random_user(session: SessionDep):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(API_URL)
        response.raise_for_status()
        random_user = response.json()["results"][0]
        user = UserCreate(
            username=random_user["login"]["username"],
            email=random_user["email"],
            password=random_user["login"]["password"],
        )

        db_user = await create_user(session, user)
        return db_user

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=str(e))
