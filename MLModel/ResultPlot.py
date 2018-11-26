import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import numpy as np
import json
import sys

path = sys.argv[1]
method = sys.argv[2]

if path.endswith(".json"):
    resultsFile = open(path, 'r')
    lines = resultsFile.read()
    results = json.loads(lines)
    resultsFile.close()

    for feature_method in results.keys():
        if len(results[feature_method].keys()) == 2:
            y_axis = results[feature_method]["mean"]
            for parameter in results[feature_method].keys():
                if parameter != "mean":
                    x_axis = results[feature_method][parameter]
                    plt.figure()
                    plt.plot(x_axis, y_axis)
                    plt.ylabel("MEAN ACCURACY")
                    plt.title(method.upper() + ": " + feature_method.upper())
                    plt.xlabel(parameter.upper())
                    plt.grid(True)
                    plt.show()
        elif len(results[feature_method].keys()) == 3:
            z_axis = results[feature_method]["mean"]
            x_axis = []
            x_label = ''
            y_label = ''
            y_axis = []
            param_id = 1
            fig = plt.figure()
            ax = Axes3D(fig)
            for parameter in results[feature_method].keys():
                if parameter != "mean":
                    if param_id == 1:
                        x_axis = results[feature_method][parameter]
                        x_label = parameter
                        ax.set_xlabel(parameter)
                        param_id += 1
                    else:
                        y_axis = results[feature_method][parameter]
                        y_label = parameter
                        ax.set_ylabel(parameter)
            ax.plot_trisurf(x_axis, y_axis, z_axis, linewidth=0)
            ax.set_zlabel("Mean Accuracy")
            max_z = max(z_axis)
            index_coordinates = z_axis.index(max_z)
            max_y = y_axis[index_coordinates]
            max_x = x_axis[index_coordinates]
            label = 'Max Accuracy: %.3f, %s: %d, %s: %d' % (max_z, x_label, max_x, y_label, max_y)
            ax.text2D(0.05, 0.90, label, color='red', transform=ax.transAxes)
            ax.text2D(0.05, 0.95, method.upper() + ": " + feature_method.upper(), transform=ax.transAxes)
            plt.show()
