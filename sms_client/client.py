import json
import asyncio
import base64
from sms_client.logging_config import logger
from sms_client.config import Config
from sms_client.http import HTTPRequest, HTTPResponse


class SMSClient:
    """Клиент для взаимодействия с SMS-сервисом."""

    def __init__(self, config: Config):
        self.config = config
        logger.debug("Инициализация клиента для %s", self.config.service_url)

    async def send_sms(self, sender: str, recipient: str, message: str) -> HTTPResponse:
        """Асинхронно отправляет SMS через API.

        Args:
            sender: Номер отправителя
            recipient: Номер получателя
            message: Текст сообщения

        Returns:
            HTTPResponse: Ответ сервера
        """
        body_data = {
            "sender": sender,
            "recipient": recipient,
            "message": message
        }
        body = json.dumps(body_data).encode()
        auth = base64.b64encode(f"{self.config.username}:{self.config.password}".encode()).decode()

        url = self.config.service_url.split("://")[-1]
        host, port = (url.split(":", 1) if ":" in url else (url, 4010))

        request = HTTPRequest(
            method="POST",
            path="/send_sms",
            headers={
                "Host": host,
                "Content-Type": "application/json",
                "Authorization": f"Basic {auth}",
                "Content-Length": str(len(body)),
            },
            body=body
        )

        logger.debug("Установка соединения с %s:%s", host, port)
        reader, writer = await asyncio.open_connection(host, int(port))

        try:
            writer.write(request.to_bytes())
            await writer.drain()
            response_data = await reader.read(4096)
            logger.debug("Получено %d байт ответа", len(response_data))

        except (ConnectionError, TimeoutError) as e:
            logger.error("Ошибка соединения: %s", str(e))
            raise

        except Exception as e:
            logger.critical("Неизвестная ошибка: %s", str(e))
            raise

        finally:
            writer.close()
            await writer.wait_closed()

        response = HTTPResponse.from_bytes(response_data)
        return response
