import pytest
from unittest.mock import patch, MagicMock
from src.services.api_client import ApiClient

# Dummy endpoint and payload
DUMMY_ENDPOINT = "test-endpoint"
DUMMY_HEADERS = {"Authorization": "Bearer test"}
DUMMY_PAYLOAD = {"data": "value"}

@pytest.fixture
def mock_config_url(monkeypatch):
    monkeypatch.setenv("BACKEND_URL", "http://localhost:1234/api")

# --------- GET tests ---------

@patch("src.services.api_client.requests.get")
def test_get_success(mock_get, mock_config_url):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": "ok"}
    mock_get.return_value = mock_response

    result = ApiClient.get(endpoint=DUMMY_ENDPOINT, headers=DUMMY_HEADERS)

    assert result == {"result": "ok"}
    mock_get.assert_called_once()

@patch("src.services.api_client.requests.get")
def test_get_http_error(mock_get, caplog, mock_config_url):
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = Exception("HTTP error")
    mock_get.return_value = mock_response

    result = ApiClient.get(endpoint=DUMMY_ENDPOINT, headers=DUMMY_HEADERS)

    assert result == {}
    assert "Unexpected error" in caplog.text

# --------- POST tests ---------

@patch("src.services.api_client.requests.post")
def test_post_success(mock_post, mock_config_url):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"created": True}
    mock_post.return_value = mock_response

    result = ApiClient.post(endpoint=DUMMY_ENDPOINT, data=DUMMY_PAYLOAD, headers=DUMMY_HEADERS)

    assert result == {"created": True}
    mock_post.assert_called_once()

@patch("src.services.api_client.requests.post")
def test_post_http_error(mock_post, caplog, mock_config_url):
    caplog.set_level("DEBUG") 

    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = Exception("HTTP error")
    mock_post.return_value = mock_response

    result = ApiClient.post(endpoint=DUMMY_ENDPOINT, data=DUMMY_PAYLOAD, headers=DUMMY_HEADERS)

    assert result == {}
    assert "Unexpected error" in caplog.text
    assert "Payload sent" in caplog.text
