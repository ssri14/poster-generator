"""Prompt helpers for building poster-generation requests."""

from __future__ import annotations

import json
from textwrap import dedent


def build_messages(
    poster_topic: str,
    target_audience: str,
    tone_style: str,
    event_details: str,
    call_to_action: str,
) -> list[dict[str, str]]:
    system_prompt = dedent(
        """
        You are a helpful assistant that creates poster-ready marketing content.
        Always return valid JSON with this exact structure:
        {
          "poster_title": "string",
          "tagline": "string",
          "main_body": "string",
          "bullet_highlights": ["string", "string", "string"],
          "call_to_action": "string",
          "suggested_layout": "string",
          "suggested_image_prompt": "string"
        }
        Keep the writing concise, vivid, and suitable for a poster.
        """
    ).strip()

    fallback_cta = call_to_action.strip() or "Join us and learn more."
    user_prompt = dedent(
        f"""
        Create poster-ready content using these inputs:
        - Poster topic: {poster_topic.strip()}
        - Target audience: {target_audience.strip() or "General audience"}
        - Tone/style: {tone_style.strip() or "Clear and engaging"}
        - Event details: {event_details.strip() or "No extra event details provided"}
        - Call-to-action: {fallback_cta}

        Requirements:
        - Make the content easy to place on a poster.
        - Write a strong title and short tagline.
        - Provide 3 to 5 bullet highlights.
        - Keep the body text concise.
        - Suggest a practical poster layout.
        - Suggest an image-generation prompt that matches the poster.
        - Return JSON only.
        """
    ).strip()

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]


def build_markdown_output(poster_data: dict[str, object]) -> str:
    bullets = poster_data.get("bullet_highlights", [])
    bullet_lines = "\n".join(f"- {item}" for item in bullets if isinstance(item, str))

    markdown = dedent(
        f"""
        # {poster_data.get("poster_title", "")}

        **Tagline:** {poster_data.get("tagline", "")}

        ## Main Body
        {poster_data.get("main_body", "")}

        ## Highlights
        {bullet_lines}

        ## Call to Action
        {poster_data.get("call_to_action", "")}

        ## Suggested Layout
        {poster_data.get("suggested_layout", "")}

        ## Suggested Image Prompt
        {poster_data.get("suggested_image_prompt", "")}
        """
    ).strip()

    return markdown


def pretty_json_example() -> str:
    """Small helper used in docs or teaching demos."""
    sample = {
        "poster_title": "Community Tech Fair",
        "tagline": "Build, learn, and create together.",
        "main_body": "Join students, teachers, and makers for hands-on demos and project showcases.",
        "bullet_highlights": [
            "Live coding demos",
            "Student innovation booths",
            "Free entry for all visitors",
        ],
        "call_to_action": "Register today and bring a friend.",
        "suggested_layout": "Large title at the top, event details in the center, highlights on the side.",
        "suggested_image_prompt": "Bright classroom tech fair poster with students presenting creative projects.",
    }
    return json.dumps(sample, indent=2)
