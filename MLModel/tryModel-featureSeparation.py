
from sklearn import metrics as m
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from imblearn.over_sampling import SMOTE

from GetDataSet import getDataSubSet

#set that defines the different sets of features that will be used
#features = [1,2,3,4,5,6,7,44]+[x for x in xrange(8,15)]+[31,32,33,34,45,50]+[c for c in xrange(35,44)]+[56,57,58,60,65,67,68,84]
#features =[3, 5, 34, 35, 38, 39, 40, 42, 51, 52, 56, 60, 62, 99]
features = [x for x in range(100,300)]
print features
# Vars to select the best suited model
bestModel = None
bestName = "none"
bestMean = 0.0
bestSet = []

X,y,X_test,Y_test= getDataSubSet(features)
scaler = preprocessing.MinMaxScaler()
scaler.fit(X)
x_norm=scaler.transform(X)

#initialize models
#forest= RandomForestClassifier(n_estimators=9100, max_depth=300, random_state=111)
gdBoost = GradientBoostingClassifier(random_state=111)
# mlp = MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(10, 2), random_state=111)
# models=[forest,gdBoost,mlp]
# names= ["Random Forest", "Gradient Boosting", "MuliLayer Perceptrons"]
#
#
#
# ##Using all the features
# model,name,mean=manual_cross_validation(x_norm, y, models, names, True)
# if(mean>bestMean):
#     bestModel,bestName,bestMean=model,name,mean
#     bestSet = features
#

#apply smote to training set
sm = SMOTE()
x_norm,y = sm.fit_sample(x_norm,y)

gdBoost.fit(x_norm,y)
print("###########################################")
print("The best model is: %s with and average accuracy of: %0.5f"%(bestName,bestMean))

print("###########")
# train best suited model
#bestModel.fit(x_norm, y)



scaler.fit(X_test)
x_test_norm = scaler.transform(X_test)
testScore = gdBoost.score(x_test_norm, Y_test)
y_predicted = gdBoost.predict(x_test_norm)
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