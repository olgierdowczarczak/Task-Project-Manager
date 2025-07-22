from passlib.context import CryptContext
import os


pwd_context: CryptContext = CryptContext(schemes=[os.environ.get("CRYPT_SCHEME")], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(secret=plain_password, hash=hashed_password)

def get_hashed_password(plain_password: str) -> str:
    return pwd_context.hash(secret=plain_password)