from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker
from app.models.user import Base, User  #Just imported User to add the User model into the Base.metadata.create_all(engine) call, which creates the users table in the database.
from app.models.profile import Profile  # Import the Profile model to include it in the database schema

from app.core.config import DATABASE_URL  # Import the DATABASE_URL from the config module to use it for creating the database engine
from sqlalchemy import select


engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20
    )                           #engine : SQLAlchemy's main connection/communication mechanism with the database

Base.metadata.create_all(engine)      #This line creates the tables in the database based on the models defined in the Base class. It checks if the tables already exist and creates them if they don't.

SessionLocal = sessionmaker(           #sessionmaker is a factory for creating new Session objects, which are used to interact with the database.
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    db = SessionLocal() # This line creates a new database session using the SessionLocal factory. The session is used to interact with the database, allowing you to perform operations like adding, querying, and committing changes to the database.

    try:
        yield db  # This line yields the database session to the caller, allowing them to use it for database operations. The session will be closed after the caller is done using it.
    finally:
        db.close()


# engine → communicates with PostgreSQL
# SessionLocal → creates database sessions
# Session → performs database work
# db.add() → adds an object to the session
# db.commit() → commits changes
# db.close() → closes the session
# flush → sends pending SQL without committing
# autoflush=False → gives us explicit control over flushing


# All users : select(User)
# Filter users : select(User).where(User.email == "test@example.com")
# Execute : result = db.execute(stmt)
# Get objects : result.scalars().all() and result.scalars().first()
