import numpy as np
import retrying
import tensorflow as tf
from tqdm import tqdm

import plotly.graph_objs as go
import plotly.io as pio
import plotly.io._orca
import random
from utils import get_rgb_color, get_random_string

tf.get_logger().setLevel('ERROR')

# Launch orca
unwrapped = plotly.io._orca.request_image_with_retrying.__wrapped__
wrapped = retrying.retry(wait_random_min=1000)(unwrapped)
plotly.io._orca.request_image_with_retrying = wrapped

MAX_Y = 100
MIN_Y = 0

# These set the ordering of bars: Ascending, descending or normal
PLOT_ORDER = {"0": 0, "1": 0, "2": 0}
SIZEREFS = {"1": 7.0, "2": 2.5 , "3": 2.0}

def generate_metadata(min_y = 0, max_y = 100):
    num_bars = 10 # np.random.randint(low=3, high=20+1) # Generate random number for number of bars, min: 3, max: 20
    x = list(range(num_bars))
    
    num_groups = np.random.randint(low=1, high=2+1)
    
    # Generate random values for bars
    y = np.random.randint(low = min_y, high = max_y + 1, size=(num_groups, num_bars))

    # Sort y plots accordingly
    sort_plots(y) 
    
    return {'x': x, 'y': y}

def sort_plots(plots):
    for i in range(len(plots)):
        t = plots[i]
        if PLOT_ORDER[str(i)] % 3 == 1:
            t = np.sort(t)
        elif PLOT_ORDER[str(i)] % 3 == 2:
            t = np.sort(t)
            t = np.flip(t)
            
        plots[i] = t
        PLOT_ORDER[str(i)] += 1
            
def generate_data(num_samples = 1):
    data = list()
    metadata = list()
    circle_data = list()
    
    for i in tqdm(range(num_samples), desc="generating metadata: "):
        
        sample = {}
        
        sample_metadata = generate_metadata()
        
        
        sample["y_values"] = sample_metadata["y"]
        sample["x_values"] = sample_metadata["x"]
              
        num_bars = len(sample["y_values"][0])
        num_groups = len(sample["y_values"])
        min_x = np.amin(sample["x_values"])
        max_x = np.amax(sample["x_values"])
        min_y = np.amin(sample["y_values"])
        max_y = np.amax(sample["y_values"])
        
        sample_styles = generate_styles(num_bars=num_bars, num_groups = num_groups, min_x=min_x, max_x=max_x, min_y=min_y, max_y=max_y)
        
        sample["marker_colors"] = sample_styles["marker_colors"]
        sample["marker_colors_rgba"] = sample_styles["marker_colors_rgba"]
        sample["plot_bg_color"] = sample_styles["plot_bg_color"]
        sample["plot_bg_color_rgba"] = sample_styles["plot_bg_color_rgba"]
        sample["bargap"] = sample_styles["bargap"]
        sample["bargroupgap"] = sample_styles["bargroupgap"]
        sample["x_tick_start"] = sample_styles["xaxis"]["tick0"]
        sample["x_tick_dist"] = sample_styles["xaxis"]["dtick"]
        sample["y_tick_start"] = sample_styles["yaxis"]["tick0"]
        sample["y_tick_dist"] = sample_styles["yaxis"]["dtick"]
        
        circle_data_sample = generate_circle_bars(sample)
        
        data.append(sample)
        metadata.append(sample_metadata)
        circle_data.append(circle_data_sample)
        
    return data, metadata, circle_data

def generate_marker_colors(num_groups, num_bars):
    one_color = np.random.randint(2) # Generate one color or different colors for bars
    
    # Avoid full black or full white
    if num_groups > 1:
        marker_colors = [(np.random.randint(low=1, high=255), np.random.randint(low=1, high=255), np.random.randint(low=1, high=255), np.round(np.random.uniform(0.5, 1), 2)) for i in range(num_groups)]
        marker_colors_as_str = ["rgba" + str(c) for c in marker_colors]  
    elif one_color:
        marker_colors = (np.random.randint(low=1, high=255), np.random.randint(low=1, high=255), np.random.randint(low=1, high=255), np.round(np.random.uniform(0.5, 1), 2))
        marker_colors_as_str = "rgba" + str(marker_colors)
    else:
        marker_colors = [(np.random.randint(low=1, high=255), np.random.randint(low=1, high=255), np.random.randint(low=1, high=255), np.round(np.random.uniform(0.5, 1), 2)) for i in range(num_bars)]
        marker_colors_as_str = ["rgba" + str(c) for c in marker_colors]
        
    return marker_colors, marker_colors_as_str

def compute_sizeref(plot_size = 500, num_groups = 1, rangey = 100):
    width = (plot_size / rangey) / (num_groups * 2 - 1)
    return ((2.0 *  width)/((3 * width)**2))

def compute_scatter_width(plot_size = 500, num_groups = 1, num_bars = 20):
    div = 4 if num_groups == 2 else 3
    temp_width = (plot_size / (((num_bars - 1) * (num_groups + (num_groups / div))) + num_groups)) / num_groups
    width = 7.5 if temp_width > 7.5 else temp_width
    if width >= 7.5 and num_groups == 2:
        width = 5.5
    return SIZEREFS[str(num_groups)] * (20.0 / num_bars)

def generate_bar_widths(num_bars):
    one_width = np.random.randint(2) # Generate one width or different widths for bars
    if one_width:
        widths = np.random.uniform(0.1, 1)
    else:
        widths = np.random.uniform(low = 0.1, high = 1, size=num_bars)
    return widths

def generate_bar_gap():
    return np.round(np.random.uniform(0, 0.5), 2)

def generate_bar_group_gap():
    return np.round(np.random.uniform(0, 0.5), 2)

def generate_tick_size(min, max):
    if min <= 0:
        start = 0
    else: 
        start = np.random.randint(0, min)
    
    # Minimum number of ticks is 2, max is 20 
    size = np.round((max - min) / np.random.randint(2, 20 + 1), 2)
    return start, size

def generate_plot_bgcolor():
    is_white = np.random.randint(2) # White or any color
    if is_white:
        bg_color = (255, 255, 255, 1)
    else:
        bg_color = (np.random.randint(low=0, high=255 + 1), np.random.randint(low=0, high=255 + 1), np.random.randint(low=0, high=255 + 1), np.round(np.random.uniform(0, 0.35), 2))

    bg_color_rgba = "rgba" + str(bg_color)
    
    return bg_color, bg_color_rgba

def generate_plot_paper_color():
    is_white = np.random.randint(2) # White or any color
    if is_white:
        paper_color = (255, 255, 255, 1)
    else:
        paper_color = (np.random.randint(low=0, high=255 + 1), np.random.randint(low=0, high=255 + 1), np.random.randint(low=0, high=255 + 1), np.round(np.random.uniform(0, 0.35), 2))

    paper_color_rgba = "rgba" + str(paper_color)
    
    return paper_color, paper_color_rgba

# Genere points for circle bar chart
def generate_circle_bars_one(data):
    num_bars = len(data["x_values"])
    num_groups = len(data["y_values"])
    width  = 30.75 # compute_scatter_width(num_groups = num_groups, num_bars = num_bars)
    group_points = []
    
    for i in range(num_groups):
        bar_points = []
        for j in range(num_bars):
            x = data["x_values"][j] + (data["x_values"][j] * 0.0)
            pointsx = [x]
            pointsy = [0]
            widths = [0]
            endy = data["y_values"][i][j]
            curryst = 4.25
            
            if endy < 2.5:
                continue

            while(curryst <= endy):
                pointsx.append(x)
                pointsy.append(curryst)
                widths.append(width)

                curryst = curryst + 7.5

            bar_points.append({"x": pointsx, "y": pointsy, "widths": widths})

        group_points.append(bar_points)
        
    return group_points

def generate_circle_bars_two(data):
    num_bars = len(data["x_values"])
    num_groups = len(data["y_values"])
    width  = 11.5 # compute_scatter_width(num_groups = num_groups, num_bars = num_bars)
    group_points = []
    
    for i in range(num_groups):
        bar_points = []
        for j in range(num_bars):
            x = data["x_values"][j] + (i * 0.35)
            pointsx = [x]
            pointsy = [0]
            widths = [0]
            endy = data["y_values"][i][j]
            curryst = 2

            while(curryst < endy):
                pointsx.append(x)
                pointsy.append(curryst)
                widths.append(width)

                curryst = curryst + 3

            bar_points.append({"x": pointsx, "y": pointsy, "widths": widths})

        group_points.append(bar_points)
        
    return group_points

def generate_circle_bars_three(data):
    num_bars = len(data["x_values"])
    num_groups = len(data["y_values"])
    width  = 8.125 #compute_scatter_width(num_groups = num_groups, num_bars = num_bars) 
    group_points = []
    
    for i in range(num_groups):
        bar_points = []
        for j in range(num_bars):
            x = data["x_values"][j] + (i * 0.25)
            pointsx = [x]
            pointsy = [0]
            widths = [0]
            endy = data["y_values"][i][j]
            curryst = 1.5

            while(curryst < endy):
                pointsx.append(x)
                pointsy.append(curryst)
                widths.append(width)

                curryst = curryst + 2.125

            bar_points.append({"x": pointsx, "y": pointsy, "widths": widths})

        group_points.append(bar_points)
        
    return group_points

def generate_circle_bars(data):
    num_groups = len(data["y_values"])
    
    if num_groups == 1:
        return generate_circle_bars_one(data)
    if num_groups == 2:
        return generate_circle_bars_two(data)
    if num_groups == 3:
        return generate_circle_bars_three(data)

def generate_styles(num_bars, num_groups, min_x, max_x, min_y, max_y):
    (marker_colors, marker_colors_rgba) = generate_marker_colors(num_groups, num_bars)
    (plot_bg_color, plot_bg_color_rgba) = generate_plot_bgcolor()
    bargap = generate_bar_gap()
    bargroupgap = generate_bar_group_gap()
    (xtick_start, xtick_size) = generate_tick_size(min_x, max_x)
    (ytick_start, ytick_size) = generate_tick_size(min_y, max_y)
    
    styles = {
        "marker_colors": marker_colors,
        "marker_colors_rgba": marker_colors_rgba,
        "plot_bg_color": plot_bg_color,
        "plot_bg_color_rgba": plot_bg_color_rgba,
        "bargap": bargap,
        "bargroupgap": bargroupgap,
        "xaxis": {
            "tick0": xtick_start,
            "dtick": xtick_size
        },
        "yaxis": {
            "tick0": ytick_start,
            "dtick": ytick_size
        }
    }
    
    return styles

# Draw source domain
def write_source_data(data, filepath, figsize=(512, 512), draw_grid=False, tick_step=10, orientation='v', p_legend=0):
    fig = go.Figure()

    for r in range(len(data["y_values"])):
        if orientation == 'v':
            trace_args = {
                'x': data["x_values"],
                'y': data["y_values"][r],
                'orientation': "v",
                'marker_color': data["marker_colors_rgba"][r] if len(data["y_values"]) > 1 else data["marker_colors_rgba"],
                'marker_line_width': 2
                }
        else:
            trace_args = {
                'x': data["y_values"][r],
                'y': data["x_values"],
                'orientation': "h",
                'marker_color': data["marker_colors_rgba"][r] if len(data["y_values"]) > 1 else data["marker_colors_rgba"],
                'marker_line_width': 2
            }

        fig.add_trace(go.Bar(**trace_args))
    
    axis_lw = random.randint(1,5)
    if orientation == 'v':
        layout_args = {
            'margin': dict(l=5, r=25, t=30, b=25),
            'plot_bgcolor': data["plot_bg_color_rgba"],
            'width': figsize[0],
            'height': figsize[1],
            'xaxis_range': [-0.5,10],
            'yaxis_range': [0,110],
            'bargap': data["bargap"],
            'bargroupgap': data["bargroupgap"],
            'showlegend': False,
            'xaxis': {
                "showline": True, 
                "linewidth": axis_lw, 
                "linecolor": 'black',
            },
            'yaxis': {
                "showline": True, 
                "linewidth": axis_lw, 
                "linecolor": 'black',
                "ticks": "outside",
                "dtick": tick_step
            }
        }
    else:
        layout_args = {
            'margin': dict(l=25, r=30, t=5, b=25),
            'plot_bgcolor': data["plot_bg_color_rgba"],
            'width':figsize[0],
            'height': figsize[1],
            'yaxis_range': [-0.5,10],
            'xaxis_range': [0,110],
            'bargap': data["bargap"],
            'bargroupgap': data["bargroupgap"],
            'showlegend': False,
            'xaxis': {
                "showline": True, 
                "linewidth": axis_lw, 
                "linecolor": 'black',
                "dtick": tick_step
            },
            'yaxis':{
                "showline": True, 
                "linewidth": axis_lw, 
                "linecolor": 'black',
                "ticks": "outside",
            }
        }

    fig.update_layout(**layout_args)
    

    fig.update_yaxes(showgrid=False)
    if draw_grid:
        ls = random.choice(['solid', 'dot', 'dash', 'longdash', 'dashdot', 'longdashdot'])
        lw = random.randint(1,2)
        if orientation == 'v':
            fig.update_yaxes(showgrid=True, gridcolor=get_rgb_color(1)[:-2], gridwidth=lw, griddash=ls)
        else:
            fig.update_xaxes(showgrid=True, gridcolor=get_rgb_color(1)[:-2], gridwidth=lw, griddash=ls)
    
    if random.random() < p_legend:
        fig.update_layout(title_text=get_random_string(40, min_length=10),
        title_x=random.uniform(0.0,0.9),
        title_y=1,
    	title_font_size= random.randint(25,35)
        )
    # if random.random() < p_legend:
    #     fig.update_layout(
    #         xaxis_title = get_random_string(20, 5),
    #         font = {
    #             "size": int(random.randint(15, 25)),
    #             "color": get_rgb_color(1)[:-2]
    #         }
    #     )
    # if random.random() < p_legend:
    #     fig.update_layout(
    #         yaxis_title = get_random_string(20, 5),
    #         font = {
    #             "size": int(random.randint(15, 25)),
    #             "color": get_rgb_color(1)[:-2]
    #         }
    #     )

    pio.write_image(fig=fig, file=filepath, format="png", width=figsize[0], height=figsize[1])
    
    
def write_circle_target_data(data, filepath, figsize=(512, 512), draw_grid=False, tick_step=10, target='rgb', orientation='v'):
    fig = go.Figure()
    for i in range(len(data)):
        for j in range(len(data[i])):
            if orientation == 'v':
                trace_args={
                    'x': data[i][j]["x"],
                    'y': data[i][j]["y"],
                    'marker': {
                            "size":np.array(data[i][j]["widths"])*np.sqrt(figsize[1]/figsize[0]),
                            "sizemode":'diameter',
                            "sizeref": 1
                        },
                    }

            else:
                trace_args={
                    'x': data[i][j]["y"],
                    'y': data[i][j]["x"],
                    'marker': {
                        "size":np.array(data[i][j]["widths"])*np.sqrt(figsize[0]/figsize[1]),        
                        "sizemode":'diameter',
                        "sizeref": 1,
                    },
                }

            fig.add_trace(go.Scatter(**trace_args))
    
    fig.update_traces(mode='markers', marker_line_width=1, visible=False)

    fp_parts = filepath.rsplit(".", 1)
    if orientation == 'v':
        layout_args = {
        'plot_bgcolor': "white",
        'margin': dict(l=30, r=30, t=30, b=30),
        'width': figsize[0],
        'height': figsize[1],
        'yaxis_range': [0,110],
        'xaxis_range': [-0.5,10],
        'xaxis': {"showticklabels": False, "linewidth": 2, "linecolor": 'black'},
        'yaxis': {"showticklabels": False, "linewidth": 2, "linecolor": 'black', "ticks": "outside", "dtick": tick_step, "ticklen": 10, "tickwidth": 2},
        'showlegend':False
        }
    else:
        layout_args = {
            'plot_bgcolor': "white",
        'margin': dict(l=30, r=30, t=30, b=30),
        'width': figsize[0], 
        'height': figsize[1],
        'xaxis_range': [0,110],
        'yaxis_range': [-0.5,10],
        'yaxis': {"showticklabels": False, "linewidth": 2, "linecolor": 'black'},
        'xaxis': {"showticklabels": False, "linewidth": 2, "linecolor": 'black', "ticks": "outside", "dtick": tick_step, "ticklen": 10, "tickwidth": 2},
        'showlegend': False
        }

    fig.update_layout(layout_args)
    
    if orientation == 'v':
        fig.update_layout(yaxis={"ticks": "outside", "dtick": tick_step, "ticklen": 10, "tickwidth": 2})
    else:
        fig.update_layout(xaxis={"ticks": "outside", "dtick": tick_step, "ticklen": 10, "tickwidth": 2})    

    if target == 'rgb':
        if draw_grid:
            if orientation == 'v':
                fig.update_yaxes(showgrid=True, gridcolor='blue', griddash='dash', gridwidth=1)
            else:
                fig.update_xaxes(showgrid=True, gridcolor='blue', griddash='dash', gridwidth=1)

        fig.update_traces(mode='markers', marker_line_width=2, marker_color="white", marker_line_color="red", visible=True)
        pio.write_image(fig=fig, file=f"{fp_parts[0]}.{fp_parts[1]}", format="png", width=figsize[0], height=figsize[1])

    else:
        pio.write_image(fig=fig, file=f"{fp_parts[0]}_axes.{fp_parts[1]}", format="png", width=figsize[0], height=figsize[1])

        if draw_grid:
            if orientation == 'v':
                fig.update_yaxes(showgrid=True, gridcolor='black', griddash='dash', gridwidth=1)
            else:
                fig.update_xaxes(showgrid=True, gridcolor='black', griddash='dash', gridwidth=1)
                
        fig.update_layout(xaxis={"linecolor": 'white',  "ticklen": 0, "tickwidth": 0}, yaxis={"linecolor": 'white', "ticklen": 0, "tickwidth": 0})
        pio.write_image(fig=fig, file=f"{fp_parts[0]}_grids.{fp_parts[1]}", format="png", width=figsize[0], height=figsize[1])

        fig.update_traces(mode='markers', marker_line_width=2, marker_color="white", marker_line_color="black", visible=True)
        fig.update_layout(yaxis={"showgrid":False}, xaxis={"showgrid":False})

        pio.write_image(fig=fig, file=f"{fp_parts[0]}_content.{fp_parts[1]}", format="png", width=figsize[0], height=figsize[1])

