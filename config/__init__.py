from pydantic_settings import BaseSettings

class CommonSettings(BaseSettings):
    APP_NAME: str = "FARM Intro"
    DEBUG_MODE: bool = False

    class Config:
        orm_mode = True

class ServerSettings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    class Config:
        orm_mode = True

class DatabaseSettings(BaseSettings):
    DB_URL: str = "mongodb+srv://hamdouch:lVRrNs9787uLgVkW@cls0.gd2gs.mongodb.net/devdb?retryWrites=true&w=majority"
    DB_NAME: str = "devdb"

    class Config:
        orm_mode = True

class Settings(CommonSettings, ServerSettings, DatabaseSettings):
    pass

settings = Settings()
