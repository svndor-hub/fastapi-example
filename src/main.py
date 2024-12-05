from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.randomuser.router import router as randomuser_router
from src.auth.router import router as auth_router
from src.users.router import router as users_router

app = FastAPI()
app.include_router(randomuser_router, prefix="/randomuser")
app.include_router(auth_router)
app.include_router(users_router, prefix="/users")

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)