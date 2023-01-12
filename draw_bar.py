import argparse
import os
import random
import tensorflow as tf
from tqdm import tqdm

from bar_generator import generate_data, write_source_data, write_circle_target_data
from utils import postprocessing, maskgen


os.makedirs("./data/source", exist_ok=True)
os.makedirs("./data/tactile", exist_ok=True)

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--target', type=str, choices=['rgb', 'channelwise'], default='rgb', help='type of target domain')
    parser.add_argument("--cnt_bar", type=int, default=20, help="number of bezier curves")
    parser.add_argument("--p_figsize", nargs=3, type=float, default=[0.5, .25, .25], help="figure size probabilities")
    parser.add_argument("--p_grid", type=float, default=0.4, help="probability of drawing grid")
    parser.add_argument("--p_legend", type=float, default=0.25, help="probability of drawing legends")
    parser.add_argument("--p_grayscale", type=float, default=0, help="probability of grayscale source domain")
    parser.add_argument("--p_rotate", type=float, default=0.5, help="probability of rotating a bar chart")
    opt = parser.parse_args()

    with tf.device('/device:GPU:0'):
        data, metadata, circle_data = generate_data(num_samples=opt.cnt_bar)

        for i in tqdm(range(len(data)), desc='bar charts: '):

            fig_size = random.choices([[512,512], [1024,512], [512,1024]], weights=opt.p_figsize)[0]
            draw_grid = random.random() < opt.p_grid
            gray_scale = random.random() < opt.p_grayscale
            orientation = 'h' if random.random() < opt.p_rotate else 'v'
            tick_step = random.randint(10, 16)

            write_source_data(data[i], f"./data/source/s_{i+1}.png", fig_size, draw_grid, tick_step, orientation, p_legend=opt.p_legend)
            postprocessing(f"./data/source/s_{i+1}.png", gray=gray_scale)
            
            write_circle_target_data(circle_data[i], f"./data/tactile/t_{i+1}.png", fig_size, draw_grid, tick_step, opt.target, orientation)
            if opt.target == 'rgb':
                postprocessing(f"./data/tactile/t_{i+1}.png", format='tiff')
            else:
                maskgen(f"./data/tactile/t_{i+1}.png")
        