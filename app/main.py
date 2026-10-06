from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.db.database import get_db, engine
from app.api.routes import user, profile, auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        print("Database connection established")

    except Exception as e:
        print("Database connection failed:", e)
        raise

    yield

    # Shutdown
    print("Application shutting down")


app = FastAPI(
    description="This is a user management API that allows you to create, read, update, and delete user information.",
    title="User Management API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the User Management API!"}

app.include_router(user.router)
app.include_router(profile.router)
app.include_router(auth.router)