from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseModel):
    authjwt_secret_key: str = os.getenv("SECRET_KEY", "your-super-secret-jwt-key-change-me")
    authjwt_access_token_expires: int = 30
    authjwt_refresh_token_expires: int = 30
    authjwt_token_location: list = ["headers"]
    authjwt_header_name: str = "Authorization"
    authjwt_header_type: str = "Bearer"


@AuthJWT.load_config
def get_config():
    return Settings().dict().items()
