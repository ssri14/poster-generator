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
        app_name: str = "Poster Generator Classroom Demo",
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
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/ssri14/poster-generator",
            "X-Title": self.app_name,
        }

        try:
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=self.timeout,
            )
        except requests.RequestException as exc:
            raise OpenRouterClientError("Network error while contacting OpenRouter.") from exc

        if response.status_code >= 400:
            message = _extract_error_message(response)
            raise OpenRouterClientError(f"API failure ({response.status_code}): {message}")

        try:
            response_data = response.json()
        except ValueError as exc:
            raise OpenRouterClientError("OpenRouter returned a non-JSON response.") from exc

        try:
            return response_data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise OpenRouterClientError("OpenRouter returned an unexpected JSON structure.") from exc


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
