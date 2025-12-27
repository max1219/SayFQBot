from dataclasses import dataclass
from typing import Optional, Sequence

from environs import Env

@dataclass(slots=True)
class BotConfig:
    token: str
    admin_ids: Sequence[int]
    debug_features: bool

@dataclass(slots=True)
class LoggingConfig:
    level: str

@dataclass(slots=True)
class DatabaseConfig:
    path: str

@dataclass(slots=True)
class Config:
    bot: BotConfig
    database: DatabaseConfig
    logging: LoggingConfig


def load_config(path: Optional[str]) -> Config:
    env = Env()
    env.read_env(path, override=True)
    return Config(
        bot=BotConfig(
            token=env("BOT_TOKEN"),
            admin_ids=list(map(int, env.list('ADMIN_IDS'))),
            debug_features=env.bool('AIOGRAM_DEBUG_FEATURES')),
        database=DatabaseConfig(path=env("DATABASE_PATH")),
        logging=LoggingConfig(level=env("LOG_LEVEL")),
    )