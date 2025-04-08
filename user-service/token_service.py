from abc import abstractmethod, ABC
from datetime import datetime, UTC, timedelta
import jwt


class TokenService(ABC):
    @abstractmethod
    def create_access_token(self, data, expires_delta: timedelta | None = None) -> str:
        pass

    @abstractmethod
    def validate_token(self, token: str) -> str | None:
        pass


class JWTTokenService(TokenService):
    def __init__(self, secret: str, expire_minutes: int, algorithm: str = "HS256") -> None:
        self.secret = secret
        self.expire_minutes = expire_minutes
        self.algorithm = algorithm

    def create_access_token(self, username: str, expires_delta: timedelta | None = None) -> str:
        to_encode = {"sub": username}
        if expires_delta:
            expire = datetime.now(UTC) + expires_delta
        else:
            expire = datetime.now(UTC) + timedelta(minutes=self.expire_minutes)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret, algorithm=self.algorithm)
        return encoded_jwt


    def validate_token(self, token: str) -> str | None:
        try:
            print(token)
            payload = jwt.decode(token, self.secret, algorithms=[self.algorithm])
            print(payload)
            username: str = payload.get("sub")
        except Exception:
            return None
        return username