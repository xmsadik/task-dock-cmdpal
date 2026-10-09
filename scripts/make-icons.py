"""Regenerate the package icons in src/ClaudeTasks/Assets.

Usage: python scripts/make-icons.py   (needs Pillow)

The mark is a slate rounded square with a white check mark over a progress bar.
Everything is drawn at 1024 px and downsampled, so small sizes stay smooth.
"""

from pathlib import Path

from PIL import Image, ImageDraw

ASSETS = Path(__file__).resolve().parent.parent / "src" / "ClaudeTasks" / "Assets"
BASE = 1024
TILE = (44, 62, 80, 255)  # slate
INK = (255, 255, 255, 255)
TRACK = (255, 255, 255, 70)
FILL = (34, 197, 94, 255)  # green: done


def stroke(d: ImageDraw.ImageDraw, points: list[tuple[float, float]], width: float) -> None:
    """Polyline with round caps and joins."""
    d.line(points, fill=INK, width=int(width), joint="curve")
    r = width / 2
    for x, y in points:
        d.ellipse((x - r, y - r, x + r, y + r), fill=INK)


def icon(size: int) -> Image.Image:
    img = Image.new("RGBA", (BASE, BASE), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, BASE - 1, BASE - 1), radius=int(BASE * 0.22), fill=TILE)

    # Check mark in the upper part of the tile.
    stroke(d, [(BASE * 0.27, BASE * 0.43), (BASE * 0.43, BASE * 0.58), (BASE * 0.74, BASE * 0.25)], BASE * 0.10)

    # Progress bar: faint track, about three quarters filled.
    x0, x1, y0, y1 = BASE * 0.20, BASE * 0.80, BASE * 0.70, BASE * 0.80
    r = (y1 - y0) / 2
    overlay = Image.new("RGBA", (BASE, BASE), (0, 0, 0, 0))
    ImageDraw.Draw(overlay).rounded_rectangle((x0, y0, x1, y1), radius=r, fill=TRACK)
    img.alpha_composite(overlay)
    d.rounded_rectangle((x0, y0, x0 + (x1 - x0) * 0.72, y1), radius=r, fill=FILL)

    return img.resize((size, size), Image.LANCZOS)


def centered(width: int, height: int, mark: int) -> Image.Image:
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    img.alpha_composite(icon(mark), ((width - mark) // 2, (height - mark) // 2))
    return img


def main() -> None:
    squares = {
        "StoreLogo.png": 50,
        "LockScreenLogo.scale-200.png": 48,
        "Square44x44Logo.scale-200.png": 88,
        "Square44x44Logo.targetsize-24_altform-unplated.png": 24,
        "Square150x150Logo.scale-200.png": 300,
    }
    for name, size in squares.items():
        icon(size).save(ASSETS / name)

    centered(620, 300, 200).save(ASSETS / "Wide310x150Logo.scale-200.png")
    centered(1240, 600, 360).save(ASSETS / "SplashScreen.scale-200.png")
    print(f"Wrote {len(squares) + 2} icons to {ASSETS}")


if __name__ == "__main__":
    main()
