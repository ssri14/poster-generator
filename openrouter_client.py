"""Small OpenRouter API client used by the Streamlit app."""

from __future__ import annotations

from typing import Any

import requests


OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


class OpenRouterClientError(Exception):
    """Raised when the OpenRouter API request fails."""


class OpenRouterClient:
    def __init__(
        self,
        api_key: str,
        base_url: str = OPENROUTER_URL,
        timeout: int = 60,
        app_name: str = "Poster Generator",
    ) -> None:
        self.api_key = api_key
        self.base_url = base_url
        self.timeout = timeout
        self.app_name = app_name

    def generate_poster_content(self, model_name: str, messages: list[dict[str, str]]) -> str:
        payload = {
            "model": model_name,
            "messages": messages,
            "response_format": {"type": "json_object"},
        }
        headers = self._build_headers()

        try:
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=self.timeout,
            )
        except requests.RequestException as exc:
            raise OpenRouterClientError("Network error while contacting OpenRouter.") from exc

        response_data = _parse_json_response(response)

        try:
            return response_data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise OpenRouterClientError("OpenRouter returned an unexpected JSON structure.") from exc

    def generate_poster_image(
        self,
        model_name: str,
        prompt: str,
        aspect_ratio: str = "3:4",
        image_size: str = "1K",
    ) -> str:
        payload = {
            "model": model_name,
            "messages": [{"role": "user", "content": prompt}],
            "modalities": ["image", "text"],
            "image_config": {
                "aspect_ratio": aspect_ratio,
                "image_size": image_size,
            },
        }
        headers = self._build_headers()

        try:
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=self.timeout,
            )
        except requests.RequestException as exc:
            raise OpenRouterClientError("Network error while contacting OpenRouter.") from exc

        response_data = _parse_json_response(response)

        try:
            message = response_data["choices"][0]["message"]
            image_data = message["images"][0]
        except (KeyError, IndexError, TypeError) as exc:
            raise OpenRouterClientError("OpenRouter returned an unexpected image response.") from exc

        image_url = image_data.get("image_url") or image_data.get("imageUrl")
        if not isinstance(image_url, dict) or not image_url.get("url"):
            raise OpenRouterClientError("OpenRouter did not return an image data URL.")

        return str(image_url["url"])

    def _build_headers(self) -> dict[str, str]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/ssri14/poster-generator",
            "X-Title": self.app_name,
        }
        return headers

def _parse_json_response(response: requests.Response) -> dict[str, Any]:
    if response.status_code >= 400:
        message = _extract_error_message(response)
        raise OpenRouterClientError(f"API failure ({response.status_code}): {message}")

    try:
        data = response.json()
    except ValueError as exc:
        raise OpenRouterClientError("OpenRouter returned a non-JSON response.") from exc

    if not isinstance(data, dict):
        raise OpenRouterClientError("OpenRouter returned an unexpected JSON structure.")

    return data


def _extract_error_message(response: requests.Response) -> str:
    try:
        data: dict[str, Any] = response.json()
    except ValueError:
        return response.text.strip() or "Unknown error"

    error = data.get("error")
    if isinstance(error, dict):
        message = error.get("message")
        if message:
            return str(message)

    detail = data.get("message")
    if detail:
        return str(detail)

    return "Unknown error"
