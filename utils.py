import random
import string
import os
import matplotlib.pyplot as plt
from PIL import Image
from PIL.ImageOps import invert, autocontrast


def expand2square(pil_img):
        width, height = pil_img.size
        if width == height:
            return pil_img
        elif width > height:
            result = Image.new(pil_img.mode, (width, width), list(pil_img.getdata())[1])
            result.paste(pil_img, (0, (width - height) // 2))
            return result
        else:
            result = Image.new(pil_img.mode, (height, height), list(pil_img.getdata())[1])
            result.paste(pil_img, ((height - width) // 2, 0))
            return result


def draw_grids(ax, **kwargs):
    ax.set_zorder(0)
    plt.grid(which='both', axis='both', **kwargs)


def get_rgb_color(alpha=0.1):
    
    def extract_rgb(color_string):
        r = int(f'0x{color_string[1:3]}',16)
        g = int(f'0x{color_string[3:5]}',16)
        b = int(f'0x{color_string[5:7]}',16)
        return (r,g,b)


    a = hex(int(alpha*255))
    base = "#ffffff"
    r,g,b = extract_rgb(base)
    while r+g+b>600:
        base = "#"+''.join([random.choice('0123456789abcdef') for _ in range(6)])
        r,g,b = extract_rgb(base)

    return "#"+''.join([random.choice('0123456789abcdef') for _ in range(6)])+a[2:]


def get_figsize(weights):
    return random.choices([[5,5], [2.5,5], [5,2.5]], weights=weights)[0]


def get_random_string(max_length, min_length=1):
    length = random.randint(min_length, max_length)
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def maskgen(fname, shape=(256, 256)):
    fname_parts = fname.rsplit('.', 1)
    msk_axes = Image.open(f"{fname_parts[0]}_axes.{fname_parts[1]}").convert('L')
    msk_grids = Image.open(f"{fname_parts[0]}_grids.{fname_parts[1]}").convert('L')
    msk_content = Image.open(f"{fname_parts[0]}_content.{fname_parts[1]}").convert('L')
    
    msk_axes = autocontrast(expand2square(invert(msk_axes)).resize(shape, resample=Image.LANCZOS))
    msk_grids = autocontrast(expand2square(invert(msk_grids)).resize(shape, resample=Image.LANCZOS))
    msk_content = autocontrast(expand2square(invert(msk_content)).resize(shape, resample=Image.LANCZOS))
    
    os.remove(f"{fname_parts[0]}_axes.{fname_parts[1]}")
    os.remove(f"{fname_parts[0]}_grids.{fname_parts[1]}")
    os.remove(f"{fname_parts[0]}_content.{fname_parts[1]}")
    
    msk_axes.save(f"{fname_parts[0]}_axes.tiff")
    msk_grids.save(f"{fname_parts[0]}_grids.tiff")
    msk_content.save(f"{fname_parts[0]}_content.tiff")
    

def postprocessing(fname, shape=(256, 256),gray=False):
    img = Image.open(fname)
    img = expand2square(img).resize(shape, resample=Image.LANCZOS)
    if gray:
        img = img.convert('L')
    img.save(fname)
