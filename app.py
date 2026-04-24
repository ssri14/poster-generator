"""Streamlit UI for the OpenRouter poster generator demo app."""

from __future__ import annotations

import base64
import json
from typing import Any

import streamlit as st

from openrouter_client import OpenRouterClient, OpenRouterClientError
from pdf_generator import generate_poster_pdf
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


def _decode_data_url(data_url: str) -> tuple[str, bytes]:
    if not data_url.startswith("data:") or "," not in data_url:
        raise ValueError("The image response was not a valid data URL.")

    header, encoded = data_url.split(",", 1)
    mime_type = header[5:].split(";", 1)[0] or "image/png"
    try:
        image_bytes = base64.b64decode(encoded)
    except (ValueError, TypeError) as exc:
        raise ValueError("The generated image could not be decoded.") from exc

    return mime_type, image_bytes


def _render_poster_output(
    data: dict[str, Any],
    poster_image_bytes: bytes | None = None,
    poster_image_mime_type: str | None = None,
) -> None:
    markdown_output = build_markdown_output(data)
    pdf_bytes = generate_poster_pdf(data, poster_image_bytes=poster_image_bytes)

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

    if poster_image_bytes and poster_image_mime_type:
        st.subheader("Generated Poster Image")
        st.image(poster_image_bytes, caption="AI-generated poster artwork preview")
        extension = poster_image_mime_type.split("/")[-1] or "png"
        st.download_button(
            "Download Poster Image",
            data=poster_image_bytes,
            file_name=f"poster-artwork.{extension}",
            mime=poster_image_mime_type,
        )

    st.subheader("Copy-friendly Markdown Output")
    st.code(markdown_output, language="markdown")

    st.download_button(
        "Download Poster PDF",
        data=pdf_bytes,
        file_name="poster-flyer.pdf",
        mime="application/pdf",
    )


def main() -> None:
    st.set_page_config(page_title="Poster Generator", page_icon="🖼️", layout="wide")
    st.title("OpenRouter Poster Generator")
    st.caption("Generate poster copy, optional artwork, and a printable PDF from one workflow.")

    with st.sidebar:
        st.header("How It Works")
        st.write(
            "Enter your OpenRouter API key and poster details, then generate"
            " poster-ready copy using the model you choose."
        )
        st.info("Your OpenRouter API key is used only for this request and is not stored in code.")
        st.caption("Image generation is optional and uses a separate OpenRouter image model.")

    with st.form("poster_form"):
        api_key = st.text_input("OpenRouter API Key", type="password")
        model_name = st.text_input("Model Name", value="openai/gpt-4o-mini")
        poster_topic = st.text_input("Poster Topic")
        target_audience = st.text_input("Target Audience", value="Students")
        tone_style = st.text_input("Tone/Style", value="Friendly and inspiring")
        event_details = st.text_area("Event Name / Details", height=120)
        call_to_action = st.text_input("Optional Call-to-Action")
        generate_image = st.checkbox("Generate poster image", value=True)
        image_model_name = st.text_input(
            "Image Model Name",
            value="google/gemini-2.5-flash-image",
            disabled=not generate_image,
        )
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
    poster_image_bytes: bytes | None = None
    poster_image_mime_type: str | None = None

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

    if generate_image and image_model_name.strip():
        with st.spinner("Generating poster image..."):
            try:
                image_data_url = client.generate_poster_image(
                    model_name=image_model_name.strip(),
                    prompt=str(poster_data["suggested_image_prompt"]),
                )
                poster_image_mime_type, poster_image_bytes = _decode_data_url(image_data_url)
            except OpenRouterClientError as exc:
                st.warning(f"Poster text was generated, but image generation failed: {exc}")
            except ValueError as exc:
                st.warning(f"Poster text was generated, but the returned image could not be used: {exc}")

    _render_poster_output(
        poster_data,
        poster_image_bytes=poster_image_bytes,
        poster_image_mime_type=poster_image_mime_type,
    )


if __name__ == "__main__":
    main()
