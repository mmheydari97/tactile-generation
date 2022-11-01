import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
from PIL import Image, ImageFilter
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


def _mplfig_to_npimage(fig):
    canvas = FigureCanvasAgg(fig)
    canvas.draw()

    l,b,w,h = canvas.figure.bbox.bounds
    w, h = int(w), int(h)

    buf = canvas.tostring_rgb()
    image= np.frombuffer(buf, dtype=np.uint8)
    return image.reshape(h,w,3)


def figure2mask(fig, shape=(256, 256), thresh=240):
    data = _mplfig_to_npimage(fig)
    im = Image.fromarray(data).convert("L")
    im = im.point( lambda p: 0 if p < thresh else 255)
    im = invert(expand2square(im)).resize(shape, resample=Image.LANCZOS).convert("1")
    return np.uint8(im)


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
    

def postprocessing(fname, shape=(256, 256)):
    img = Image.open(fname)
    img = expand2square(img).resize(shape, resample=Image.LANCZOS)
    img.save(fname)
