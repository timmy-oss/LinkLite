from pydantic import BaseSettings, AnyUrl


class Settings(BaseSettings):
    " Model for the application settings  "
    debug : bool = True
    app_name : str = "Blinkr"
    allowed_origins : list[str] = ["http://localhost:3000", "https://pp2.timmypelumy.dev", "https://blinkr.onrender.com" ]
    db_url : AnyUrl = "redis://127.0.0.1:10005"
    db_username : str = "default"
    db_password  : str = "root"
    base_domain : str = "localhost:7000"
    


    class Config:
        env_file = ".env"
