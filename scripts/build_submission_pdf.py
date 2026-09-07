from pathlib import Path

from PIL import Image
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


ROOT = Path(r"D:\x=0\Y2S1\DEP5118\ITA2")
SCREENSHOT_DIR = ROOT / "Submission" / "Screenshot"
OUTPUT = ROOT / "Submission" / "DEP5118_ITA2_500000_Trees_Submission_Final_v2.pdf"

PAGE_W, PAGE_H = landscape(A4)
MARGIN = 36
GREEN = colors.HexColor("#24352b")
MUTED = colors.HexColor("#5f6d64")
ACCENT = colors.HexColor("#2f8f5b")
PANEL = colors.HexColor("#fbfaf5")

TITLE = "500,000 Trees: Singapore's Urban Forest"
AUTHOR = "Zhou Jiaxuan"
URL_TEXT = "Website URL: https://oldsix1026-png.github.io/dep5118-urban-forest/"

INTENTION = (
    "Singapore is often described as the City in Nature. This story starts from that policy "
    "background and reads trees as more than greenery. Trees support shade, comfort, memory, "
    "and everyday urban life, so they can be understood as city infrastructure and living "
    "heritage. The StoryMap moves from island-wide green structure to protected Heritage "
    "Tree patterns, access context, conservation areas, and finally one tree in Singapore "
    "Botanic Gardens."
)

CHAPTERS = [
    (
        "Chapter 1: Singapore as an Urban Forest",
        "The opening view sets up Singapore's City in Nature background. Parks and nature reserves "
        "form the green base of the urban forest, while a faint density layer hints that protected "
        "trees are not spread evenly across the island.",
        "Chapter 1.png",
    ),
    (
        "Chapter 2: Where the Urban Forest Is Protected",
        "This chapter maps Heritage Trees per square kilometre by subzone. It does not represent all "
        "street trees. The stronger clusters appear around historic, institutional, park, and landscape "
        "areas where mature trees have been formally recognised.",
        "Chapter 2.png",
    ),
    (
        "Chapter 3: From Tree Density to Everyday Access",
        "The story then asks whether protected tree concentration also means everyday access. The map "
        "uses Heritage Trees per 100 HDB buildings as a proxy. It is not a walking-distance model, but "
        "it compares protected trees with residential context.",
        "Chapter 3.png",
    ),
    (
        "Chapter 4: Trees That Carry Memory",
        "After the density and access views, the map returns to individual Heritage Trees and Tree "
        "Conservation Areas. This shifts the story from quantity to value, protection, and urban memory.",
        "Chapter 4.png",
    ),
    (
        "Chapter 5: One Tree, One Story",
        "The final view zooms to a small group of Heritage Trees in Singapore Botanic Gardens, beginning "
        "with Chengal Pasir. Clicking each orange point opens a short card with its name, location, "
        "photo, and NParks profile link.",
        "Chapter 5.png",
    ),
]


def draw_wrapped(c, text, x, y, width, font="Helvetica", size=10.5, leading=14, color=GREEN):
    c.setFillColor(color)
    c.setFont(font, size)
    words = text.split()
    lines = []
    line = ""
    for word in words:
        test = f"{line} {word}".strip()
        if c.stringWidth(test, font, size) <= width:
            line = test
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)

    for line in lines:
        c.drawString(x, y, line)
        y -= leading
    return y


def draw_image_fit(c, image_path, x, y, max_w, max_h):
    with Image.open(image_path) as img:
        img_w, img_h = img.size
        if img.mode in ("RGBA", "LA"):
            background = Image.new("RGB", img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1])
            img_for_pdf = background
        else:
            img_for_pdf = img.convert("RGB")
    scale = min(max_w / img_w, max_h / img_h)
    draw_w = img_w * scale
    draw_h = img_h * scale
    c.drawImage(
        ImageReader(img_for_pdf),
        x,
        y + max_h - draw_h,
        draw_w,
        draw_h,
        preserveAspectRatio=True,
        mask="auto",
    )


def draw_page_header(c, label):
    c.setFillColor(GREEN)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(MARGIN, PAGE_H - 36, label)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 9)
    c.drawRightString(PAGE_W - MARGIN, PAGE_H - 34, f"By {AUTHOR}")


def draw_photo_strip(c, image_names, x, y, tile_w=64, tile_h=48, gap=8):
    for i, name in enumerate(image_names):
        path = ROOT / "urban-forest" / "assets" / name
        if not path.exists():
            continue
        c.setFillColor(colors.white)
        c.roundRect(x + i * (tile_w + gap), y, tile_w, tile_h, 5, stroke=0, fill=1)
        draw_image_fit(c, path, x + i * (tile_w + gap), y, tile_w, tile_h)


def draw_photo_grid(c, image_names, x, y, tile_w=136, tile_h=96, gap=12):
    c.setFillColor(ACCENT)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x, y + tile_h * 2 + gap + 22, "Heritage Tree photos")
    for i, name in enumerate(image_names):
        path = ROOT / "urban-forest" / "assets" / name
        if not path.exists():
            continue
        col = i % 2
        row = i // 2
        px = x + col * (tile_w + gap)
        py = y + (1 - row) * (tile_h + gap)
        if i == 4:
            px = x
            py = y - tile_h - gap
            current_w = tile_w * 2 + gap
        else:
            current_w = tile_w
        c.setFillColor(colors.white)
        c.roundRect(px, py, current_w, tile_h, 5, stroke=0, fill=1)
        draw_image_fit(c, path, px, py, current_w, tile_h)


def build():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUTPUT), pagesize=landscape(A4))

    draw_page_header(c, TITLE)
    c.setFont("Helvetica-Bold", 13)
    c.setFillColor(ACCENT)
    c.drawString(MARGIN, PAGE_H - 66, "Story intention")
    y = draw_wrapped(c, INTENTION, MARGIN, PAGE_H - 88, 360, size=10.5)
    y -= 10
    draw_wrapped(c, URL_TEXT, MARGIN, y, 360, font="Helvetica-Bold", size=10, color=MUTED)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 8.5)
    c.drawString(MARGIN, 28, "Website published through GitHub Pages.")
    draw_photo_strip(c, ["chengal-pasir.png", "tembusu.jpg", "teak.jpg", "nemesu.jpg", "saga.jpg"], MARGIN, 84)

    cover = SCREENSHOT_DIR / "Cover.png"
    if cover.exists():
        draw_image_fit(c, cover, MARGIN + 390, 46, PAGE_W - MARGIN * 2 - 390, PAGE_H - 90)
    c.showPage()

    for i, (title, text, filename) in enumerate(CHAPTERS, start=1):
        draw_page_header(c, title)
        c.setFillColor(PANEL)
        c.roundRect(MARGIN, PAGE_H - 128, PAGE_W - MARGIN * 2, 64, 8, stroke=0, fill=1)
        draw_wrapped(c, text, MARGIN + 16, PAGE_H - 86, PAGE_W - MARGIN * 2 - 32, size=9.7, leading=12.3)
        screenshot = SCREENSHOT_DIR / filename
        if screenshot.exists():
            if i == 5:
                draw_image_fit(c, screenshot, MARGIN, 38, 255, PAGE_H - 178)
                draw_photo_grid(
                    c,
                    ["chengal-pasir.png", "tembusu.jpg", "teak.jpg", "nemesu.jpg", "saga.jpg"],
                    MARGIN + 292,
                    150,
                )
            else:
                draw_image_fit(c, screenshot, MARGIN, 38, PAGE_W - MARGIN * 2, PAGE_H - 178)
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 8.5)
        c.drawRightString(PAGE_W - MARGIN, 20, f"Storyboard page {i}")
        c.showPage()

    c.save()
    print(OUTPUT)


if __name__ == "__main__":
    build()
