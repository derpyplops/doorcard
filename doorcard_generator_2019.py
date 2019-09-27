from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
import os
import math
import glob
import ntpath

def get_name(path):
    head, tail = ntpath.split(path)
    return (tail or ntpath.basename(head))

def generate_doorcard(src, bg_path, font_path):

    bg = Image.new(mode = "RGB", size = (2290, 1440), color = (179, 32, 32))

    fontsize = 160  # starting font size
    path, file_ext = os.path.splitext(src)
    name = get_name(path).upper()
    img = Image.open(src).convert("RGBA")   
    font = ImageFont.truetype(font_path, fontsize)
    text_l, text_h = (font.getsize(name))
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
    font = ImageFont.truetype(font_path, font_size)
    while font.getsize(name)[0] < TEXT_LENGTH:
        # iterate until the text size is just larger than the criteria
        font_size += 10
        font = ImageFont.truetype(font_path, font_size)

    d = ImageDraw.Draw(bg)
    text_w = math.floor(1145 + 1145/2 - font.getsize(name)[0] / 2)
    d.text((text_w, 250 - math.floor(font.getsize(name)[1] / 2)), name, (255,255,255), font=font)

    # draw outlines

    d.rectangle([(0,0), (2290, 50)], (0,0,0), (0,0,0), 0)
    d.rectangle([(0,1440-50), (2290, 1440)], (0,0,0), (0,0,0), 0)
    d.rectangle([(0,0), (50, 1440)], (0,0,0), (0,0,0), 0)
    d.rectangle([(2290-50,0), (2290, 1440)], (0,0,0), (0,0,0), 0)
    d.rectangle([(2290/2-25,0), (2290/2+25, 1440)], (0,0,0), (0,0,0), 0)

    # paste logo
    
    emblem = Image.open(curr_path + "/emblem.png").convert("RGBA")
    emblem_w = 275
    emblem = emblem.resize((emblem_w,emblem_w), Image.ANTIALIAS)
    bg.paste(emblem, (math.floor(2290/4*3-emblem_w/2), 1000), emblem)
    

    # save
    os.chdir("../output")
    bg.save(name + ".png", "PNG")
    os.chdir("../input")

curr_path = os.getcwd()
print(curr_path)
os.chdir("input")
src_array = os.listdir()

bg_path = curr_path + "/bg2.png"
print(bg_path)
font_path = curr_path + "/JosefinSans-SemiBold.ttf"

# src_array = [src_array[-1]] #! DELETE LATER

for f in src_array:
    generate_doorcard(f, bg_path, font_path)

# generate_doorcard("C:\\Users\\derpy\\Pictures\\doorcard_pics\\Wen Cong.jpg")

print("Done!")