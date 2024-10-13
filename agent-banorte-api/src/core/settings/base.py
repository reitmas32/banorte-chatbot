# Standard Library
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Third Party Stuff
from pydantic_settings import BaseSettings as PydanticBaseSettings
from pydantic_settings import SettingsConfigDict

from core.utils.environment import EnvironmentsTypes

LIST_PATH_TO_ADD = []
if LIST_PATH_TO_ADD:
    sys.path.extend(LIST_PATH_TO_ADD)


BASE_DIR = Path(__file__).resolve().parent.parent
ENVS_DIR = BASE_DIR.parent / "envs"
ENV_BASE_FILE_PATH = ENVS_DIR / ".env.base"
load_dotenv(ENV_BASE_FILE_PATH)
ENVIRONMENT = os.environ.get("ENVIRONMENT")
EnvironmentsTypes.check_env_value(ENVIRONMENT)
ENV_FILE_PATH = ENVS_DIR / EnvironmentsTypes.get_env_file_name(ENVIRONMENT)


class Settings(PydanticBaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_FILE_PATH, extra="ignore", case_sensitive=True)
    ENVIRONMENT: str = ENVIRONMENT
    # Database settings
    # ----------------------------------------------------------------
    FIREBASE_URL: str
    TELEGRAM_KEY: str
    PORT: int = 5050
    # Project Constants
    # ----------------------------------------------------------------
    PROJECT_NAME: str = "AsistentApi"
    PROJECT_ID: str = "A0001"
    TIME_ZONE: str = "utc"
    TIME_ZONE_UTC: str = "utc"
    DATE_FORMAT: str = "%Y-%m-%d"
    DATE_TIME_FORMAT: str = "%Y-%m-%d %H:%M:%S"

