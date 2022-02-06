import json
from sys import getallocatedblocks
from PIL import Image, ImageFont, ImageDraw
import random


data = json.load(open('kanji-wanikani.json', encoding="utf8"))


def getAllKanjis():
    allkanjis = []
    for key in data:
        if data[key]["wk_level"] is None:
            continue
        allkanjis.append(key)
    return allkanjis


def getKanjis(level):
    kanjis = []
    for key in data:
        if data[key]["wk_level"] is None:
            continue

        if data[key]["wk_level"] <= level:
            kanjis.append(key)
    return kanjis


def makeImage(rows, level, shuffle=False):
    allkanjis = getAllKanjis()
    lines = len(allkanjis)//rows + 1
    kanjis = getKanjis(level)
    margin = 100
    size = 100
    charHeight = size

    if shuffle:
        random.shuffle(allkanjis)

    img = Image.new('RGB', (rows*size+2*margin,
                            lines*size+margin), color=(0, 0, 0))

    font = ImageFont.truetype('NotoSansJP-Regular.otf', size)
    d = ImageDraw.Draw(img)

    def paint():
        counter = 0
        for line in range(lines):
            for i in range(rows):
                if i+rows*line >= len(allkanjis):
                    return

                text = allkanjis[i+rows*line]
                # color the character if it has been learned in a lesson
                color = 100, 100, 100
                if any(text == s for s in kanjis):
                    color = 70 + 8*line, 50, 220 - 8*line

                d.text((i*size+margin, line*charHeight),
                       text, font=font, fill=(color))
                counter = counter + 1
                if counter % 100 == 0:
                    print("Processing... "+str(counter)+"/"+str(len(allkanjis)))

        print(counter)

    paint()
    print("Done!")

    img.save('result.jpg')


rows = input("Number of rows (default 60): ")
if rows == "":
    rows = 60
else:
    rows = int(rows)

level = input("Wanikani level? ")
if level == "":
    level = 60
else:
    level = int(level)


shuffle = input("Shuffle kanjis? ")
if shuffle.lower() == "yes" or shuffle.lower == "oui":
    shuffle = True
else:
    shuffle = False

makeImage(rows, level, shuffle)
