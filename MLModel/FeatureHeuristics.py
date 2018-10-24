import numpy as np
from sklearn import metrics as m
from sklearn import preprocessing
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from sklearn.neural_network import MLPClassifier
import copy

from GetDataSet import getDataSet
from Validation import manual_cross_validation

feature_lower_bound = 0
feature_upper_bound = 100
feature_amount = 64


def tree_selection_heuristic(x_norm, y, X_test, Y_test):
    # The feature set that is going to be evaluated
    feature_set = [0]
    max_accuracy = 0.0
    best_set = []
    best_model = None

    # For every set of 1 feature the recursive search is applied
    for i in xrange(feature_amount):
        feature_set.pop()
        feature_set.append(i)
        new_x_norm = build_dataset(x_norm, feature_set)
        new_x_test = build_dataset(X_test, feature_set)
        calc_accuracy, calc_best_model = choose_model(new_x_norm, y, new_x_test, Y_test)
        calc_accuracy, calc_best_set, calc_best_model = recursive_tree_exploration(x_norm, y, X_test, Y_test,
                                                                                   feature_set,
                                                                                   calc_accuracy, calc_best_model)
        if calc_accuracy > max_accuracy:
            max_accuracy = calc_accuracy
            best_set = calc_best_set
            best_model = calc_best_model

    print "-----------------------------------"
    print "---------BEST FEATURE SET----------"
    print best_set

    print "-----------------------------------"
    print "-------------ACCURACY--------------"
    print max_accuracy

    return best_model


def recursive_tree_exploration(x_norm, y, X_test, Y_test, feature_set, past_accuracy, past_model):
    last_added = feature_set[len(feature_set) - 1]
    last_added += 1
    new_feature_set = copy.copy(feature_set)
    new_feature_set.append(0)

    max_accuracy = past_accuracy
    best_set = feature_set
    best_model = past_model
    for iter in range(last_added, feature_amount, 1):
        new_feature_set.pop()
        new_feature_set.append(iter)
        new_x_norm = build_dataset(x_norm, new_feature_set)
        new_x_test = build_dataset(X_test, new_feature_set)
        calc_accuracy, calc_best_model = choose_model(new_x_norm, y, new_x_test, Y_test)
        if calc_accuracy > max_accuracy:
            max_accuracy = calc_accuracy
            best_set = new_feature_set
            best_model = calc_best_model
            calc_accuracy, calc_best_set, calc_best_model = recursive_tree_exploration(x_norm, y, X_test, Y_test,
                                                                                       new_feature_set,
                                                                                       max_accuracy, calc_best_model)
            if calc_accuracy > max_accuracy:
                max_accuracy = calc_accuracy
                best_set = calc_best_set
                best_model = calc_best_model

    print best_set
    print "BEST SET ACCURACY: "+str(max_accuracy)
    print "BEST SET MODEL: " + str(best_model)
    return max_accuracy, best_set, best_model


def build_dataset(x_norm, range):
    x = []
    for vid in x_norm:
        feat_vals = []
        for cod in range:
            feat_vals.append(vid[cod])
        x.append(feat_vals)
    return np.asmatrix(x)


def choose_model(x_norm, y, X_test, Y_test):
    # initialize models
    forest = RandomForestClassifier(n_estimators=100, max_depth=20, random_state=111)
    gdBoost = GradientBoostingClassifier(random_state=111)
    mlp = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(10, 2), random_state=111)
    models = [forest, gdBoost, mlp]
    names = ["Random Forest", "Gradient Boosting", "MuliLayer Perceptrons"]

    # Vars to select the best suited model
    bestModel = None
    bestName = "none"
    bestMean = 0.0
    x_best = []
    scenario = "none"

    # Using all the features
    # print("------------------------------------------")
    # print("------All Features -----------------------")
    model, name, mean = manual_cross_validation(x_norm, y, models, names, silent=True)
    if mean > bestMean:
        bestModel, bestName, bestMean = model, name, mean

    # print("###########################################")
    # print("The best model is: %s with and average accuracy of: %0.5f" % (bestName, bestMean))

    # Saving the best model
    joblib.dump(bestModel, "Best%s.joblib" % bestName)

    # print("Best suited model %s: TESTING SET" % (bestName))
    # print("     Accuracy: %0.5f" % testScore)
    # print("     F1: %0.5f" % f1)
    # print("     Average Precision: %0.5f" % average_precision)
    # print("     Recall: %0.5f" % recall)
    # print("     ROC AUC: %0.5f" % roc_auc)

    return bestMean, bestName


X, y, X_test, Y_test = getDataSet(feature_lower_bound, feature_upper_bound)
## Count number of 'easy' labeled instances and total instances
# This is done to keep control of the correct distribution of the dataset and the parameters of the experiment.
easyCount = 0
totalCount = 0
for i in xrange(len(Y_test)):
    if (Y_test[i] == "Easy"):
        easyCount += 1
    totalCount += 1
print("Ratio of Easy over all on testing set: %0.2f" % ((easyCount + 0.0) / len(Y_test)))
easyCount = 0
for i in xrange(len(y)):
    if (y[i] == "Easy"):
        easyCount += 1
    totalCount += 1
print("Ratio of Easy over all on training set: %0.2f" % ((easyCount + 0.0) / len(y)))
print("Number of instances: %0.0f" % (totalCount))

scaler = preprocessing.MinMaxScaler()
scaler.fit(X)
x_norm = scaler.transform(X)
feature_amount = len(x_norm[0])
print "FEATURE AMOUNT: "+str(feature_amount)

tree_selection_heuristic(x_norm, y, X_test, Y_test)
