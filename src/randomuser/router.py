from fastapi import APIRouter, HTTPException
import httpx

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
