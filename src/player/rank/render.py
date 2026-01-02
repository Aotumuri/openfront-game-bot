from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

from player.rank.constants import RANK_COLORS, RANK_FONT_PATH


def _load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    try:
        return ImageFont.truetype(RANK_FONT_PATH, size=size)
    except OSError as exc:
        raise RuntimeError(
            f"Invalid font file at {RANK_FONT_PATH}. Please place a valid .ttf file."
        ) from exc


def build_rank_png(rank: str, progress: float) -> bytes:
    progress = max(0.0, min(1.0, progress))
    size = 200
    stroke_width = 12
    radius = 80
    center = size // 2
    bbox = (
        center - radius,
        center - radius,
        center + radius,
        center + radius,
    )

    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.ellipse(bbox, outline="#d0d7de", width=stroke_width)

    if progress > 0:
        stroke = RANK_COLORS.get(rank, "#1f8b4c")
        start_angle = -90
        end_angle = start_angle + 360 * progress
        draw.arc(bbox, start=start_angle, end=end_angle, fill=stroke, width=stroke_width)

    font = _load_font(56)
    text = rank
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    text_pos = (center - text_width / 2, center - text_height / 2 - 4)
    text_fill = RANK_COLORS.get(rank, "#1f8b4c")
    draw.text(text_pos, text, font=font, fill=text_fill)

    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()
