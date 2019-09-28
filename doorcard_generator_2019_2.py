from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
import os
import math
import glob
import ntpath
from openpyxl import load_workbook

wb = load_workbook(filename = 'firebirds1920s1.xlsx')
sheet = wb['Sheet1']
rows = range(2, 83)
cols = ['G', 'H', 'I']
person_lists = []
for r in rows:
    person = []
    for c in cols:
        person.append(sheet[c + str(r)].value)
    person_lists.append(person)

print(person_lists)


def get_name(path):
    head, tail = ntpath.split(path)
    return (tail or ntpath.basename(head))

def generate_doorcard(src, name, major, song_text):

    bg = Image.new(mode = "RGB", size = (2290, 1440), color = (179, 32, 32))
    font_path = curr_path + "/JosefinSans-SemiBold.ttf"

    fontsize = 160  # starting font size
    path, file_ext = os.path.splitext(src)
    name = name.upper()
    img = Image.open(src).convert("RGBA")   
    name_font = ImageFont.truetype(font_path, fontsize)
    text_l, text_h = (name_font.getsize(name))
    bg_w, bg_h = bg.size

    def cropz(img, w, h):
        img_w, img_h = img.size
        scaled_width = w
        scaled_height = math.floor(w / img_w * img_h) # stretch img to given width
        print(w, img_w, img_h)
        print("old Image size: " + str(img_w) + " " + str(img_h))
        print("new Image size: " + str(scaled_width) + " " + str(scaled_height))
        
        img = img.resize((scaled_width, scaled_height), Image.ANTIALIAS)
        x = img_w//2 - w//2
        y = img_h//2 - h//2
        mod_img = img.crop((x, y, x + w, y + h))
        return img

    # create / load background ok


    # crop & paste photo
    cropped_img = cropz(img, bg_w // 2, bg_h)
    bg.paste(cropped_img, (0, 0), cropped_img)

    # paste text

    TEXT_LENGTH = 900
    font_size = 50
    name_font = ImageFont.truetype(font_path, font_size)
    while name_font.getsize(name)[0] < TEXT_LENGTH:
        # iterate until the text size is just larger than the criteria
        font_size += 10
        name_font = ImageFont.truetype(font_path, font_size)

    d = ImageDraw.Draw(bg)

    centre = 1145 + 1145/2
    text_w = math.floor(centre - name_font.getsize(name)[0] / 2)
    text_h = 250 - math.floor(name_font.getsize(name)[1] / 2)
    
    # from centre of above, minus half of length of major name
    
    d.text((text_w, text_h), name, (255,255,255), font=name_font)

    major_font = ImageFont.truetype(font_path, 60)
    major_w = math.floor(centre - major_font.getsize(major)[0] / 2)
    major_h = text_h + name_font.getsize(name)[1] + 50
    d.text((major_w, major_h), major, (255,255,255), font=major_font)

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

    song_font = ImageFont.truetype(font_path, 60)
    song_x = centre - math.floor(song_font.getsize(song_text)[0] / 2)
    song_y = 750

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
            print(line_text)
            print(font.getsize(line_text + word)[0], " ", width)
            if font.getsize(line_text + word)[0] > width: #correct later
                line_text += '\n'
                lines.append(line_text)
                line_text = word
                
            else:
                line_text += word
        lines.append(line_text)
        return ''.join(lines)
    

    # 1 insert newlines when length of text exceeds text_len
    # 2 displace by margin length

    d.text((SONG_HDR_X, SONG_HDR_Y), SONG_HDR, WHITE, font=SONG_HDR_FONT)
    d.rectangle([(box_coords_x, box_coords_y), (box_coords_x + box_width, box_coords_y + box_height)], WHITE, WHITE, 0)
    d.text((box_coords_x + box_margin, box_coords_y + 50), wrap_text(song_text, box_text_length), (179, 32, 32), font=song_font)
    

    # save
    os.chdir("../output")
    bg.save(name + ".png", "PNG")
    os.chdir("../input")

curr_path = os.getcwd()
print(curr_path)
os.chdir("input")
src_array = os.listdir()

bg_path = curr_path + "/bg2.png"

# src_array = [src_array[-1]] #! DELETE LATER

# get list of [src, name, song_text]
# person_lists = [[src_array[0], "Derpy", "Projects and Facilities Management", "hurts 2b human - P!nk & Khalid"]]

# def generate_doorcard(src, name, major, song_text):
# for person in person_lists:
#     generate_doorcard(*person)

# generate_doorcard("C:\\Users\\derpy\\Pictures\\doorcard_pics\\Wen Cong.jpg")

print("Done!")