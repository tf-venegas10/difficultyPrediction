
from sklearn import preprocessing
from GetDataSet import getDataSubSet
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.feature_selection import VarianceThreshold
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.feature_selection import RFECV
from sklearn.externals import joblib
from Validation import manual_cross_validation
from sklearn import metrics as m

#set that defines the different sets of features that will be used
#features = [1,2,3,4,5,6,7,44]+[x for x in xrange(8,15)]+[31,32,33,34,45,50]+[c for c in xrange(35,44)]+[56,57,58,60,65,67,68,84]
features =[11, 12, 14, 16, 19, 20, 23, 24, 25, 30, 63]
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
forest= RandomForestClassifier(n_estimators=100, max_depth=20, random_state=111)
gdBoost = GradientBoostingClassifier(random_state=111)
mlp = MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(10, 2), random_state=111)
models=[forest,gdBoost,mlp]
names= ["Random Forest", "Gradient Boosting", "MuliLayer Perceptrons"]



##Using all the features
model,name,mean=manual_cross_validation(x_norm, y, models, names, True)
if(mean>bestMean):
    bestModel,bestName,bestMean=model,name,mean
    bestSet = features


print("###########################################")
print("The best model is: %s with and average accuracy of: %0.5f"%(bestName,bestMean))

print("###########")
# train best suited model
bestModel.fit(x_norm, y)
scaler.fit(X_test)
x_test_norm = scaler.transform(X_test)
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