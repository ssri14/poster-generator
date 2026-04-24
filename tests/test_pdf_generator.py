from pdf_generator import generate_pdf_from_markdown


def test_generate_pdf_from_markdown_returns_pdf_bytes() -> None:
    markdown = """
# Campus Innovation Fair

**Tagline:** Build ideas together

## Highlights
- Live demos
- Student showcases
"""

    pdf_bytes = generate_pdf_from_markdown(markdown, title="Campus Innovation Fair")

    assert isinstance(pdf_bytes, bytes)
    assert pdf_bytes.startswith(b"%PDF")
    assert len(pdf_bytes) > 500


def test_generate_pdf_from_markdown_handles_empty_text() -> None:
    pdf_bytes = generate_pdf_from_markdown("", title="Empty Poster")

    assert pdf_bytes.startswith(b"%PDF")
