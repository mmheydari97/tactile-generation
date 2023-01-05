import os
import numpy as np
import matplotlib.pyplot as plt

cross = []
def on_press(event):
    
    if str(event.button) == "MouseButton.LEFT":
        cross.append([event.xdata, event.ydata])
    

file_count = len(next(os.walk("./points"))[2])

for i in range(file_count):

    cross = []
    b = np.load(f"points/{i+1}.npy")

    fig = plt.figure()
    plt.plot(b[:,0], b[:,1])
    fig.canvas.mpl_connect('button_press_event', on_press)
    plt.show()

    np.save(f"./intersections/{i+1}.npy", np.array(cross))
    print(f"intersections {i+1} created.")
    if i%10 == 0:
        plt.close('all')
