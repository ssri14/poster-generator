from unittest.mock import Mock, patch

import requests
import pytest

from openrouter_client import OpenRouterClient, OpenRouterClientError


def _mock_response(
    *,
    status_code: int = 200,
    json_data=None,
    text: str = "",
):
    response = Mock()
    response.status_code = status_code
    response.text = text
    response.json = Mock(return_value=json_data)
    return response


def test_generate_poster_content_returns_message_content() -> None:
    client = OpenRouterClient(api_key="test-key")
    response = _mock_response(
        json_data={"choices": [{"message": {"content": '{"poster_title":"Demo"}'}}]}
    )

    with patch("openrouter_client.requests.post", return_value=response) as mock_post:
        result = client.generate_poster_content(
            model_name="openai/gpt-4o-mini",
            messages=[{"role": "user", "content": "Create a poster"}],
        )

    assert result == '{"poster_title":"Demo"}'
    mock_post.assert_called_once()


def test_generate_poster_content_raises_for_network_error() -> None:
    client = OpenRouterClient(api_key="test-key")

    with patch(
        "openrouter_client.requests.post",
        side_effect=requests.RequestException("connection failed"),
    ):
        with pytest.raises(OpenRouterClientError, match="Network error"):
            client.generate_poster_content(
                model_name="openai/gpt-4o-mini",
                messages=[{"role": "user", "content": "Create a poster"}],
            )


def test_generate_poster_content_raises_for_api_error() -> None:
    client = OpenRouterClient(api_key="test-key")
    response = _mock_response(
        status_code=401,
        json_data={"error": {"message": "Invalid API key"}},
    )

    with patch("openrouter_client.requests.post", return_value=response):
        with pytest.raises(OpenRouterClientError, match="Invalid API key"):
            client.generate_poster_content(
                model_name="openai/gpt-4o-mini",
                messages=[{"role": "user", "content": "Create a poster"}],
            )


def test_generate_poster_content_raises_for_invalid_json_response() -> None:
    client = OpenRouterClient(api_key="test-key")
    response = Mock()
    response.status_code = 200
    response.json.side_effect = ValueError("bad json")

    with patch("openrouter_client.requests.post", return_value=response):
        with pytest.raises(OpenRouterClientError, match="non-JSON response"):
            client.generate_poster_content(
                model_name="openai/gpt-4o-mini",
                messages=[{"role": "user", "content": "Create a poster"}],
            )


def test_generate_poster_content_raises_for_unexpected_json_structure() -> None:
    client = OpenRouterClient(api_key="test-key")
    response = _mock_response(json_data={"choices": []})

    with patch("openrouter_client.requests.post", return_value=response):
        with pytest.raises(OpenRouterClientError, match="unexpected JSON structure"):
            client.generate_poster_content(
                model_name="openai/gpt-4o-mini",
                messages=[{"role": "user", "content": "Create a poster"}],
            )


def test_generate_poster_image_returns_data_url() -> None:
    client = OpenRouterClient(api_key="test-key")
    response = _mock_response(
        json_data={
            "choices": [
                {
                    "message": {
                        "images": [
                            {
                                "image_url": {
                                    "url": "data:image/png;base64,abc123"
                                }
                            }
                        ]
                    }
                }
            ]
        }
    )

    with patch("openrouter_client.requests.post", return_value=response):
        result = client.generate_poster_image(
            model_name="google/gemini-2.5-flash-image",
            prompt="Create a bright event poster illustration",
        )

    assert result == "data:image/png;base64,abc123"


def test_generate_poster_image_raises_for_missing_image_data() -> None:
    client = OpenRouterClient(api_key="test-key")
    response = _mock_response(json_data={"choices": [{"message": {"images": []}}]})

    with patch("openrouter_client.requests.post", return_value=response):
        with pytest.raises(OpenRouterClientError, match="unexpected image response"):
            client.generate_poster_image(
                model_name="google/gemini-2.5-flash-image",
                prompt="Create a bright event poster illustration",
            )
