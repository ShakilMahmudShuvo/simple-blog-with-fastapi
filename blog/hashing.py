from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher:
    def bcrypt_hash(password: str) :
        return pwd_context.hash(password)
