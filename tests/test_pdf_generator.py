import base64

from pdf_generator import generate_poster_pdf


SAMPLE_PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+Xw0YAAAAASUVORK5CYII="
)


def test_generate_poster_pdf_returns_pdf_bytes() -> None:
    poster_data = {
        "poster_title": "Campus Innovation Fair",
        "tagline": "Build ideas together",
        "main_body": "Meet student teams, discover creative projects, and explore hands-on demos.",
        "bullet_highlights": ["Live demos", "Student showcases", "Interactive booths"],
        "call_to_action": "Register today and bring a friend.",
    }

    pdf_bytes = generate_poster_pdf(poster_data)

    assert isinstance(pdf_bytes, bytes)
    assert pdf_bytes.startswith(b"%PDF")
    assert len(pdf_bytes) > 500
    assert b"Campus Innovation Fair" in pdf_bytes


def test_generate_poster_pdf_handles_missing_fields() -> None:
    pdf_bytes = generate_poster_pdf({})

    assert pdf_bytes.startswith(b"%PDF")
    assert b"Community Event" in pdf_bytes


def test_generate_poster_pdf_accepts_generated_image() -> None:
    poster_data = {
        "poster_title": "Design Showcase",
        "tagline": "A gallery of ideas",
        "main_body": "Discover visual concepts, student projects, and creative experiments.",
        "bullet_highlights": ["Poster displays", "Talks", "Team projects"],
        "call_to_action": "Join the showcase this Friday.",
    }

    pdf_bytes = generate_poster_pdf(poster_data, poster_image_bytes=SAMPLE_PNG)

    assert pdf_bytes.startswith(b"%PDF")
    assert len(pdf_bytes) > 800
