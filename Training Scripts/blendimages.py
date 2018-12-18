from PIL import Image
from PIL import ImageDraw
from PIL import ImageEnhance
import pathlib
from pathlib import Path
import random
import os.path
from random import randrange

# Module to generate text and images for Darknet. All paths must be edited before running code. 
# Restarts loop for limited images
def revertnum(count, max):
    count = count + 1
    if(count > max):
        return 0
    else:
        return count


# Function to change the image size
def changeImageSize(maxWidth, 
                    maxHeight, 
                    image):
    
    widthRatio  = maxWidth/image.size[0]
    heightRatio = maxHeight/image.size[1]

    newWidth    = int(widthRatio*image.size[0])
    newHeight   = int(heightRatio*image.size[1])

    newImage    = image.resize((newWidth, newHeight))
    return newImage

# gets image from path
def built_path_number(r):
    if(r < 10):
        path = '0000000' + str(r) + '.jpg'
    elif(r < 100):
        path = '000000' + str(r) + '.jpg'
    elif(r < 1000):
        path = '00000' + str(r) + '.jpg'
    else:
        path = '0000' + str(r) + '.jpg'
    return path
    # paste the rotated image onto the background image



back_count = 0 # counter for background images
time_count = 0 # counter for time images
save_count = 1 # counter for save images
num_foreground = 549 # number of foreground images
num_background = 937 # number of background images
num_pictures = 2000 # desired number of output images

# prepares an image for detection
def process_image(back_path, for_path):

# define coefficients for random shift

    persp = randrange(-7,7)/-10 # coeffecients for random perspective shift
    rotation1 = randrange(0,359) # rotate the time image between 0 and 359 degrees
    rotorpers = randrange(0,2) # either perform a perspective shift or a rotation
    if(rotorpers == 1):
        rotation1 = 0
    else:
        persp = 0
    flip = randrange(0,1) # used for flipping images. Change range from (0,2) to apply flipping. In this case, no horizontal flip is applied
    brightness = randrange(35,100)/100 # change image brightness
    rand_perc = randrange(15,45)/100 $ resize foreground images relative to background image

    background_im_orig = Image.open(background_path) # open background image
    fore_im_orig = Image.open(foreground_path) # open foreground image
    fore_im_rgba = fore_im_orig.convert("RGBA")

# resize the background image to scale with time magazine image
    if(background_im_orig.size[0] > fore_im_orig.size[0]):
        background_im_orig = changeImageSize(fore_im_orig.size[0], int(background_im_orig.size[1]/background_im_orig.size[0]*fore_im_orig.size[0]), background_im_orig)

# flip images
    if(flip == 1):
        fore_im_rgba = fore_im_rgba.transpose(Image.FLIP_LEFT_RIGHT)
# apply perspective shift
    xshift = abs(persp) * fore_im_rgba.size[0]*1.33
    new_width = fore_im_rgba.size[0]+ int(round(xshift))
    perspective_img = fore_im_rgba.transform((new_width, fore_im_rgba.size[1]), Image.AFFINE, (1, persp, -xshift if persp > 0 else 0, 0, 1, 0), Image.BICUBIC)
# apply rotation and resize
    fore_im_rot = perspective_img.rotate(rotation1, expand = 1)
    resize_width = rand_perc*background_im_orig.size[0] # shifts magazine size.
    resize_height = fore_im_rot.size[1]/fore_im_rot.size[0]*resize_width # get ratio of width/height for time image
    if(resize_height > background_im_orig.size[1] or resize_width > background_im_orig.size[0]):
        #print("error 1")
        resize_height = resize_height/2
        resize_width = resize_width/2   
    fore_im_resiz = changeImageSize(int(resize_width), int(resize_height), fore_im_rot)
    top_left_w, top_left_h = 0,0 
    bot_right_w, bot_right_h = fore_im_resiz.size[0],fore_im_resiz.size[1]
    if(background_im_orig.size[0]-fore_im_resiz.size[0] <= 0 or background_im_orig.size[1]-fore_im_resiz.size[1] <= 0):
        return 0, 0, 0, 0, 0

# randomly shift foreground image location
    shift1 = randrange(0, background_im_orig.size[0]-fore_im_resiz.size[0])
    shift2 = randrange(0, background_im_orig.size[1]-fore_im_resiz.size[1])
    top_left_w = top_left_w + shift1
    bot_right_w = bot_right_w + shift1
    top_left_h =  top_left_h + shift2
    bot_right_h = bot_right_h + shift2
# paste foreground image onto background image
    background_im_orig.paste(fore_im_resiz, (shift1,shift2), fore_im_resiz)
# get coefficients for Darknet
    cent_x = (float(bot_right_w)+float(top_left_w))/2
    cent_y = (float(bot_right_h)+float(top_left_h))/2
    width = float(bot_right_w)-float(top_left_w)
    height = float(bot_right_h)-float(top_left_h)
    dw = 1./background_im_orig.size[0]
    dh = 1./background_im_orig.size[1]
    cent_x = dw * cent_x
    cent_y = dh * cent_y
    width = dw * width
    height = dh * height
    background_im_orig = background_im_orig.point(lambda p: p*brightness)
    #draw = ImageDraw.Draw(background_im_orig)
    #draw.rectangle(((top_left_w, top_left_h), (bot_right_w, bot_right_h)), fill=None, outline="blue")
    background_im_orig = background_im_orig.convert("RGB")
    return background_im_orig, cent_x, cent_y, width, height





# loop through images
for x in range(0, num_pictures):
    # build paths. Edit path to match desired path. 
    background_path = Path('C:/Users/WilliT11/Documents/Dataset/dataset/Background') / built_path_number(back_count)
    foreground_path = Path('C:/Users/WilliT11/Documents/Dataset/dataset/Time') / built_path_number(time_count)
    # create save paths for time magazine images
    pic_save = 'pos-' + str(x) + '.jpg'
    pic_save_path = Path('C:/Users/WilliT11/Documents/Dataset/dataset/output') / pic_save
    txt_save = 'pos-' + str(x) + '.txt'
    txt_save_path = Path('C:/Users/WilliT11/Documents/Dataset/dataset/output') / txt_save
    # create save path for background images
    pic_save2 = 'pos-' + str(x+num_pictures+1) + '.jpg'
    pic_save_path2 = Path('C:/Users/WilliT11/Documents/Dataset/dataset/output') / pic_save2
    txt_save2 = 'pos-' + str(x+num_pictures+1) + '.txt'
    txt_save_path2 = Path('C:/Users/WilliT11/Documents/Dataset/dataset/output') / txt_save2
    while(not background_path.exists()):
        back_count = revertnum(back_count, num_background)
        background_path = Path('C:/Users/WilliT11/Documents/Dataset/dataset/Background') / built_path_number(back_count)
    while(not foreground_path.exists()):
        time_count = revertnum(time_count, num_foreground)
        foreground_path = Path('C:/Users/WilliT11/Documents/Dataset/dataset/Time') / built_path_number(time_count)
    outpicture, outx, outy, outw, outh = process_image(background_path, foreground_path)
    while(outpicture == 0):
        back_count = revertnum(back_count, num_background)
        time_count = revertnum(time_count, num_foreground)
        while(not background_path.exists()):
            back_count = revertnum(back_count, num_background)
            background_path = Path('C:/Users/WilliT11/Documents/Dataset/dataset/Background') / built_path_number(back_count)
        while(not foreground_path.exists()):
            time_count = revertnum(time_count, num_foreground)
            foreground_path = Path('C:/Users/WilliT11/Documents/Dataset/dataset/Time') / built_path_number(time_count)
        outpicture, outx, outy, outw, outh = process_image(background_path, foreground_path)
# save pictures and text files
    outpicture.save(pic_save_path, "JPEG")
    txt_string = '0 ' + str(outx) + ' ' + str(outy) + ' ' + str(outw) + ' ' + str(outh)
    f= open(txt_save_path,"w+")
    f.write(txt_string)
    f.close()
    background_im_only = Image.open(background_path) # open background image without time magazine
    background_im_only = background_im_only.convert("RGB")
    background_im_only.save(pic_save_path2, "JPEG")
    f2= open(txt_save_path2,"w+")
    f2.close()
    back_count = revertnum(back_count, num_background)
    time_count = revertnum(time_count, num_foreground)


outpicture.show()
