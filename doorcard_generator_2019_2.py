from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
import os
import math
import glob
import ntpath
from openpyxl import load_workbook
import pprint

# print(person_lists)


def get_name(path):
    head, tail = ntpath.split(path)
    return (tail or ntpath.basename(head))

def generate_doorcard(src, name, major, song_text, rotate_dir):

    bg = Image.new(mode = "RGB", size = (2290, 1440), color = (179, 32, 32))
    font_path = curr_path + "/JosefinSans-SemiBold.ttf"

    fontsize = 160  # starting font size
    path, file_ext = os.path.splitext(src)
    name = name.upper()
    print(name)
    img = Image.open(src).convert("RGBA")   
    name_font = ImageFont.truetype(font_path, fontsize)
    text_l, text_h = (name_font.getsize(name))
    bg_w, bg_h = bg.size

    def cropz(img, w, h):
        img_w, img_h = img.size
        if img_w > img_h:
            img = img.rotate(90)
        if rotate_dir:
            img = img.rotate(180)
        
        scaled_width = w
        scaled_height = math.floor(w / img_w * img_h) # stretch img to given width
        # print(w, img_w, img_h)
        # print("old Image size: " + str(img_w) + " " + str(img_h))
        # print("new Image size: " + str(scaled_width) + " " + str(scaled_height))
        
        img = img.resize((scaled_width, scaled_height), Image.ANTIALIAS)
        x = img_w//2 - w//2
        y = img_h//2 - h//2
        mod_img = img.crop((x, y, x + w, y + h))
        return img

    # create / load background ok


    # crop & paste photo
    img_w, img_h = img.size
    if img_w > img_h:
        img = img.rotate(90, expand=True)
    cropped_img = cropz(img, bg_w // 2, bg_h)
    bg.paste(cropped_img, (0, 0), cropped_img)

    # paste text

    TEXT_LENGTH = 900
    font_size = 50
    name_font = ImageFont.truetype(font_path, font_size)
    if len(name) < 4:
        name_font = ImageFont.truetype(font_path, 400)
    else:    
        while name_font.getsize(name)[0] < TEXT_LENGTH:
            # iterate until the text size is just larger than the criteria
            font_size += 10
            name_font = ImageFont.truetype(font_path, font_size)

    d = ImageDraw.Draw(bg)

    centre = 1145 + 1145/2
    text_w = math.floor(centre - name_font.getsize(name)[0] / 2)
    text_h = 250 - math.floor(name_font.getsize(name)[1] / 2)
    major_h = 0
    if len(name) < 4:
        text_h += 75
        major_h += 0
    
    # from centre of above, minus half of length of major name
    
    

    # draw outlines

    d.rectangle([(0,0), (2290, 50)], (0,0,0), (0,0,0), 0)
    d.rectangle([(0,1440-50), (2290, 1440)], (0,0,0), (0,0,0), 0)
    d.rectangle([(0,0), (50, 1440)], (0,0,0), (0,0,0), 0)
    d.rectangle([(2290-50,0), (2290, 1440)], (0,0,0), (0,0,0), 0)
    d.rectangle([(2290/2-25,0), (2290/2+25, 1440)], (0,0,0), (0,0,0), 0)

    # paste logo
    
    emblem = Image.open(curr_path + "/emblem.png").convert("RGBA")
    emblem_w = 225
    emblem = emblem.resize((emblem_w,emblem_w), Image.ANTIALIAS)
    bg.paste(emblem, (math.floor(2290/4*3-emblem_w/2), 1100), emblem)

    SONG_HDR = "A song that describes me:"
    SONG_HDR_FONT = ImageFont.truetype(font_path, 50)
    SONG_HDR_X = centre - math.floor(SONG_HDR_FONT.getsize(SONG_HDR)[0] / 2)
    SONG_HDR_Y = 600

    WHITE = (255,255,255)

    

    box_coords_x = centre - 400
    box_coords_y = 700
    box_width = 800
    box_height = 300
    box_margin = 100
    box_text_length = box_width - box_margin * 2

    def wrap_text(text, width):
        lines = []  
        line_text = ""
        fontsize = 60
        font = ImageFont.truetype(font_path, fontsize)
        for word in text.split(" "):
            # print(line_text)
            # print(font.getsize(line_text + " " + word)[0], " ", width)
            if font.getsize(line_text + " " + word)[0] > width: #correct later
                line_text += '\n'
                lines.append(line_text)
                line_text = word
                
            else:
                line_text += " " + word
        lines.append(line_text)
        return (''.join(lines))[1:]
    

    # 1 insert newlines when length of text exceeds text_len
    # 2 displace by margin length

    if song_text:

        d.text((text_w, text_h), name, (255,255,255), font=name_font)

        major_font = ImageFont.truetype(font_path, 60)
        major_w = math.floor(centre - major_font.getsize(major)[0] / 2)
        major_h += text_h + name_font.getsize(name)[1] + 50
        d.text((major_w, major_h), major, (255,255,255), font=major_font)

        song_font = ImageFont.truetype(font_path, 60)
        song_x = centre - math.floor(song_font.getsize(song_text)[0] / 2)
        song_y = 750

        d.text((SONG_HDR_X, SONG_HDR_Y), SONG_HDR, WHITE, font=SONG_HDR_FONT)
        d.rectangle([(box_coords_x, box_coords_y), (box_coords_x + box_width, box_coords_y + box_height)], WHITE, WHITE, 0)
        d.text((box_coords_x + box_margin, box_coords_y + 50), wrap_text(song_text, box_text_length), (179, 32, 32), font=song_font)

    else:

        displ = 350

        d.text((text_w, text_h + displ), name, (255,255,255), font=name_font)

        major_font = ImageFont.truetype(font_path, 60)
        major_w = math.floor(centre - major_font.getsize(major)[0] / 2)
        major_h += text_h + name_font.getsize(name)[1] + displ + 40
        d.text((major_w, major_h), major, (255,255,255), font=major_font)
    

    # save
    os.chdir("../output")
    bg.save(name + ".png", "PNG")
    os.chdir("../input")

curr_path = os.getcwd()
print(curr_path)
os.chdir("input")
src_array = os.listdir()
print(src_array)
ids = []
for src in src_array:
    path, file_ext = os.path.splitext(src)
    ids.append(path.split('\\')[0].upper())

os.chdir("..")

wb = load_workbook(filename = 'firebirds1920s1.xlsx')
sheet = wb['Sheet1']
cols = ['G', 'H', 'I', 'L']
person_lists = []
for r in ids:
    person = [r + ".jpg"]
    for c in cols:
        person.append(sheet[c + str(int(r) + 1)].value)
    person_lists.append(person)

pprint.pprint(person_lists)


bg_path = curr_path + "/bg2.png"

# def generate_doorcard(src, name, major, song_text):
os.chdir("input")
for person in person_lists:
    generate_doorcard(*person)


print("Done!")
