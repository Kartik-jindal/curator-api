from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Manages application settings and configuration by reading from environment
    variable file. This provides a centralized and secure way to
    handle configuration.
    """
    # SECRET_KEY: A long, random, secret string used for signing JWTs.
    # It is critical this is kept secret and not hardcoded. 
    # The application will fail to start if this is not provided.
    SECRET_KEY: str

    # ALGORITHM: The cryptographic algorithm used for encoding JWTs.
    # HS256 (HMAC using SHA-256) is a common and secure choice.
    ALGORITHM: str = "HS256"

    # Defines the lifetime of the access token in  minutes.
    # After this time, the user will need to log in again.
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # model_config is a special Pydantic configuration attribute.
    # It instructs the Settings class to load values from a file named ".env" using UTF-8 encoding.
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

# Create a single, importable instance of the Settings class.
# Other parts of your application will import this `settings` object to access configuration values like `settings.SECRET_KEY`.
settings = Settings()