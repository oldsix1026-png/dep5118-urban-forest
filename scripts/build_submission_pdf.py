from pathlib import Path
from io import BytesIO

from PIL import Image
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


ROOT = Path(r"D:\x=0\Y2S1\DEP5118\ITA2")
SCREENSHOT_DIR = ROOT / "Submission" / "Screenshot"
OUTPUT = ROOT / "Submission" / "DEP5118_ITA2_500000_Trees_Submission_Final_v3.pdf"

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
    buffer = BytesIO()
    img_for_pdf.save(buffer, format="JPEG", quality=92)
    buffer.seek(0)
    c.drawImage(
        ImageReader(buffer),
        x,
        y + max_h - draw_h,
        draw_w,
        draw_h,
        preserveAspectRatio=True,
        mask="auto",
    )


def draw_image_cover(c, image_path, x, y, box_w, box_h):
    with Image.open(image_path) as img:
        if img.mode in ("RGBA", "LA"):
            background = Image.new("RGB", img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1])
            img = background
        else:
            img = img.convert("RGB")

        img_w, img_h = img.size
        scale = max(box_w / img_w, box_h / img_h)
        crop_w = int(box_w / scale)
        crop_h = int(box_h / scale)
        left = max(0, (img_w - crop_w) // 2)
        top = max(0, (img_h - crop_h) // 2)
        cropped = img.crop((left, top, left + crop_w, top + crop_h))

    buffer = BytesIO()
    cropped.save(buffer, format="JPEG", quality=92)
    buffer.seek(0)
    c.drawImage(ImageReader(buffer), x, y, box_w, box_h, preserveAspectRatio=False, mask="auto")


def draw_page_header(c, label):
    c.setFillColor(GREEN)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(MARGIN, PAGE_H - 36, label)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 9)
    c.drawRightString(PAGE_W - MARGIN, PAGE_H - 34, f"By {AUTHOR}")


def build():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUTPUT), pagesize=landscape(A4))

    draw_page_header(c, TITLE)
    c.setFont("Helvetica-Bold", 13)
    c.setFillColor(ACCENT)
    c.drawString(MARGIN, PAGE_H - 66, "Story intention")
    y = draw_wrapped(c, INTENTION, MARGIN, PAGE_H - 88, PAGE_W - MARGIN * 2, size=9.6, leading=12)
    y -= 12
    c.setFillColor(colors.HexColor("#e7f1eb"))
    c.roundRect(MARGIN, y - 18, PAGE_W - MARGIN * 2, 30, 6, stroke=0, fill=1)
    draw_wrapped(c, URL_TEXT, MARGIN + 14, y - 8, PAGE_W - MARGIN * 2 - 28, font="Helvetica-Bold", size=12, color=ACCENT)

    cover = SCREENSHOT_DIR / "Cover.png"
    if cover.exists():
        draw_image_cover(c, cover, MARGIN, 32, PAGE_W - MARGIN * 2, 310)
    c.showPage()

    for i, (title, text, filename) in enumerate(CHAPTERS, start=1):
        draw_page_header(c, title)
        c.setFillColor(PANEL)
        c.roundRect(MARGIN, PAGE_H - 128, PAGE_W - MARGIN * 2, 64, 8, stroke=0, fill=1)
        draw_wrapped(c, text, MARGIN + 16, PAGE_H - 86, PAGE_W - MARGIN * 2 - 32, size=9.7, leading=12.3)
        screenshot = SCREENSHOT_DIR / filename
        if screenshot.exists():
            draw_image_cover(c, screenshot, MARGIN, 34, PAGE_W - MARGIN * 2, PAGE_H - 182)
        c.showPage()

    c.save()
    print(OUTPUT)


if __name__ == "__main__":
    build()
