import argparse
import asyncio
from .client import SMSClient
from .config import Config


async def async_main():
    """Основная асинхронная функция приложения."""
    parser = argparse.ArgumentParser(description="Отправка SMS через API")
    parser.add_argument("--sender", required=True, help="Номер отправителя", nargs="?")
    parser.add_argument("--recipient", required=True, help="Номер получателя", nargs="?")
    parser.add_argument("--message", required=True, help="Текст сообщения", nargs="?")
    args = parser.parse_args()

    try:
        config = Config.from_file()
        client = SMSClient(config)
        response = await client.send_sms(args.sender, args.recipient, args.message)

        print(f"Код ответа: {response.status_code}")
        print(f"Тело ответа: {response.body.decode()}")
    except Exception as e:
        raise RuntimeError(f"Error: {e}")


def main():
    """Точка входа в приложение."""
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
