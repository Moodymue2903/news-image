#!/usr/bin/env python3
"""Render the news-image-01 v3 front page for Friday 13 November 2026.

An infographic-style one-page summary (33 stories, 6 continents) in the
shape of the day's top-scoring entry: a masthead with a story/continent
count and colour legend, three big top stories, a numbered 3-column grid
of 12 more stories, an "ALSO ON FRIDAY" briefs block, and a schematic
world map with numbered dots. All type is real (PIL + DejaVu fonts), so
every headline is legible. Writes entry.png (1024x1024 JPEG, under 1 MiB).
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 24
BG = (253, 248, 238)
INK = (22, 22, 22)
RULE = (22, 22, 22)
ACCENT = (178, 34, 34)
MUTED = (90, 84, 74)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# Continent colours (used for the dots and legend).
CONT = {
    "N. America": (198, 52, 44),
    "S. America": (214, 128, 32),
    "Europe": (46, 110, 190),
    "Africa": (34, 139, 90),
    "Asia": (128, 66, 160),
    "Oceania": (20, 140, 160),
    "Global": (110, 110, 110),
}

def font(path, size):
    return ImageFont.truetype(path, size)

def wrap(draw, text, fnt, width):
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

def dot(d, cx, cy, r, colour):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=colour)

# (number, continent, category, headline, subline)
TOP3 = [
    (1, "N. America", "UNITED STATES · AVIATION",
     "FAA grounds every US departure for four hours",
     "Telecoms failed at 4 pm ET; flights resumed at 8:15 pm."),
    (2, "Asia", "MIDDLE EAST · IRAN WAR",
     "Iran says it hit a US radar in Bahrain; US denies it",
     "Tehran calls it payback for a US strike at Sirik."),
    (3, "Asia", "ASIA · DIPLOMACY",
     "Trump, Xi and Putin to hold a first three-way summit",
     "The White House sets it for 19 November in China."),
]

# (number, continent, category, headline, subline) — main grid, 12 stories.
GRID = [
    (4, "Europe", "UKRAINE WAR", "Ukraine fires about 1,200 drones at Russia", "Four dead in Volgograd, Russia says"),
    (5, "Europe", "EUROPE · DIPLOMACY", "Europe names its team for Ukraine peace talks", "EU and five nations; agreed in Dublin"),
    (6, "N. America", "SCIENCE · SPACE", "Starship reaches orbit on 15th test flight", "26 satellites out; booster catch off"),
    (7, "S. America", "PERU · RELIGION", "Pope Leo XIV says Mass in Peru", "Vast crowd in his former diocese"),
    (8, "Asia", "INDIA · ROAD CRASH", "Bus crash in Assam, India, kills at least 24", "Head-on with a truck, police say"),
    (9, "Asia", "TÜRKIYE · QATAR", "Türkiye and Qatar sign mutual defence pact", "Erdogan and Emir Tamim, in Istanbul"),
    (10, "Global", "GLOBAL · TECH", "Microsoft 365 back after 24-hour outage", "Worldwide; not a cyber-attack, it says"),
    (11, "Africa", "DR CONGO · HEALTH", "Ebola still spreading in DR Congo, WHO says", "400 to 500 new cases every week"),
    (12, "N. America", "UNITED STATES · ACCIDENT", "Tanker hits docked New Orleans riverboat", "It capsizes; all 197 aboard rescued"),
    (13, "Global", "MARKETS · TECH", "Nvidia's value falls below $4 trillion", "Lost about $650bn in value this week"),
    (14, "Europe", "SPORT · FOOTBALL", "Pochettino leaves USA for Manchester United", "Signs a two-and-a-half-year deal"),
    (15, "Global", "CLIMATE · COP31", "UN chief: 1.5°C overshoot \"inevitable\"", "Guterres at COP31 in Antalya, Türkiye"),
]

# (number, brief) — "ALSO ON FRIDAY" one-liners, 18 more stories.
BRIEFS = [
    (16, "Norway: court voids 3 oil licences"),
    (17, "Moscow: car bomb wounds ex-Kyiv aide"),
    (18, "Iberia: Storm Charles floods towns"),
    (19, "Japan: yen tests 160 per dollar"),
    (20, "Kenya: building collapse kills six"),
    (21, "Guinea: 10 die in gold-mine clashes"),
    (22, "Delhi now world's most polluted city"),
    (23, "US to seize $1.2B from Binance hack"),
    (24, "Van Hollen challenges Schumer"),
    (25, "Brooklyn collapse toll settles at 8 dead"),
    (26, "IAEA warns over Iran's Isfahan plant"),
    (27, "Israeli strikes in Lebanon; 3 killed in Gaza"),
    (28, "Saudis urge EU to list Houthis as terrorists"),
    (29, "French warship docks in Latakia"),
    (30, "Measles ruling awaited for US and Mexico"),
    (31, "US assures India of tariff advantage"),
    (32, "Wall Street falls 0.4% after Nvidia drop"),
    (33, "IEA: oil surplus; Brent jumps to $95.82"),
]

# Coarse continent polygons in lon/lat-ish coords (x: -180..180, y: 90..-60).
# Deliberately rough — a schematic map, not a survey.
LAND = [
    # North America
    [(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 69), (-82, 66), (-76, 60), (-70, 58), (-65, 45), (-70, 42), (-75, 35), (-80, 32), (-81, 26), (-84, 30), (-90, 30), (-97, 26), (-97, 16), (-105, 20), (-110, 23), (-117, 33), (-125, 40), (-125, 49), (-135, 58), (-155, 58), (-165, 60)],
    # Greenland
    [(-58, 64), (-45, 60), (-32, 68), (-22, 70), (-30, 76), (-45, 76), (-58, 74)],
    # South America
    [(-80, 9), (-77, 4), (-80, -3), (-81, -6), (-77, -12), (-72, -18), (-70, -23), (-70, -30), (-72, -37), (-73, -44), (-70, -50), (-66, -55), (-68, -52), (-62, -45), (-58, -38), (-52, -32), (-48, -28), (-41, -23), (-35, -9), (-35, -6), (-43, -3), (-50, 0), (-55, 5), (-62, 9), (-72, 11)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 48), (-4, 50), (2, 51), (8, 57), (10, 59), (18, 56), (21, 55), (24, 58), (30, 60), (30, 66), (25, 70), (18, 69), (12, 65), (5, 58), (5, 53), (8, 55), (8, 50), (12, 54), (19, 54), (23, 54), (28, 54), (28, 47), (23, 40), (19, 42), (13, 44), (8, 44), (3, 42), (-2, 37)],
    # Africa
    [(-6, 35), (10, 37), (20, 32), (30, 31), (32, 31), (35, 28), (37, 22), (39, 18), (43, 12), (51, 11), (51, 2), (46, -2), (40, -10), (36, -18), (32, -26), (28, -33), (20, -35), (16, -29), (12, -18), (9, -1), (9, 4), (-8, 4), (-13, 8), (-17, 15), (-16, 20), (-15, 27), (-10, 31)],
    # Asia
    [(30, 66), (40, 68), (50, 69), (60, 69), (70, 72), (80, 73), (90, 75), (100, 77), (110, 74), (120, 73), (130, 72), (140, 72), (150, 70), (160, 69), (170, 67), (178, 65), (170, 60), (162, 58), (158, 52), (150, 59), (142, 54), (142, 50), (140, 45), (135, 43), (130, 42), (127, 40), (122, 38), (120, 32), (122, 28), (120, 22), (110, 20), (108, 18), (105, 10), (100, 8), (98, 10), (95, 16), (92, 21), (89, 22), (86, 20), (80, 15), (77, 8), (75, 12), (72, 20), (68, 23), (62, 25), (57, 26), (52, 26), (50, 29), (48, 30), (44, 29), (42, 29), (39, 21), (35, 28), (32, 31)],
    # Australia
    [(114, -22), (114, -30), (115, -35), (120, -34), (125, -32), (130, -32), (135, -35), (140, -38), (145, -38), (150, -37), (153, -32), (153, -27), (150, -22), (146, -19), (142, -11), (136, -12), (132, -11), (126, -14), (122, -17), (118, -20)],
]

# Story locations on the map (lon, lat, story number).
MAP_DOTS = [
    (-100, 39, 1), (-60, 30, 2), (100, 35, 3), (35, 50, 4), (10, 50, 5),
    (-100, 35, 6), (-75, -10, 7), (92, 26, 8), (32, 40, 9), (0, 20, 10),
    (25, 0, 11), (-90, 30, 12), (-100, 35, 13), (-5, 50, 14), (32, 40, 15),
]

def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    x0, x1 = MARGIN, W - MARGIN
    y = MARGIN

    # Masthead
    f_kicker = font(SANS_B, 20)
    d.text((x0, y), "THE DAY'S WORLD NEWS IN ONE PICTURE", font=f_kicker, fill=ACCENT)
    f_count = font(SANS_B, 20)
    cnt = "33 stories · 6 continents · all from Friday"
    d.text((x1 - d.textlength(cnt, font=f_count), y), cnt, font=f_count, fill=INK)
    y += 28
    f_mast = font(SERIF_B, 58)
    mast = "Friday 13 November 2026"
    d.text(((W - d.textlength(mast, font=f_mast)) / 2, y), mast, font=f_mast, fill=INK)
    y += 70
    # Continent legend
    f_leg = font(SANS_B, 15)
    lx = x0
    for name, col in CONT.items():
        dot(d, lx + 7, y + 8, 6, col)
        d.text((lx + 17, y), name, font=f_leg, fill=INK)
        lx += 17 + int(d.textlength(name, font=f_leg)) + 18
    y += 30
    d.line([(x0, y), (x1, y)], fill=RULE, width=3)
    y += 12

    # Top 3 stories (three columns)
    col_w = (x1 - x0 - 2 * 18) // 3
    f_num = font(SERIF_B, 26)
    f_cat = font(SANS_B, 14)
    f_head = font(SANS_B, 21)
    f_sub = font(SANS, 15)
    top_y = y
    for i, (n, cont, cat, head, sub) in enumerate(TOP3):
        cx = x0 + i * (col_w + 18)
        col = CONT[cont]
        d.rectangle([cx, top_y, cx + col_w, top_y + 6], fill=col)
        d.text((cx, top_y + 10), str(n), font=f_num, fill=ACCENT)
        d.text((cx + 34, top_y + 16), cat, font=f_cat, fill=col)
        hy = top_y + 46
        for line in wrap(d, head, f_head, col_w)[:3]:
            d.text((cx, hy), line, font=f_head, fill=INK)
            hy += 24
        sy = hy + 4
        for line in wrap(d, sub, f_sub, col_w)[:2]:
            d.text((cx, sy), line, font=f_sub, fill=MUTED)
            sy += 19
    y = top_y + 176
    d.line([(x0, y), (x1, y)], fill=RULE, width=2)
    y += 10

    # Main grid: 12 stories, 3 columns x 4 rows
    f_ghead = font(SANS_B, 17)
    f_gsub = font(SANS, 13)
    row_h = 92
    for i, (n, cont, cat, head, sub) in enumerate(GRID):
        col = i % 3
        row = i // 3
        cx = x0 + col * (col_w + 18)
        cy = y + row * row_h
        colr = CONT[cont]
        # Number gets a fixed-width slot so two-digit numbers never overlap the category.
        num_w = 44 if n >= 10 else 34
        d.text((cx, cy), str(n), font=f_num, fill=ACCENT)
        d.text((cx + num_w, cy + 6), cat, font=f_cat, fill=colr)
        hy = cy + 30
        for line in wrap(d, head, f_ghead, col_w)[:2]:
            d.text((cx, hy), line, font=f_ghead, fill=INK)
            hy += 20
        for line in wrap(d, sub, f_gsub, col_w)[:1]:
            d.text((cx, hy), line, font=f_gsub, fill=MUTED)
    y += 4 * row_h + 2
    d.line([(x0, y), (x1, y)], fill=RULE, width=2)
    y += 10

    # ALSO ON FRIDAY briefs (three columns)
    f_brief_h = font(SANS_B, 18)
    d.text((x0, y), "ALSO ON FRIDAY", font=f_brief_h, fill=INK)
    y += 26
    f_b = font(SANS, 14)
    bcol_w = (x1 - x0 - 2 * 20) // 3
    for i, (n, text) in enumerate(BRIEFS):
        col = i % 3
        row = i // 3
        bx = x0 + col * (bcol_w + 20)
        by = y + row * 20
        d.text((bx, by), f"{n}  {text}", font=f_b, fill=INK)
    y += 6 * 20 + 8
    d.line([(x0, y), (x1, y)], fill=RULE, width=2)
    y += 8

    # World map strip
    f_map_h = font(SANS_B, 16)
    d.text((x0, y), "WHERE IT HAPPENED", font=f_map_h, fill=INK)
    map_top = y + 22
    map_h = H - MARGIN - map_top - 4
    map_w = x1 - x0
    # Project lon/lat to the map strip.
    def proj(lon, lat):
        px = x0 + (lon + 180.0) / 360.0 * map_w
        py = map_top + (90.0 - lat) / 150.0 * map_h
        return (px, py)
    for poly in LAND:
        pts = [proj(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=(214, 205, 188), outline=(150, 140, 120))
    f_dot = font(SANS_B, 12)
    for lon, lat, n in MAP_DOTS:
        px, py = proj(lon, lat)
        dot(d, px, py, 9, ACCENT)
        d.text((px - 3, py - 6), str(n), font=f_dot, fill=(255, 255, 255))

    img.save("entry.png", "JPEG", quality=92)

if __name__ == "__main__":
    main()
