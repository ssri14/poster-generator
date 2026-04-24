"""Helpers for turning poster markdown into a simple PDF."""

from __future__ import annotations

from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


def generate_pdf_from_markdown(markdown_text: str, title: str = "Poster Content") -> bytes:
    """Render a small subset of markdown into a classroom-friendly PDF."""
    buffer = BytesIO()
    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        title=title,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
    )

    styles = getSampleStyleSheet()
    heading_style = styles["Heading2"]
    title_style = styles["Title"]
    body_style = styles["BodyText"]
    body_style.spaceAfter = 8

    bullet_style = ParagraphStyle(
        "PosterBullet",
        parent=body_style,
        leftIndent=18,
        bulletIndent=6,
        spaceAfter=4,
    )

    story = []
    for line in markdown_text.splitlines():
        text = line.strip()
        if not text:
            story.append(Spacer(1, 0.12 * inch))
            continue

        if text.startswith("# "):
            story.append(Paragraph(_escape_pdf_text(text[2:]), title_style))
            story.append(Spacer(1, 0.1 * inch))
            continue

        if text.startswith("## "):
            story.append(Paragraph(_escape_pdf_text(text[3:]), heading_style))
            continue

        if text.startswith("- "):
            story.append(
                Paragraph(
                    _escape_pdf_text(text[2:]),
                    bullet_style,
                    bulletText="•",
                )
            )
            continue

        story.append(Paragraph(_escape_pdf_text(_convert_inline_bold(text)), body_style))

    if not story:
        story.append(Paragraph("No poster content available.", body_style))

    document.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes


def _convert_inline_bold(text: str) -> str:
    """Convert simple markdown bold into ReportLab-compatible tags."""
    parts = text.split("**")
    if len(parts) < 3:
        return text

    converted: list[str] = []
    for index, part in enumerate(parts):
        if index % 2 == 1:
            converted.append(f"<b>{part}</b>")
        else:
            converted.append(part)
    return "".join(converted)


def _escape_pdf_text(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
