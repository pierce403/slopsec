#!/usr/bin/env python3
from pathlib import Path
import random

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "og-card.png"
RABBIT = ROOT / "assets" / "hacker-rabbit.png"

WIDTH = 1200
HEIGHT = 630
GREEN = (166, 255, 47)
SOFT = (93, 255, 100)
AMBER = (255, 209, 102)
BLACK = (2, 3, 2)


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/{name}.ttf", size)


def text(draw: ImageDraw.ImageDraw, xy: tuple[int, int], value: str, fill, fnt, glow=0):
    if glow:
        layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        glow_draw = ImageDraw.Draw(layer)
        glow_draw.text(xy, value, font=fnt, fill=(*fill[:3], 120))
        layer = layer.filter(ImageFilter.GaussianBlur(glow))
        draw.bitmap((0, 0), layer, fill=None)
    draw.text(xy, value, font=fnt, fill=fill)


def main() -> None:
    random.seed(31337)
    img = Image.new("RGB", (WIDTH, HEIGHT), BLACK)
    draw = ImageDraw.Draw(img)

    for y in range(HEIGHT):
        shade = int(5 + y * 11 / HEIGHT)
        draw.line((0, y, WIDTH, y), fill=(0, shade, 1))

    for _ in range(220):
        x = random.randrange(0, WIDTH)
        y = random.randrange(0, HEIGHT)
        w = random.randrange(8, 74)
        alpha = random.randrange(22, 92)
        color = (GREEN[0] * alpha // 255, GREEN[1] * alpha // 255, GREEN[2] * alpha // 255)
        draw.rectangle((x, y, min(WIDTH, x + w), y + 2), fill=color)

    rabbit = Image.open(RABBIT).convert("RGBA")
    rabbit = rabbit.resize((660, 660), Image.Resampling.LANCZOS)
    rabbit = rabbit.crop((0, 18, 660, 630))

    glow = Image.new("RGBA", rabbit.size, (0, 0, 0, 0))
    glow.alpha_composite(rabbit)
    glow = glow.filter(ImageFilter.GaussianBlur(18))
    img.paste(glow, (548, 3), glow)
    img.paste(rabbit, (562, 0), rabbit)

    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rectangle((0, 0, 760, HEIGHT), fill=(0, 0, 0, 178))
    overlay_draw.rectangle((0, 0, WIDTH, HEIGHT), outline=(*GREEN, 120), width=2)
    img = Image.alpha_composite(img.convert("RGBA"), overlay)
    draw = ImageDraw.Draw(img)

    mono = font("DejaVuSansMono", 30)
    title = font("DejaVuSansMono-Bold", 128)
    subtitle = font("DejaVuSansMono-Bold", 38)
    small = font("DejaVuSansMono", 28)

    text(draw, (66, 62), "pierce@slopsec:~$ ./preview", AMBER, mono, glow=2)
    text(draw, (62, 132), "slopsec", GREEN, title, glow=6)
    text(draw, (70, 286), "sketchy shit,", SOFT, subtitle, glow=3)
    text(draw, (70, 336), "non-deterministic prices", SOFT, subtitle, glow=3)
    text(draw, (72, 436), "AI security research & consulting", (217, 255, 216), small, glow=2)
    text(draw, (72, 481), "agentic systems // LLM apps // evals", (123, 202, 130), small, glow=1)

    for y in range(0, HEIGHT, 4):
        draw.line((0, y, WIDTH, y), fill=(0, 0, 0, 46), width=1)

    OUT.parent.mkdir(exist_ok=True)
    img.convert("RGB").save(OUT, quality=95)


if __name__ == "__main__":
    main()
