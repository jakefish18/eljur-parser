"""
Project settings.

Some settings are imported from .env file.
If file doesn't exist the error will be thrown.
"""
from environs import Env

env = Env()
env.read_env()


class Settings:
    # Eljur user auth settings.
    user_name: str = env("USER_NAME")
    user_password: str = env("USER_PASSWORD")

    # Parsing settings.
    user_agent: str = "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0"
    ELJUR_URL: str = "https://rbli.eljur.ru"
    lyceum_classes: list = ["11А", "10А", "10Б", "11Б"]


settings = Settings()
