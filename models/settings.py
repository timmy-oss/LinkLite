from pydantic import BaseSettings
from pydantic import AnyUrl
from typing import Any







class Settings(BaseSettings):
    " Model for the application settings  "
    debug : bool = True
    app_name : str = "HydraTest"
    allowed_origins : list[str] = ["http://localhost:3000","https://timmy-oss-sturdy-bassoon-x47x4vqv4q536vjw-3000.preview.app.github.dev"]
    db_url : AnyUrl = "redis://127.0.0.1:10005"
    db_username : str = "default"
    db_password  : str = "root"
    


    class Config:
        env_file = ".secrets"