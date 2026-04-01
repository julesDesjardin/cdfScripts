import urllib.request
import json
from PIL import Image, ImageDraw, ImageFont, ImageOps
from io import BytesIO

import requests


def get_max_font_size(draw, text, font_path, max_width, max_height):
    font_size = 1

    while True:
        if font_size == 150:
            return font_size
        font = ImageFont.truetype(font_path, font_size)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        if text_width > max_width or text_height > max_height:
            return font_size - 1

        font_size += 1


def generateNametag(templateName, name, country, registrantId):

    # Load image
    img = Image.open(templateName).convert("RGBA")
    draw = ImageDraw.Draw(img)

    if name == 'Artūrs Jakovļevs':
        text = 'Arturs Jakovlevs'
    elif name == 'Kryštof Basl':
        text = 'Krystof Basl'
    else:
        text = name.split('(')[0]
    print(text)
    font_path = "./inglobal/inglobal.ttf"

    # Define the area the text must fit into
    area_width = 1000
    area_height = 300

    # Find best font size
    best_size = get_max_font_size(draw, text, font_path, area_width, area_height)
    font = ImageFont.truetype(font_path, best_size)

    # Measure final text
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Center text in the whole image
    img_width, _ = img.size
    x = (img_width - text_width) // 2
    y = 820 - text_height // 2

    # Draw Name
    draw.text((x, y), text, font=font, fill=(0, 0, 0, 255))

    # QRCodes
    font_path = './biolinum/LinBiolinum_R.ttf'

    text = 'Résultats'
    font = ImageFont.truetype(font_path, 80)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Center text in the whole image
    x = 500 - text_width // 2
    y = 1800 - text_height // 2

    draw.text((x, y), text, font=font, fill=(0, 0, 0, 255))

    text = 'Planning'
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Center text in the whole image
    x = 1248 - text_width // 2
    y = 1800 - text_height // 2

    draw.text((x, y), text, font=font, fill=(0, 0, 0, 255))

    insert = Image.open('qrcodeLive.png').convert('RGBA')

    img.paste(insert, (350, 1900), insert)

    if registrantId != 0:
        url = "https://api.qrserver.com/v1/create-qr-code/"
        params = {
            "size": "300x300",
            "data": f"https://www.competitiongroups.com/competitions/FrenchChampionship2026/persons/{registrantId}",
            "bgcolor": "FFF7EA"
        }

        response = requests.get(url, params=params)

        qr_img = Image.open(BytesIO(response.content)).convert("RGBA")

        img.paste(qr_img, (1098, 1900), qr_img)

    url = f"https://flagcdn.com/w320/{country.lower()}.png"

    response = requests.get(url)

    flag = Image.open(BytesIO(response.content)).convert("RGBA")
    flag.thumbnail((1000, 100))

    flag_width = flag.width
    flag_height = flag.height

    img.paste(flag, ((img_width - flag_width) // 2, 980 - flag_height // 2), flag)

    return img


with urllib.request.urlopen("https://www.worldcubeassociation.org/api/v0/competitions/FrenchChampionship2026/wcif/public") as url:
    data = json.loads(url.read().decode())

with open('compcount.json', 'r') as compFile:
    compJson = json.load(compFile)

compCount = dict([])
for item in compJson:
    compCount[item['id']] = item['count']

adherents = ['2015CLEM03', '2019TOMM01', '2022MORE12', '2016ANSE02', '2022CHAN39', '2014LAFO02', '2010DESJ01', '2014LAFO01', '2014GARC27', '2009BONN01', '2014MALI04', '2021RUTH02', '2008PIAU01', '2015LUCI02', '2010ESTU01', '2018NEVE02', '2015PHOM01', '2018HENN02', '2023BLIN01', '2022KYKE01', '2017MART50', '2025RHAR01', '2022SOUA01', '2017RIVA09', '2012YEMI01', '2018TILL02', '2010WEYE02', '2021THOM05', '2016SANC41', '2022ROMA05', '2018AUBR01', '2016VINC01', '2023GALL30', '2016PYWI01', '2015DEGL01', '2021DAMM01', '2018JEHA01', '2023GOGL01', '2021CAMB01', '2023GOGL02', '2019PLAN02', '2017MORE17', '2023MENU01', '2022RODE02', '2024BERT02', '2014SEBA01', '2024CAPE02', '2023BERN07', '2025FRON01', '2017PRES04', '2011HOFF02', '2008LAUR01', '2025ZEMM01', '2018DUTH01', '2020ROUY01', '2013GUER03', '2024BERN05', '2021BOUC01', '2008MORE02', '2024VILL45', '2024WOJT04', '2013CLAP01', '2016BAZI03', '2018SOUT02', '2021BERY01', '2025MESN01', '2016LECO01', '2023MFOU01', '2013COLI02', '2012CARL03', '2025ROMA08', '2021PRIE01', '2024DECA01', '2013CHEN22', '2025DUVE02', '2021EYRA01', '2022RINC06', '2022DAUG01', '2018MADR02', '2022DOTT02', '2018LUCM01', '2025JOUS01', '2019MERR02', '2022BONN01', '2025PERI03', '2022JEHA01', '2015REIS02', '2016POUS01', '2022ECHE01', '2024SAUG01', '2025VERN01', '2025MOUT03', '2025ETON01', '2015CRAN01', '2024THOM41', '2022TREM02', '2022PALM09',
             '2024BOUB01', '2013FERT01', '2022ESSL01', '2016BEYE01', '2024BIAG01', '2024DORO01', '2022GRAS02', '2024SCHM02', '2025PACQ03', '2025BOAS02', '2024DAMM01', '2023GOZL02', '2024RENN05', '2014BEGU01', '2024BERN10', '2024GALB01', '2024MARC11', '2025PALE02', '2010KADD01', '2024LACA01', '2025GELY01', '2023LEPR01', '2017SAFO01', '2025BRAH01', '2025ETON02', '2023DECH02', '2023FAUR01', '2025BORN02', '2022STEF09', '2025MOUL02', '2025PACQ01', '2017CRET01', '2024DECA02', '2022GUIL06', '2024GELY01', '2022VALL10', '2023CHAU13', '2025PACQ02', '2025MONG06', '2025CHAR04', '2018PROV01', '2023VELC01', '2024WALA01', '2022MONE02', '2024LECA02', '2025DAMM02', '2022CHAU04', '2025HANO02', '2022ROMA07', '2025HANO01', '2024GAUT04', '2025CAPE02', '2017MEUN01', '2025DECH02', '2013GERT01', '2024BONN02', '2025MARC05', '2024DEMA01', '2025DECH03', '2022ROYM01', '2024BOYE02', '2016BUCK01', '2016JURK01', '2022GIRA05', '2019MEUN02', '2025SAIG06', '2022MONE04', '2025SAIG04', '2015GIRA02', '2025SAIG07', '2025SAIG05', '2024PORE01', '2019POUC01', '2018DALO01', '2024LYYE01', '2022ALVA16', '2025WENG01', '2023BARB28', '2025PORE01', '2024ANTO01', '2025MEYE08', '2010VALO01', '2024ANTO11', '2016BOUR01', '2017MARF01', '2018GOME06', '2014BAUD02', '2023TRAN19', '2013FRAI01', '2022MENC01', '2022FERR16', '2019DERA02', '2024VILL06', '2025BEND02', '2016MELA02', '2023FERR27', '2025CHAR12']

orgas = ['2015CLEM03', '2019TOMM01', '2022MORE12', '2023BERN08', '2016ANSE02',
         '2022CHAN39', '2014LAFO02', '2010DESJ01', '2014MALI04', '2010ESTU01', '2015REYN07']
delegates = ['2023BERN08', '2016ANSE02', '2014LAFO02', '2010DESJ01', '2014LAFO01', '2014GARC27', '2009BONN01',
             '2021RUTH02', '2008PIAU01', '2015LUCI02', '2018NEVE02', '2016FARR02', '2014BEGU01', '2024BERN05', '2018AUBR01']

templates = []
images = []
for person in data['persons']:
    wcaid = person['wcaId']
    if wcaid is None:
        templates.append(('Compétieur_1compoumoins_pas_AFS.png', person['name'], person['countryIso2'], person['registrantId']))
        continue
    if wcaid == '2015REYN07':
        continue
    if wcaid in orgas:
        if wcaid in adherents:
            templates.append(('Orga_AFS.png', person['name'], person['countryIso2'], person['registrantId']))
        else:
            templates.append(('Orga_pas_AFS.png', person['name'], person['countryIso2'], person['registrantId']))
        continue
    if wcaid in delegates:
        if wcaid in adherents:
            templates.append(('Délégué_AFS.png', person['name'], person['countryIso2'], person['registrantId']))
        else:
            templates.append(('Délégué_pas_AFS.png', person['name'], person['countryIso2'], person['registrantId']))
        continue
    count = compCount[wcaid]
    if count == 1:
        if wcaid in adherents:
            templates.append(('Compétieur_1compoumoins_AFS.png', person['name'], person['countryIso2'], person['registrantId']))
        else:
            templates.append(('Compétieur_1compoumoins_pas_AFS.png', person['name'], person['countryIso2'], person['registrantId']))
        continue
    if count <= 10:
        if wcaid in adherents:
            templates.append(('Compétieur_2-10comps_AFS.png', person['name'], person['countryIso2'], person['registrantId']))
        else:
            templates.append(('Compétieur_2-10comps_pas_AFS.png', person['name'], person['countryIso2'], person['registrantId']))
        continue
    if wcaid in adherents:
        templates.append(('Compétieur_AFS.png', person['name'], person['countryIso2'], person['registrantId']))
    else:
        templates.append(('Compétieur_pas_AFS.png', person['name'], person['countryIso2'], person['registrantId']))
    continue

templates.sort(key=lambda x: x[1])
templates.append(('Orga_pas_AFS.png', 'Laurent Reynaud', 'FR', 0))
templates.append(('Orga_pas_AFS.png', 'Tifenn Le Roy', 'FR', 0))

for (template, name, country, registrantId) in templates:
    images.append(generateNametag(template, name, country, registrantId))


# Page size (A4 at 300 DPI ~ 2480x3508 px)
PAGE_WIDTH, PAGE_HEIGHT = 2480, 3508

# Coordinates for 2x2 grid
positions = [
    (0, 0),  # top-left
    (PAGE_WIDTH // 2, 0),  # top-right
    (0, PAGE_HEIGHT // 2),  # bottom-left
    (PAGE_WIDTH // 2, PAGE_HEIGHT // 2),  # bottom-right
]

pages = []
order = [0, 2, 1, 3]
for i in range(0, len(images), 4):
    page = Image.new("RGB", (PAGE_WIDTH, PAGE_HEIGHT), "white")
    for j in range(4):
        index = order[j]
        if i + index >= len(images):
            continue
        img = images[i + index]
        # Resize image to fit a quarter of the page
        target_width = PAGE_WIDTH // 2
        target_height = PAGE_HEIGHT // 2
        img_resized = img.resize((target_width, target_height), Image.LANCZOS)
        page.paste(img_resized, positions[j], img_resized)  # respects transparency
        print(f'{i+j} / {len(images)}')
    page = page.rotate(90, expand=True)
    pages.append(page)

# Save all pages to a single PDF
pages[0].save("output.pdf", save_all=True, append_images=pages[1:])
