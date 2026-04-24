"""Helpers for turning poster content into a more polished PDF poster."""

from __future__ import annotations

from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader, simpleSplit
from reportlab.pdfgen import canvas


PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN = 42


def generate_poster_pdf(
    poster_data: dict[str, object],
    poster_image_bytes: bytes | None = None,
) -> bytes:
    """Render structured poster content as a one-page, poster-style PDF."""
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4, pageCompression=0)
    pdf.setTitle(str(poster_data.get("poster_title", "Poster Content")))

    _draw_background(pdf)
    _draw_header(pdf, poster_data)
    _draw_feature_panel(pdf, poster_data, poster_image_bytes)
    _draw_highlights_panel(pdf, poster_data)
    _draw_call_to_action(pdf, poster_data)

    pdf.showPage()
    pdf.save()
    return buffer.getvalue()


def _draw_background(pdf: canvas.Canvas) -> None:
    pdf.setFillColor(colors.HexColor("#f7f1e3"))
    pdf.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)

    pdf.setFillColor(colors.HexColor("#ffd166"))
    pdf.circle(PAGE_WIDTH - 60, PAGE_HEIGHT - 70, 60, fill=1, stroke=0)

    pdf.setFillColor(colors.HexColor("#ef476f"))
    pdf.circle(65, PAGE_HEIGHT - 120, 26, fill=1, stroke=0)

    pdf.setFillColor(colors.HexColor("#118ab2"))
    pdf.circle(PAGE_WIDTH - 85, 120, 40, fill=1, stroke=0)


def _draw_header(pdf: canvas.Canvas, poster_data: dict[str, object]) -> None:
    title = _clean_text(poster_data.get("poster_title"), "Community Event")
    tagline = _clean_text(poster_data.get("tagline"), "Bring people together with a clear message.")

    top = PAGE_HEIGHT - 95
    pdf.setFillColor(colors.HexColor("#073b4c"))
    pdf.roundRect(MARGIN, top - 110, PAGE_WIDTH - (2 * MARGIN), 110, 20, fill=1, stroke=0)

    pdf.setFillColor(colors.white)
    title_lines = simpleSplit(title, "Helvetica-Bold", 26, PAGE_WIDTH - (2 * MARGIN) - 36)
    y = top - 25
    for line in title_lines[:3]:
        pdf.setFont("Helvetica-Bold", 26)
        pdf.drawString(MARGIN + 18, y, line)
        y -= 30

    pdf.setFillColor(colors.HexColor("#ffd166"))
    pdf.roundRect(MARGIN + 18, top - 100, PAGE_WIDTH - (2 * MARGIN) - 36, 28, 12, fill=1, stroke=0)
    pdf.setFillColor(colors.HexColor("#073b4c"))
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(MARGIN + 30, top - 89, tagline[:95])


def _draw_feature_panel(
    pdf: canvas.Canvas,
    poster_data: dict[str, object],
    poster_image_bytes: bytes | None,
) -> None:
    body = _clean_text(
        poster_data.get("main_body"),
        "Share the key event details, why it matters, and what attendees can expect.",
    )

    panel_x = MARGIN
    panel_y = PAGE_HEIGHT - 420
    panel_width = PAGE_WIDTH - (2 * MARGIN)
    panel_height = 165

    pdf.setFillColor(colors.white)
    pdf.roundRect(panel_x, panel_y, panel_width, panel_height, 18, fill=1, stroke=0)

    pdf.setFillColor(colors.HexColor("#ef476f"))
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(panel_x + 18, panel_y + panel_height - 28, "Why You Should Attend")

    image_width = 0
    if poster_image_bytes:
        image_width = _draw_feature_image(
            pdf,
            panel_x + panel_width - 150,
            panel_y + 18,
            132,
            panel_height - 36,
            poster_image_bytes,
        )

    pdf.setFillColor(colors.HexColor("#1f2933"))
    pdf.setFont("Helvetica", 13)
    body_width = panel_width - 36 - image_width
    lines = simpleSplit(body, "Helvetica", 13, body_width)
    y = panel_y + panel_height - 55
    for line in lines[:7]:
        pdf.drawString(panel_x + 18, y, line)
        y -= 18


def _draw_feature_image(
    pdf: canvas.Canvas,
    x: float,
    y: float,
    max_width: float,
    max_height: float,
    image_bytes: bytes,
) -> float:
    image_reader = ImageReader(BytesIO(image_bytes))
    img_width, img_height = image_reader.getSize()
    if img_width <= 0 or img_height <= 0:
        return 0

    scale = min(max_width / img_width, max_height / img_height)
    draw_width = img_width * scale
    draw_height = img_height * scale

    frame_x = x - 8
    frame_y = y - 8
    frame_width = draw_width + 16
    frame_height = draw_height + 16

    pdf.setFillColor(colors.HexColor("#ffd166"))
    pdf.roundRect(frame_x, frame_y, frame_width, frame_height, 16, fill=1, stroke=0)
    pdf.drawImage(
        image_reader,
        x,
        y + max(0, (max_height - draw_height) / 2),
        width=draw_width,
        height=draw_height,
        preserveAspectRatio=True,
        mask="auto",
    )
    return frame_width + 16


def _draw_highlights_panel(pdf: canvas.Canvas, poster_data: dict[str, object]) -> None:
    bullet_items = [
        str(item).strip()
        for item in poster_data.get("bullet_highlights", [])
        if str(item).strip()
    ]
    if not bullet_items:
        bullet_items = [
            "Interactive highlights",
            "Useful takeaways",
            "A welcoming audience experience",
        ]

    panel_x = MARGIN
    panel_y = 150
    panel_width = PAGE_WIDTH - (2 * MARGIN)
    panel_height = 180

    pdf.setFillColor(colors.HexColor("#118ab2"))
    pdf.roundRect(panel_x, panel_y, panel_width, panel_height, 18, fill=1, stroke=0)

    pdf.setFillColor(colors.white)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(panel_x + 18, panel_y + panel_height - 28, "Highlights")

    y = panel_y + panel_height - 58
    for item in bullet_items[:5]:
        wrapped = simpleSplit(item, "Helvetica", 12, panel_width - 58)
        first_line = True
        for line in wrapped[:3]:
            if first_line:
                pdf.setFont("Helvetica-Bold", 13)
                pdf.drawString(panel_x + 22, y, "•")
                pdf.setFont("Helvetica", 12)
                pdf.drawString(panel_x + 38, y, line)
                first_line = False
            else:
                pdf.drawString(panel_x + 38, y, line)
            y -= 16
        y -= 8
        if y < panel_y + 18:
            break


def _draw_call_to_action(pdf: canvas.Canvas, poster_data: dict[str, object]) -> None:
    call_to_action = _clean_text(
        poster_data.get("call_to_action"),
        "Join us and learn more.",
    )

    panel_x = MARGIN
    panel_y = 58
    panel_width = PAGE_WIDTH - (2 * MARGIN)
    panel_height = 62

    pdf.setFillColor(colors.HexColor("#073b4c"))
    pdf.roundRect(panel_x, panel_y, panel_width, panel_height, 20, fill=1, stroke=0)

    pdf.setFillColor(colors.white)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, panel_y + 38, "Take Action")

    pdf.setFont("Helvetica", 12)
    cta_lines = simpleSplit(call_to_action, "Helvetica", 12, panel_width - 36)
    y = panel_y + 20
    for line in cta_lines[:2]:
        pdf.drawCentredString(PAGE_WIDTH / 2, y, line)
        y -= 14


def _clean_text(value: object, default: str) -> str:
    text = str(value).strip() if value is not None else ""
    return text or default
