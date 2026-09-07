from pathlib import Path

from PIL import Image
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


ROOT = Path(r"D:\x=0\Y2S1\DEP5118\ITA2")
SCREENSHOT_DIR = ROOT / "Submission" / "Screenshot"
OUTPUT = ROOT / "Submission" / "DEP5118_ITA2_500000_Trees_Submission_Final.pdf"

PAGE_W, PAGE_H = landscape(A4)
MARGIN = 36
GREEN = colors.HexColor("#24352b")
MUTED = colors.HexColor("#5f6d64")
ACCENT = colors.HexColor("#2f8f5b")
PANEL = colors.HexColor("#fbfaf5")

TITLE = "500,000 Trees: Singapore's Urban Forest"
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
    scale = min(max_w / img_w, max_h / img_h)
    draw_w = img_w * scale
    draw_h = img_h * scale
    c.drawImage(ImageReader(str(image_path)), x, y + max_h - draw_h, draw_w, draw_h, preserveAspectRatio=True, mask="auto")


def draw_page_header(c, label):
    c.setFillColor(ACCENT)
    c.rect(0, PAGE_H - 8, PAGE_W, 8, stroke=0, fill=1)
    c.setFillColor(GREEN)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(MARGIN, PAGE_H - 42, label)


def build():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUTPUT), pagesize=landscape(A4))

    draw_page_header(c, TITLE)
    c.setFont("Helvetica-Bold", 13)
    c.setFillColor(ACCENT)
    c.drawString(MARGIN, PAGE_H - 72, "Story intention")
    y = draw_wrapped(c, INTENTION, MARGIN, PAGE_H - 94, 350, size=10.5)
    y -= 10
    draw_wrapped(c, URL_TEXT, MARGIN, y, 350, font="Helvetica-Bold", size=10, color=MUTED)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 8.5)
    c.drawString(MARGIN, 28, "Website published through GitHub Pages.")

    cover = SCREENSHOT_DIR / "Cover.png"
    if cover.exists():
        draw_image_fit(c, cover, MARGIN + 380, 54, PAGE_W - MARGIN * 2 - 380, PAGE_H - 108)
    c.showPage()

    for i, (title, text, filename) in enumerate(CHAPTERS, start=1):
        draw_page_header(c, title)
        c.setFillColor(PANEL)
        c.roundRect(MARGIN, PAGE_H - 158, PAGE_W - MARGIN * 2, 82, 8, stroke=0, fill=1)
        draw_wrapped(c, text, MARGIN + 16, PAGE_H - 102, PAGE_W - MARGIN * 2 - 32, size=10.5)
        screenshot = SCREENSHOT_DIR / filename
        if screenshot.exists():
            draw_image_fit(c, screenshot, MARGIN, 38, PAGE_W - MARGIN * 2, PAGE_H - 214)
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 8.5)
        c.drawRightString(PAGE_W - MARGIN, 20, f"Storyboard page {i}")
        c.showPage()

    c.save()
    print(OUTPUT)


if __name__ == "__main__":
    build()
