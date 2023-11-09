from datetime import datetime, timedelta

from jose import JWTError, jwt

from .claims import Claims


class JWTContext:
    def __init__(self, secret: str, algorithm: str = "HS256") -> None:
        self._secret = secret
        self._algorithm = algorithm

    def encode(
        self,
        sub: str,
    ) -> str:
        claims = {
            "iss": "test-calendar-events",
            "sub": sub,
            "alg": self._algorithm,
            "exp": datetime.utcnow() + timedelta(minutes=30),
        }

        return jwt.encode(claims, self._secret, algorithm=self._algorithm)

    def decode(self, token: str) -> Claims:
        raw_claims = jwt.decode(token, self._secret, algorithms=[self._algorithm])

        return Claims(**raw_claims)

    def verify(self, token: str) -> bool:
        try:
            self.decode(token)
        except JWTError:
            return False
        return True
