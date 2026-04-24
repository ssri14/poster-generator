"""Streamlit UI for the OpenRouter poster generator demo app."""

from __future__ import annotations

import json
from typing import Any

import streamlit as st

from openrouter_client import OpenRouterClient, OpenRouterClientError
from poster_prompt import build_markdown_output, build_messages


def _normalize_poster_data(payload: Any) -> dict[str, Any]:
    """Accept either a dict or a JSON string and return validated poster data."""
    if isinstance(payload, dict):
        data = payload
    elif isinstance(payload, str):
        try:
            data = json.loads(payload)
        except json.JSONDecodeError as exc:
            raise ValueError("The API returned invalid JSON content.") from exc
    else:
        raise ValueError("The API returned an unexpected response format.")

    required_fields = [
        "poster_title",
        "tagline",
        "main_body",
        "bullet_highlights",
        "call_to_action",
        "suggested_layout",
        "suggested_image_prompt",
    ]
    missing = [field for field in required_fields if field not in data]
    if missing:
        missing_fields = ", ".join(missing)
        raise ValueError(f"The generated content is missing required fields: {missing_fields}.")

    bullets = data.get("bullet_highlights")
    if not isinstance(bullets, list):
        raise ValueError("The generated bullet highlights must be a list.")

    return data


def _render_poster_output(data: dict[str, Any]) -> None:
    st.success("Poster content generated successfully.")
    st.subheader("Poster Title")
    st.write(data["poster_title"])

    st.subheader("Short Tagline")
    st.write(data["tagline"])

    st.subheader("Main Body Text")
    st.write(data["main_body"])

    st.subheader("Bullet Highlights")
    for bullet in data["bullet_highlights"]:
        st.markdown(f"- {bullet}")

    st.subheader("Call to Action")
    st.write(data["call_to_action"])

    st.subheader("Suggested Layout")
    st.write(data["suggested_layout"])

    st.subheader("Suggested Image Prompt")
    st.code(data["suggested_image_prompt"], language="text")

    st.subheader("Copy-friendly Markdown Output")
    st.code(build_markdown_output(data), language="markdown")


def main() -> None:
    st.set_page_config(page_title="Poster Generator", page_icon="🖼️", layout="wide")
    st.title("OpenRouter Poster Generator")
    st.caption("A simple classroom demo for Streamlit, testing, and CI/CD.")

    with st.sidebar:
        st.header("How It Works")
        st.write(
            "Enter your OpenRouter API key and poster details, then generate"
            " poster-ready copy using the model you choose."
        )
        st.info("Your OpenRouter API key is used only for this request and is not stored in code.")

    with st.form("poster_form"):
        api_key = st.text_input("OpenRouter API Key", type="password")
        model_name = st.text_input("Model Name", value="openai/gpt-4o-mini")
        poster_topic = st.text_input("Poster Topic")
        target_audience = st.text_input("Target Audience", value="Students")
        tone_style = st.text_input("Tone/Style", value="Friendly and inspiring")
        event_details = st.text_area("Event Name / Details", height=120)
        call_to_action = st.text_input("Optional Call-to-Action")
        submit = st.form_submit_button("Generate Poster Content", type="primary")

    if not submit:
        return

    if not api_key.strip():
        st.error("Please enter your OpenRouter API key before generating poster content.")
        return

    if not poster_topic.strip():
        st.error("Please enter a poster topic so the app knows what to generate.")
        return

    messages = build_messages(
        poster_topic=poster_topic,
        target_audience=target_audience,
        tone_style=tone_style,
        event_details=event_details,
        call_to_action=call_to_action,
    )

    client = OpenRouterClient(api_key=api_key.strip())

    with st.spinner("Generating poster-ready content..."):
        try:
            raw_content = client.generate_poster_content(model_name=model_name.strip(), messages=messages)
            poster_data = _normalize_poster_data(raw_content)
        except OpenRouterClientError as exc:
            st.error(f"OpenRouter request failed: {exc}")
            return
        except ValueError as exc:
            st.error(str(exc))
            return

    _render_poster_output(poster_data)


if __name__ == "__main__":
    main()
