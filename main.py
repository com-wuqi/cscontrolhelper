from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from .routers import user as user_router
from .routers import admin as admin_router
from .routers import sse as sse_router

from .depends import create_db_and_tables
from contextlib import asynccontextmanager


#可以像访问系统环境变量一样使用 .env 文件中的变量，例如 os.getenv(key, default=None)

@asynccontextmanager
async def lifespan(_: FastAPI):
    create_db_and_tables()
    yield



app = FastAPI(debug=True,lifespan=lifespan)

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user_router.router)
app.include_router(admin_router.router)
app.include_router(sse_router.router)


@app.get("/")
async def read_root():
    return {"Hello": "World"}

