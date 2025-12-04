from pydantic import BaseModel


class CurrentUserResponse(BaseModel):
    id: int
    email: str
    role: str


class UserResponse(BaseModel):
    email: str
    role: str


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
    expires_in: int
