from passlib.context import CryptContext


class HashInCryptContext:
    def __init__(self, schemes: list[str] | None = None) -> None:
        if not schemes:
            schemes = ["bcrypt"]

        self._crypt_context = CryptContext(schemes=schemes, deprecated="auto")

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        return self._crypt_context.verify(plain_password, hashed_password)

    def hash(self, password: str) -> str:
        return self._crypt_context.hash(password)
