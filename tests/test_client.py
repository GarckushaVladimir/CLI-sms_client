import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from sms_client.config import Config
from sms_client.client import SMSClient
from sms_client.http import HTTPResponse


@pytest.fixture
def mock_config():
    return Config(
        service_url="http://test:4010",
        username="test",
        password="test"
    )


@pytest.mark.asyncio
@patch("asyncio.open_connection")
async def test_send_sms_success(mock_conn, mock_config):
    """Тестирует успешную отправку SMS."""
    mock_reader = AsyncMock()
    mock_reader.read.return_value = (
        b"HTTP/1.1 200 OK\r\n"
        b"Content-Type: application/json\r\n"
        b"Content-Length: 21\r\n"
        b"\r\n"
        b'{"status": "success"}'
    )

    mock_writer = MagicMock()
    mock_writer.drain = AsyncMock()
    mock_writer.close = MagicMock()
    mock_writer.wait_closed = AsyncMock()

    mock_conn.return_value = (mock_reader, mock_writer)

    client = SMSClient(mock_config)
    response = await client.send_sms("123456789", "987654321", "Hello, World!")

    assert isinstance(response, HTTPResponse)
    assert response.status_code == 200
    assert response.body == b'{"status": "success"}'
    mock_writer.write.assert_called_once()
    mock_writer.drain.assert_awaited_once()
    mock_writer.close.assert_called_once()
    mock_writer.wait_closed.assert_awaited_once()


@pytest.mark.asyncio
@patch("asyncio.open_connection")
async def test_connection_error(mock_conn, mock_config):
    """Тестирует обработку ошибки соединения."""
    mock_conn.side_effect = ConnectionRefusedError("Сервер недоступен")
    client = SMSClient(mock_config)

    with pytest.raises(ConnectionRefusedError):
        await client.send_sms("+123", "+456", "test")
