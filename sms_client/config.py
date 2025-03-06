from dataclasses import dataclass

try:
    import tomllib  # Python 3.11+
except ImportError:
    import tomli as tomllib  # Python <3.11


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
        with open(path, 'rb') as f:
            data = tomllib.load(f)
        return cls(**data["sms_service"])
