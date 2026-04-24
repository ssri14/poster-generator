from poster_prompt import build_markdown_output, build_messages


def test_build_messages_includes_required_inputs() -> None:
    messages = build_messages(
        poster_topic="Science Expo",
        target_audience="High school students",
        tone_style="Energetic",
        event_details="Friday 4 PM in the main hall",
        call_to_action="Reserve your seat today",
    )

    assert len(messages) == 2
    assert messages[0]["role"] == "system"
    assert "valid JSON" in messages[0]["content"]
    assert "Science Expo" in messages[1]["content"]
    assert "High school students" in messages[1]["content"]
    assert "Reserve your seat today" in messages[1]["content"]


def test_build_messages_uses_default_call_to_action() -> None:
    messages = build_messages(
        poster_topic="Robotics Workshop",
        target_audience="Students",
        tone_style="Friendly",
        event_details="Saturday at 10 AM",
        call_to_action="",
    )

    assert "Join us and learn more." in messages[1]["content"]


def test_build_markdown_output_formats_sections() -> None:
    poster_data = {
        "poster_title": "Innovation Day",
        "tagline": "Ideas that spark action",
        "main_body": "Celebrate student creativity and problem solving.",
        "bullet_highlights": ["Live demos", "Guest speakers", "Hands-on booths"],
        "call_to_action": "Sign up now",
        "suggested_layout": "Title first, highlights in the middle, CTA at the bottom",
        "suggested_image_prompt": "Modern school event poster with lightbulb and students",
    }

    markdown = build_markdown_output(poster_data)

    assert "# Innovation Day" in markdown
    assert "- Live demos" in markdown
    assert "## Suggested Image Prompt" in markdown
