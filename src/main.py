from fastapi import FastAPI

from src.randomuser.router import router as randomuser_router
from src.auth.router import router as auth_router

app = FastAPI()
app.include_router(randomuser_router, prefix="/randomuser")
app.include_router(auth_router, prefix="/auth")
