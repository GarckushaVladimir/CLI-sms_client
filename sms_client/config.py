from dataclasses import dataclass
from sms_client.logging_config import logger

try:
    import tomllib

except ImportError:
    import tomli as tomllib


@dataclass
class Config:
    """Конфигурация клиента SMS-сервиса."""
    service_url: str
    username: str
    password: str

    @classmethod
    def from_file(cls, path: str = "config.toml") -> "Config":
        """Загружает конфигурацию из TOML-файла.

        Args:
            path (str): Путь к файлу конфигурации. По умолчанию 'config.toml'.

        Returns:
            Config: Загруженная конфигурация.
        """
        logger.info("Загрузка конфигурации из %s", path)
        with open(path, 'rb') as f:
            data = tomllib.load(f)
        return cls(**data["sms_service"])
