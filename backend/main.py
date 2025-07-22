from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from routers.auth import router as auth_router
from routers.user import router as user_router


app: FastAPI = FastAPI()
app.include_router(router=auth_router)
app.include_router(router=user_router)