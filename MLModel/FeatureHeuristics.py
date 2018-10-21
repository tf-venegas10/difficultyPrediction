from sklearn import metrics as m
from sklearn import preprocessing
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from sklearn.feature_selection import RFECV
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import VarianceThreshold
from sklearn.feature_selection import chi2
from sklearn.neural_network import MLPClassifier

from GetDataSet import getDataSet
from Validation import manual_cross_validation

feature_amount = 10


def tree_selection_heuristic(x_norm, y, X_test, Y_test):
    id = x_norm.keys()[0]
    # A feature hash is created to transform nominal features into numerical identifiers
    feature_hash = {}
    i = 1
    # The hash for every feature is created
    for f in x_norm[id]:
        feature_hash[i] = f
        i += 1

    # The feature set that is going to be evaluated
    feature_set = [0]
    max_accuracy = 0.0
    best_set = []
    best_model = None

    # For every set of 1 feature the recursive search is applied
    for i in range(1, len(feature_amount) + 1, 1):
        feature_set.pop()
        feature_set.append(i)
        new_x_norm = build_dataset(x_norm, feature_set, feature_hash)
        new_x_test = build_dataset(X_test, feature_set, feature_hash)
        calc_accuracy, calc_best_model = choose_model(new_x_norm, y, new_x_test, Y_test)
        calc_accuracy, calc_best_set, calc_best_model = recursive_tree_exploration(x_norm, y, X_test, Y_test,
                                                                                   feature_set, feature_hash,
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


def recursive_tree_exploration(x_norm, y, X_test, Y_test, feature_set, feature_hash, past_accuracy, past_model):
    last_added = feature_set[len(feature_set) - 1]
    last_added += 1
    new_feature_set = feature_set.append(0)

    max_accuracy = past_accuracy
    best_set = feature_set
    best_model = past_model
    for i in range(last_added, len(feature_amount), 1):
        new_feature_set.pop()
        new_feature_set.append(i)
        new_x_norm = build_dataset(x_norm, new_feature_set, feature_hash)
        new_x_test = build_dataset(X_test, new_feature_set, feature_hash)
        calc_accuracy, calc_best_model = choose_model(new_x_norm, y, new_x_test, Y_test)
        if calc_accuracy > max_accuracy:
            calc_accuracy, calc_best_set, calc_best_model = recursive_tree_exploration(x_norm, y, X_test, Y_test,
                                                                                       new_feature_set, feature_hash,
                                                                                       calc_accuracy, calc_best_model)
            if calc_accuracy > max_accuracy:
                max_accuracy = calc_accuracy
                best_set = calc_best_set
                best_model = calc_best_model

    return max_accuracy, best_set, best_model


def build_dataset(x_norm, range, hash):
    x = {}
    for id in x_norm.keys:
        for cod in range:
            x[id] = {}
            x[id][hash[cod]] = x_norm[id][hash[cod]]
    return x


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
    print("------------------------------------------")
    print("------All Features -----------------------")
    model, name, mean = manual_cross_validation(x_norm, y, models, names)
    if mean > bestMean:
        bestModel, bestName, bestMean = model, name, mean
        x_best = x_norm
        scenario = "all"

    # Removing features with low variance
    print("------------------------------------------")
    print("------Removing features with low variance -----------------------")
    sel = VarianceThreshold(threshold=(0.01))
    x_case = sel.fit_transform(x_norm)
    model, name, mean = manual_cross_validation(x_case, y, models, names)
    if mean > bestMean:
        bestModel, bestName, bestMean = model, name, mean
        x_best = x_case
        scenario = "variance"

    # Univariate feature selection
    print("------------------------------------------")
    print("------Univariate feature selection-----------------------")
    sel2 = SelectKBest(chi2, k=2)
    x_case = sel2.fit_transform(x_norm, y)

    model, name, mean = manual_cross_validation(x_case, y, models, names)
    if mean > bestMean:
        bestModel, bestName, bestMean = model, name, mean
        x_best = x_case
        scenario = "univariate"

    # Recursive Elimination
    print("------------------------------------------")
    print("------Backwards Elimination-----------------------")

    selectorGB = RFECV(gdBoost, step=1, cv=3)
    selectorGB = selectorGB.fit(x_norm, y)
    joblib.dump(selectorGB, 'BEGrandientBoosting.joblib')
    print(" gb done")
    selectorForest = RFECV(forest, step=1, cv=3)
    selectorForest = selectorForest.fit(x_norm, y)
    joblib.dump(selectorForest, 'BERandomForest.joblib')
    print("forest be done")
    # selectorMLP = RFECV(mlp, step=1, cv=3)
    # selectorMLP = selectorMLP.fit(x_norm,y)
    # print(" mlp done")
    model, name, mean = manual_cross_validation(x_norm, y, [selectorForest, selectorGB], names)
    if mean > bestMean:
        bestModel, bestName, bestMean = model, name, mean
        x_best = x_norm
        scenario = "all"

    print("###########################################")
    print("The best model is: %s with and average accuracy of: %0.5f" % (bestName, bestMean))

    ## Saving the best model
    joblib.dump(bestModel, "Best%s.joblib" % bestName)

    # train best suited model
    bestModel.fit(x_best, y)
    scaler = preprocessing.MinMaxScaler()
    scaler.fit(X_test)
    x_test_norm = scaler.transform(X_test)
    if scenario == "variance":
        x_test_norm = sel.transform(x_test_norm)
    elif scenario == "univariate":
        x_test_norm = sel2.transform(x_test_norm)
    testScore = bestModel.score(x_test_norm, Y_test)
    y_predicted = bestModel.predict(x_test_norm)
    y_predicted2 = []
    y_test2 = []
    for k in xrange(len(y_predicted)):
        if (y_predicted[k] == "Easy"):
            y_predicted2.append(1)
        else:
            y_predicted2.append(0)
        if (Y_test[k] == "Easy"):
            y_test2.append(1)
        else:
            y_test2.append(0)

    f1 = (m.f1_score(y_test2, y_predicted2))
    average_precision = (m.average_precision_score(y_test2, y_predicted2))
    recall = (m.recall_score(y_test2, y_predicted2))
    roc_auc = (m.roc_auc_score(y_test2, y_predicted2))

    print("Best suited model %s: TESTING SET" % (bestName))
    print("     Accuracy: %0.5f" % testScore)
    print("     F1: %0.5f" % f1)
    print("     Average Precision: %0.5f" % average_precision)
    print("     Recall: %0.5f" % recall)
    print("     ROC AUC: %0.5f" % roc_auc)

    return average_precision, bestModel


X, y, X_test, Y_test = getDataSet(feature_amount)
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

tree_selection_heuristic(x_norm, y, X_test, Y_test)
