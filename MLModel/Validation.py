import warnings
##WARNING warinings are beeing ignored !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
warnings.filterwarnings('ignore')
from sklearn.model_selection import KFold
import numpy as np
from imblearn.over_sampling import SMOTE
from sklearn import metrics as m

'''
Function that does the cross validation applying SMOTE for every model and chooses the best fitting model
@param x the data to fit
@param y the target variable to be predicted
@param models the models to be tested
@param names the name of the models to be tested
'''
def manual_cross_validation(x, y, models, names):
    sm = SMOTE()
    kf = KFold(n_splits=10)
    bestMean = 0.0
    bestModel = None
    bestName = "none"
    for i in xrange(len(models)):
    # do cross_validation
        scores = []
        f1s = []
        average_precisions = []
        recalls = []
        roc_aucs = []
        for train_index, test_index in kf.split(x):
            X_train, X_test = x[train_index], x[test_index]
            y_train, y_test = y[train_index], y[test_index]
            X, Y = sm.fit_sample(X_train, y_train)
            models[i] = models[i].fit(X, Y)
            scores.append(models[i].score(X_test, y_test))
            y_predicted = models[i].predict(X_test)
            y_predicted2=[]
            y_test2=[]
            for k in xrange (len(y_predicted)):
                if(y_predicted[k]=="Easy"):
                    y_predicted2.append(1)
                else:
                    y_predicted2.append(0)
                if(y_test[k]=="Easy"):
                    y_test2.append(1)
                else:
                    y_test2.append(0)

            #calculate performance measures
            f1s.append(m.f1_score(y_test2, y_predicted2))
            average_precisions.append(m.average_precision_score(y_test2, y_predicted2))
            recalls.append(m.recall_score(y_test2, y_predicted2))
            roc_aucs.append(m.roc_auc_score(y_test2, y_predicted2))
        # report results
        scores = np.array(scores)
        score = scores.mean()
        f1s = np.array(f1s)
        average_precisions = np.array(average_precisions)
        recalls = np.array(recalls)
        roc_aucs = np.array(roc_aucs)
        print("%s: "%names[i])
        print("    Accuracy: %0.4f (+/- %0.4f)" % ( score, scores.std() * 2 ))
        print("    F1: %0.4f (+/- %0.4f)" % ( f1s.mean(), f1s.std() * 2 ))
        print("    Average Precision: %0.4f (+/- %0.4f)" % ( average_precisions.mean(), average_precisions.std() * 2 ))
        print("    Recall : %0.4f (+/- %0.4f)" % ( recalls.mean(), recalls.std() * 2 ))
        print("    ROC AUC: %0.4f (+/- %0.4f)" % ( roc_aucs.mean(), roc_aucs.std() * 2 ))

        if (score > bestMean):
            bestMean = score
            bestModel = models[i]
            bestName = names[i]
    return (bestModel, bestName, bestMean)