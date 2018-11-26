import copy

from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier

from GetDataSet import getDataSubSet
from Validation import manual_cross_validation

feature_lower_bound = 0
feature_upper_bound = 100
feature_amount = 100
# initialize models
forest = RandomForestClassifier(n_estimators=100, max_depth=20, random_state=111)
gdBoost = GradientBoostingClassifier(random_state=111)
mlp = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(10, 2), random_state=111)
models = [forest, gdBoost, mlp]
names = ["Random Forest", "Gradient Boosting", "MuliLayer Perceptrons"]

def tree_selection_heuristic():
    # The feature set that is going to be evaluated
    feature_set = [0]
    max_accuracy = 0.0
    best_set = []
    best_model = None

    # For every set of 1 feature the recursive search is applied
    for i in xrange(1,feature_amount):
        feature_set.pop()
        feature_set.append(i)
        new_x_norm,y, _, _ = getDataSubSet(feature_set)
        #INIT FOR RECURSIVE CALL
        model, calc_best_model, calc_accuracy = manual_cross_validation(new_x_norm, y, models, names,True)
        #RECURSIVE CALL
        calc_accuracy, calc_best_set, calc_best_model = recursive_tree_exploration(feature_set,
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


def recursive_tree_exploration( feature_set, past_accuracy, past_model):
    last_added = feature_set[len(feature_set) - 1]
    new_feature_set = copy.copy(feature_set)
    #POR QUe AGREGAR 0 ??
    ## COUNT 1 APPEND
    new_feature_set.append(0)

    max_accuracy = past_accuracy
    best_set = feature_set
    best_model = past_model
    for iter in xrange(last_added +1, feature_amount):
        ## COUNT 1 POP
        new_feature_set.pop()
        ## COUNT 1 APPEND
        new_feature_set.append(iter)
        new_x_norm, y, _, _ = getDataSubSet(new_feature_set)
        model, calc_best_model, calc_accuracy = manual_cross_validation(new_x_norm, y, models, names,True)
        if calc_accuracy > max_accuracy:
            max_accuracy = calc_accuracy
            best_set = new_feature_set
            best_model = calc_best_model
            calc_accuracy, calc_best_set, calc_best_model = recursive_tree_exploration(new_feature_set,max_accuracy, calc_best_model)
            if calc_accuracy > max_accuracy:
                max_accuracy = calc_accuracy
                best_set = calc_best_set
                best_model = calc_best_model

    print best_set
    print "BEST SET ACCURACY: "+str(max_accuracy)
    print "BEST SET MODEL: " + str(best_model)
    return max_accuracy, best_set, best_model







## Count number of 'easy' labeled instances and total instances
# This is done to keep control of the correct distribution of the dataset and the parameters of the experiment.



tree_selection_heuristic()
