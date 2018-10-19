from sklearn.model_selection import cross_val_score

'''
Function that does the cross validation for every model and chooses the best fitting model
@param x the data to fit
@param y the target variable to be predicted
@param models the models to be tested
@param names the name of the models to be tested
'''


def cross_validation(x, y, models, names):
    bestMean = 0.0
    bestModel = None
    bestName = "none"
    for i in xrange(len(models)):
        # do cross_validation
        scores = (cross_val_score(models[i], x, y, cv=10))
        # report results
        print("%s: Accuracy: %0.2f (+/- %0.2f)" % (names[i], scores.mean(), scores.std() * 2))
        if (scores.mean() > bestMean):
            bestMean = scores.mean()
            bestModel = models[i]
            bestName = names[i]

    return (bestModel, bestName, bestMean)
    # scoresForest = (cross_val_score(forest, x, y, cv=10))
    # scoresGB = cross_val_score(gdBoost, x, y, cv=10)
    # scoresMLP = cross_val_score(mlp, x, y, cv=10)
    #
    # # report cross-validation results
    # print("Forest: Accuracy: %0.2f (+/- %0.2f)" % (scoresForest.mean(), scoresForest.std() * 2))
    # print("Gradient Boosting: Accuracy: %0.2f (+/- %0.2f)" % (scoresGB.mean(), scoresGB.std() * 2))
    # print("Multi-layer perceptrons: Accuracy: %0.2f (+/- %0.2f)" % (scoresMLP.mean(), scoresMLP.std() * 2))
