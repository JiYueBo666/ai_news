from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from routers import favorite, history, news, user
from utils.exception import register_exception

app = FastAPI()
register_exception(app)
app.include_router(favorite.router)
app.include_router(history.router)
app.include_router(news.router)
app.include_router(user.router)


origins = [
    "http://localhost:5173",
    "http://localhost",
    "http://your-frontend-domain.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}
