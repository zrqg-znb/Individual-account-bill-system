from datetime import datetime

from pydantic import BaseModel, Field


class CredentialsSchema(BaseModel):
    phone: str = Field(..., description="手机号", example="13100001111")
    password: str = Field(..., description="密码", example="123456")


class JWTOut(BaseModel):
    access_token: str
    username: str


class JWTPayload(BaseModel):
    user_id: int
    username: str
    is_superuser: bool
    exp: datetime
