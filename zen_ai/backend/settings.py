from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Manages application settings and secrets using Pydantic.
    It automatically reads variables from a .env file.
    """
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str

    # This tells Pydantic where to find the .env file.
    # The path is relative to where the application is run.
    model_config = SettingsConfigDict(env_file="zen_ai/backend/.env", env_file_encoding='utf-8')

# Create a single, reusable instance of the settings object.
# Other parts of the application will import this object.
settings = Settings()
