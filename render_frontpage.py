#!/usr/bin/env python3
"""Render the news-image-01 front page for Friday 13 November 2026.

Draws a dense newspaper front page with PIL and real fonts (no AI text):
a masthead, a lead story, and a two-column grid of 24 more stories, so the
image itself sums up the day's world news in legible type. Writes entry.png
(1024x1024 JPEG bytes under that name, under 1 MiB).
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 26
BG = (255, 255, 255)
INK = (18, 18, 18)
RULE = (18, 18, 18)
ACCENT = (178, 34, 34)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

def wrap(draw, text, fnt, width):
    """Greedy word wrap to the given pixel width; returns a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

# (category, headline) — 24 stories after the lead, in rough importance order.
STORIES = [
    ("TECH", "Nvidia chief Jensen Huang resigns; shares plunge 14%"),
    ("TECH", "Microsoft 365 outage enters day two; Outlook and Teams down"),
    ("ASIA", "China holds large unannounced naval drills around Taiwan"),
    ("U.S.", "FAA lifts nationwide ground stop after comms failure"),
    ("EUROPE", "Europe joins Ukraine peace talks; largest prisoner swap begins"),
    ("U.S.", "Brooklyn collapse toll settles at 8 dead, 18 injured"),
    ("U.S.", "Van Hollen challenges Schumer for Senate leadership"),
    ("CRYPTO", "U.S. to seize $1.2B from Binance hack blamed on North Korea"),
    ("VATICAN", "Pope Leo meets abuse survivors in Peru; record crowds"),
    ("INDIA", "Delhi overtakes Lahore as world's most polluted city"),
    ("INDIA", "23 die in bus-truck collision near Kaziranga, Assam"),
    ("MIDDLE EAST", "Qatar and Turkey sign mutual defense pact"),
    ("ENERGY", "IEA forecasts oil surplus; Brent crude jumps to $95.82"),
    ("TECH", "U.S. officials clash over Nvidia chip export controls"),
    ("HEALTH", "Measles elimination ruling awaited for U.S. and Mexico"),
    ("SYRIA", "French warship docks in Latakia for the first time"),
    ("MARKETS", "Wall Street falls 0.4% after Nvidia drop"),
    ("IRAN", "IAEA warns over Iran's uninspected Isfahan plant"),
    ("MIDDLE EAST", "Israeli strikes in south Lebanon; 3 killed in Gaza"),
    ("RUSSIA", "Moscow car bomb wounds ex-aide to Ukrainian PM"),
    ("YEMEN", "Saudi Arabia urges EU to list Houthis as terrorists"),
    ("INDIA", "U.S. assures India of tariff advantage over rivals"),
]

def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    x0, x1 = MARGIN, W - MARGIN
    y = MARGIN

    # Masthead
    f_mast = font(SERIF_B, 62)
    mast = "THE WORLD TODAY"
    d.text(((W - d.textlength(mast, font=f_mast)) / 2, y), mast, font=f_mast, fill=INK)
    y += 78
    f_date = font(SANS_B, 30)
    date = "FRIDAY 13 NOVEMBER 2026"
    d.text(((W - d.textlength(date, font=f_date)) / 2, y), date, font=f_date, fill=ACCENT)
    y += 44
    d.line([(x0, y), (x1, y)], fill=RULE, width=3)
    y += 14

    # Lead story
    f_lead = font(SERIF_B, 44)
    lead = "IRAN STRIKES U.S. RADAR AS TANKERS BURN IN HORMUZ"
    for line in wrap(d, lead, f_lead, x1 - x0):
        d.text((x0, y), line, font=f_lead, fill=INK)
        y += 50
    f_leadsub = font(SANS, 22)
    sub = "Tehran says it destroyed a U.S. early-warning radar in Bahrain, in retaliation for a U.S. strike on a telecom tower in Sirik."
    for line in wrap(d, sub, f_leadsub, x1 - x0):
        d.text((x0, y), line, font=f_leadsub, fill=INK)
        y += 28
    y += 8
    d.line([(x0, y), (x1, y)], fill=RULE, width=2)
    y += 12

    # Two-column story grid
    col_w = (x1 - x0 - 24) // 2
    f_cat = font(SANS_B, 15)
    f_head = font(SANS_B, 19)
    row_h = 60
    for i, (cat, head) in enumerate(STORIES):
        col = i % 2
        row = i // 2
        cx = x0 + col * (col_w + 24)
        cy = y + row * row_h
        d.text((cx, cy), cat, font=f_cat, fill=ACCENT)
        lines = wrap(d, head, f_head, col_w)
        ly = cy + 19
        for line in lines[:2]:
            d.text((cx, ly), line, font=f_head, fill=INK)
            ly += 22

    img.save("entry.png", "JPEG", quality=92)

if __name__ == "__main__":
    main()
