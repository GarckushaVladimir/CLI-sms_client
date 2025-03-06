# SMS Client CLI 

**CLI-клиент для отправки SMS через API** 

Инструмент для интеграции с SMS-сервисом. Отправка сообщения из командной строки с поддержкой асинхронных запросов.

## Особенности
- Асинхронная отправка SMS через HTTP API
- Конфигурация через TOML-файл
- Логирование операций в файл и консоль
- Автоматическая авторизация (Basic Auth)
- Тестирование с помощью pytest

## Установка
1. Клонируйте репозиторий:
    ```bash
    git clone https://github.com/GarckushaVladimir/CLI-sms_client.git 
    cd CLI-sms_client
    ```
   

2. Установите зависимости:
    ```bash
    python -m pip install .
    ```

3. Настройте конфигурацию в `config.toml`:
   ```toml
   [sms_service]
   service_url = "http://localhost:4010" # Хост сервиса отправки SMS
   username = "admin" # Имя пользователя
   password = "password"  # Пароль
   ```
## Запуск мок-сервера

Для тестирования программы можно использовать мок-сервер Prism.

1. Скачайте Prism для своей платформы:

   [Windows / Linux / macOS](https://github.com/stoplightio/prism/releases)

2. Поместите Prism в корнь проекта.

3. Запустите мок-сервер:

   - Linux: ```./prism-cli-linux mock sms-platform.yaml```
   - macOS: ```./prism-cli-macos mock sms-platform.yaml```
   - Windows: ```./prism-cli-win.exe mock sms-platform.yaml```

## Использование
   ```bash
   sms-client --sender "+79001234567" --recipient "+79007654321" --message "Привет, мир!"
   ```

Пример вывода:
   ```
   Код ответа: 200
   Тело ответа: {"status": "success", "message_id": "123456"}
   ```
## Тестирование
Для запуска тестов (требуются dev-зависимости):
   ```bash
   python -m pip install .[dev]
   pytest -v tests/
   ```
