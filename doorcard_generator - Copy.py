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
    fontsize = 160  # starting font size
    path, file_ext = os.path.splitext(src)
    name = get_name(path)
    bg = Image.open(bg_path).convert("RGBA")
    img = Image.open(src).convert("RGBA")   
    font = ImageFont.truetype(font_path, fontsize)
    text_l, text_h = (font.getsize(name))
    bg_l, bg_h = bg.size

    diameter = 900
    radius = diameter / 2
    top_margin = 100
    bottom_margin = math.floor((bg_h + diameter + top_margin) / 2) - text_h / 2
    
    img = img.resize((diameter, diameter), Image.ANTIALIAS) # squashes pic to size
    # circle crop after this
    width, height = img.size
    centre_x = width // 2
    centre_y = height // 2
    for i in range(width):
        for j in range(height):
            #gets dist from centre by taking centre coords and curr coords
            dist = math.sqrt((i - centre_x) ** 2 + (centre_y - j) ** 2)
            if dist > radius:
                img.putpixel((i, j), (255, 255, 255, 0))  #turns the color black or white (crop
    # end of circle crop
    
    bg.paste(img, (math.floor(bg_l / 2 - diameter / 2), top_margin), img)
    draw = ImageDraw.Draw(bg)

    '''
    while font.getsize(name)[0] < 300:
        # iterate until the text size is just larger than the criteria
        fontsize += 1
        font = ImageFont.truetype("C:\\Users\\derpy\\Downloads\\greataris_destain-alternative\destain.ttf", fontsize)
    '''
    draw.text((bg_l / 2 - text_l / 2 + 15, bottom_margin), name, (0,0,0), font=font)
    bg.save(name + ".png", "PNG")

curr_path = os.getcwd()
print(curr_path)
os.chdir("input")
src_array = os.listdir()
print(src_array)
bg_path = curr_path + "/bg2.png"
print(bg_path)
font_path = curr_path + "/destain.ttf"
for f in src_array:
    generate_doorcard(f, bg_path, font_path)

# generate_doorcard("C:\\Users\\derpy\\Pictures\\doorcard_pics\\Wen Cong.jpg")

print("Done!")