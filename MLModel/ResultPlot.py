import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import json
import sys

path = sys.argv[1]
method = sys.argv[2]
figure = 1

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
                    plt.figure(figure)
                    plt.plot(x_axis, y_axis)
                    plt.ylabel("MEAN ACCURACY")
                    plt.title(method.upper() + ": " + feature_method.upper())
                    plt.xlabel(parameter.upper())
                    plt.grid(True)
                    plt.show()
                    figure += 1
        elif len(results[feature_method].keys()) == 3:
            z_axis = results[feature_method]["mean"]
            param_id = 1
            for parameter in results[feature_method].keys():
                if parameter != "mean":
                    if param_id == 1:
                        x_axis = results[feature_method][parameter]

                        param_id += 1
                    else:
                        y_axis = results[feature_method][parameter]