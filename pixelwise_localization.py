import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from utils import expand2square


with Image.open("./source/s_7.jpg") as img:
    
    ratio = img.getbbox()[2]/img.getbbox()[3]
    img = expand2square(img).resize((256, 256))
    fig_size = [a for a in [[10,20], [20,10], [10,10]] if a[0]/a[1]==ratio][0]
    
    print(f"ratio: {ratio}")

    if ratio == 1:
        zero = (32, 228)
        x_max = (230, 228)
        y_max = (32, 30)
    
    elif ratio == 0.5:    
        zero = (79, 228)
        x_max = (179, 228)
        y_max = (79, 30)
        
    else:
        zero = (32, 179)
        x_max = (230, 179)
        y_max = (32, 79)

img.putpixel(zero, (255,0,0))
img.putpixel(x_max, (255,0,0))
img.putpixel(y_max, (255,0,0))


b = np.load("./points/7.npy")
plt.figure(figsize=fig_size)
plt.plot(b[:,0], b[:,1])

xlimits = plt.xlim()
ylimits = plt.ylim()

points = [(193, 94), (137, 118), (145, 129)]
for p in points:
    img.putpixel(p, (255,0,0))
img.show()

for p in points:
    x_int = (p[0] - zero[0])/(x_max[0]-(zero[0]-1))*(xlimits[1]-xlimits[0])+xlimits[0]
    y_int = (p[1] - zero[1])/((y_max[1]-1) - zero[1])*(ylimits[1]-ylimits[0])+ylimits[0]
    plt.scatter(x_int, y_int, s=100, edgecolors='w', lw=6, zorder=2)
plt.show()