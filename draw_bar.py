import argparse
import os
import random
import tensorflow as tf
from tqdm import tqdm

from bar_generator import generate_data, write_source_data, write_circle_target_data
from utils import postprocessing, maskgen

P_grid = 0.4

os.makedirs("./data/source", exist_ok=True)
os.makedirs("./data/tactile", exist_ok=True)



    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--target', type=str, choices=['rgb', 'channelwise'], default='rgb', help='type of target domain')
    parser.add_argument("--cnt_bar", type=int, default=5000, help="number of bezier curves")
    parser.add_argument("--p_figsize", nargs=3, type=float, default=[.5, .25, .25], help="figure size probabilities")
    parser.add_argument("--p_grid", type=float, default=0.4, help="probability of drawing grid")
    parser.add_argument("--p_legend", type=float, default=0.2, help="probability of drawing legends")
    parser.add_argument("--p_grayscale", type=float, default=0.2, help="probability of grayscale source domain")

    opt = parser.parse_args()

    with tf.device('/device:GPU:0'):
        data, metadata, circle_data = generate_data(num_samples=opt.cnt_bar)

        for i in tqdm(range(len(data)), desc='bar charts: '):

            fig_size = random.choices([[512,512], [1024,512], [512,1024]], weights=opt.p_figsize)[0]
            draw_grid = random.random() < opt.p_grid
            gray_scale = random.random() < opt.p_grayscale
            tick_step = random.randint(10, 16)

            write_source_data(data[i], f"./data/source/s_{i+1}.png", fig_size, draw_grid, tick_step)
            postprocessing(f"./data/source/s_{i+1}.png", gray_scale)
            
            write_circle_target_data(circle_data[i], f"./data/tactile/t_{i+1}.png", fig_size, draw_grid, tick_step)
            maskgen(f"./data/tactile/t_{i+1}.png")