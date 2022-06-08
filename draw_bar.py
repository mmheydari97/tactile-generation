import os
import random
import pandas as pd
import tensorflow as tf

from bar_generator import generate_data, write_source_data, write_circle_target_data, serialize_data
from utils import postprocessing, maskgen

NUM_SAMPLES = 10
P_grid = 0.4

os.makedirs("./data/source", exist_ok=True)
os.makedirs("./data/tactile", exist_ok=True)


with tf.device('/device:GPU:0'):
    data, metadata, circle_data = generate_data(num_samples=NUM_SAMPLES)

    for i in range(len(data)):
        print(f"== Writing file: {i+1}")

        print(f"\t== Writing source file: {i+1}")
        fig_size = random.choices([[512,512], [1024,512], [512,1024]], weights=[.5, .25, .25])[0]
        draw_grid = random.random() < P_grid
        tick_step = random.randint(10, 16)

        write_source_data(data[i], f"./data/source/s_{i+1}.png", fig_size, draw_grid, tick_step)
        postprocessing(f"./data/source/s_{i+1}.png")
        
        print(f"\t== Writing tactile file: {i+1}")
        write_circle_target_data(circle_data[i], f"./data/tactile/t_{i+1}.png", fig_size, draw_grid, tick_step)
        maskgen(f"./data/tactile/t_{i+1}.png")
        
    metadata_df = serialize_data(metadata, ["x", "y"])
    metadata_df.to_csv("metadata.csv", index=False)

# !zip -qq -r ./bardata.zip ./data/ ./metadata.csv
