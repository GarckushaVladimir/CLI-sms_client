import argparse
import asyncio
from sms_client.logging_config import logger
from sms_client.client import SMSClient
from sms_client.config import Config


async def async_main():
    """Основная асинхронная функция приложения."""
    parser = argparse.ArgumentParser(description="Отправка SMS через API")
    parser.add_argument("--sender", required=True, help="Номер отправителя", nargs="?")
    parser.add_argument("--recipient", required=True, help="Номер получателя", nargs="?")
    parser.add_argument("--message", required=True, help="Текст сообщения", nargs="?")
    args = parser.parse_args()

    logger.info("Запуск с параметрами: %s", vars(args))

    try:
        config = Config.from_file()
        client = SMSClient(config)
        response = await client.send_sms(args.sender, args.recipient, args.message)

        print(f"Код ответа: {response.status_code}")
        print(f"Тело ответа: {response.body.decode()}")
        logger.info("Успешный ответ: %d", response.status_code)

    except Exception as e:
        logger.critical("Критическая ошибка: %s", str(e))
        raise


def main():
    """Точка входа в приложение."""
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
