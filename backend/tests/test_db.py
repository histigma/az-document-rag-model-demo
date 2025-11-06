# tests/test_weaviate_client.py
import pytest
from unittest.mock import MagicMock
from modules.db.driver.weaviate_client import LocalWeaviateDB


@pytest.fixture
def mock_client():
    client = MagicMock()
    client.is_ready.return_value = True
    client.is_connected.return_value = True
    client.collections.create_from_dict.return_value = {"result": "ok"}
    return client


def test_localweaviate_initialization(monkeypatch, mock_client):
    monkeypatch.setattr(
        "modules.db.driver.weaviate_client.wv.connect_to_local",
        lambda **kwargs: mock_client
    )

    db = LocalWeaviateDB()
    assert db.connected is True
    assert db.conn == mock_client


def test_localweaviate_enter_exit(mock_client):
    db = LocalWeaviateDB(connector=lambda **_: mock_client)
    with db as conn:
        assert conn.is_ready()
    mock_client.close.assert_called_once()


def test_create_schema(mock_client):
    db = LocalWeaviateDB(connector=lambda **_: mock_client)
    result = db._create_schema({"collection": "Test"})
    assert result == {"result": "ok"}
    mock_client.collections.create_from_dict.assert_called_once()


def test_testmode_no_connection():
    db = LocalWeaviateDB(test_mode=True)
    with pytest.raises(ConnectionError):
        _ = db.conn
