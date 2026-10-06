from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash 

from dotenv import load_dotenv
import os

from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY


load_dotenv()  # This line loads environment variables from a .env file into the application's environment, allowing you to access sensitive information like secret keys and database credentials without hardcoding them into your code.



password_hash = PasswordHash.recommended()   # This line creates a recommended password hashing algorithm instance using the pwdlib library. The recommended() method selects a secure and up-to-date hashing algorithm for password storage.


def hash_password(password: str) -> str:     # This function takes a plain-text password as input and returns its hashed version using the password_hash instance created earlier. The hash() method applies the selected hashing algorithm to the password, ensuring that it is securely stored in the database.
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:       # This function takes a plain-text password and a hashed password as input and verifies if the plain-text password matches the hashed version. It returns True if the passwords match and False otherwise. The verify() method checks the provided password against the stored hash, ensuring that the authentication process is secure.
    return password_hash.verify(password, hashed_password)


def create_access_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "exp": expire
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token

def verify_access_token(token: str) -> dict:
    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )

    return payload
