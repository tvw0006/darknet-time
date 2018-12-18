from PIL import Image
from PIL import ImageDraw
from PIL import ImageEnhance
import glob
import pathlib
from pathlib import Path
import random
import os.path
from random import randrange

def from_yolo_to_cor(box, img):
    img_h, img_w = img.size[1], img.size[0]
    # x1, y1 = ((x + witdth)/2)*img_width, ((y + height)/2)*img_height
    # x2, y2 = ((x - witdth)/2)*img_width, ((y - height)/2)*img_height
    x1 = int((box[0] + box[2] / 2)*img_w)
    y1 = int((box[1] + box[3] / 2)*img_h)
    x2 = int((box[0] - box[2] / 2)*img_w)
    y2 = int((box[1] - box[3] / 2)*img_h)
    return x1, y1, x2, y2
    
def draw_boxes(img, x1, y1, x2, y2, pic_save_path):
    box = [x1, y1, x2, y2]
    x1, y1, x2, y2 = from_yolo_to_cor(box, img)
    draw = ImageDraw.Draw(img)
    draw.rectangle(((x1, y1), (x2, y2)), fill=None, outline="green")
    img = img.convert("RGB")
    img.save(pic_save_path, "JPEG")

for n in range(0,500):
    pic_open = 'pos-' + str(n) + '.jpg'
    txt_open = 'pos-' + str(n) + '.txt'
    pic_save_new = 'test-' + str(n) + '.jpg'
    pic_path = Path('C:/Users/WilliT11/Documents/Dataset/dataset/output') / pic_open
    text_path = Path('C:/Users/WilliT11/Documents/Dataset/dataset/output') / txt_open
    pic_save_path = Path('C:/Users/WilliT11/Documents/Dataset/dataset/output') / pic_save_new
    background_im_orig = Image.open(pic_path)
    background_im_orig = background_im_orig.convert("RGBA")
    file = open(text_path, 'r')
    for line in file:
        split = line.split(" ")
    x1 = float(split[1])
    x2 = float(split[2])
    y1 = float(split[3])
    y2 = float(split[4])
    draw_boxes(background_im_orig, x1, x2, y1, y2, pic_save_path)
    
    
