## Dataset Generation
To start from scratch we need to generate training and testing samples for the model.
If we wish to generate more samples the code is provided on `datagen` folder and we should run `python ./datagen/draw_plot.py`. This file takes input arguments to change the number of instances to generate listed below.

- `--cnt_bezier`: The number of bezier curve samples can be changed using this argument.
- `--cnt_scatter`: The number of scatter plot samples can be changed using this argument.
- `--cnt_polygon`: The number of polygon samples can be changed using this argument.
- `--p_figsize`: This argument controls the percentage of squared, vertical and horizontal plots. For instance with [0.5, 0.3, 0.2] results in 50% squared, 30% vertical and 20% horizontal plots.
- `--p_1D`: This argument controls the percentage of bezier curves that strictly have no intersections. 
- `--p_grid`: This argument controls the percentage of samples with gridlines.

As an example of running the code using all of these arguments we can write `python ./datagen/draw_plot.py --cnt_bezier 10 --cnt_scatter 5 --cnt_polygon 6 --p_figsize 0.33 0.33 0.33 --p_1D 0.9 --p_grid 0.1`. After generating samples, we should split them as train and test sets each having source and tactile folders.

**_NOTE:_** By default a dataset of 5000 samples (2000 bezier curves, 1500 polygons and, 1500 scatter plots) has been provided. 90% of the data was assigned to training process and the rest of them belongs to test process. Both of the subsets are balanced and we can find them on `data` directory.
