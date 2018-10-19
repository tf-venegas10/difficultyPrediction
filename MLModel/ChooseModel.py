from sklearn import preprocessing
from GetDataSet import getDataSet
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.feature_selection import VarianceThreshold
from CrossValidation import cross_validation
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.feature_selection import RFECV
from sklearn.externals import joblib
from sklearn.metrics import recall_score

X,Y,X_test,Y_test= getDataSet(100)
# Get the dataset from the database
X, Y, X_test, Y_test = getDataSet()
easyCount = 0
for i in xrange(len(Y_test)):
    if (Y_test[i] == "Easy"):
        easyCount += 1
print("Ratio of Easy over all on testing set: %0.2f" % ((easyCount + 0.0) / len(Y_test)))
easyCount = 0
for i in xrange(len(Y)):
    if (Y[i] == "Easy"):
        easyCount += 1
print("Ratio of Easy over all on training set: %0.2f" % ((easyCount + 0.0) / len(Y)))

# Oversampling of data usign SMOTE algorithm
sm = SMOTE()
x, y = sm.fit_sample(X, Y)

# Normalization of feature values
scaler = preprocessing.MinMaxScaler()
scaler.fit(x)
x_norm = scaler.transform(x)

# initialize models
'''
TO-DO: variate tunning parameters and evaluate the performance behaviour
'''
forest = RandomForestClassifier(n_estimators=100, max_depth=20, random_state=111)
gdBoost = GradientBoostingClassifier(random_state=111)
mlp = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(10, 2), random_state=111)
models = [forest, gdBoost, mlp]
names = ["Random Forest", "Gradient Boosting", "MuliLayer Perceptrons"]

# Vars to select the best suited model
bestModel = None
bestName = "none"
bestMean= 0.0
x_best=[]
scenario = "none"


# Using all the features
print("------------------------------------------")
print("------All Features -----------------------")
model,name,mean=cross_validation(x_norm, y, models, names)
if(mean>bestMean):
    bestModel,bestName,bestMean=model,name,mean
    x_best=x_norm
    scenario = "all"


# Removing features with low variance
print("------------------------------------------")
print("------Removing features with low variance -----------------------")
sel = VarianceThreshold(threshold=(0.01))
x_case = sel.fit_transform(x_norm)
model, name, mean = cross_validation(x_case, y, models, names)
if (mean > bestMean):
    bestModel, bestName, bestMean = model, name, mean
    x_best = x_case
    scenario = "variance"

## Univariate feature selection
# print("------------------------------------------")
# print("------Univariate feature selection-----------------------")
# x_case = SelectKBest(chi2, k=2).fit_transform(x_norm, y)
# model,name,mean=cross_validation(x_case, y, models, names)
# if(mean>bestMean):
#     bestModel,bestName,bestMean=model,name,mean
#     x_best = x_case
#     scenario = "univariate"
# Univariate feature selection
print("------------------------------------------")
print("------Univariate feature selection-----------------------")
'''
TO-DO: variate k values in order to observe the behaviour of model performance and number of top features
'''


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
model, name, mean = cross_validation(x_norm, y, [selectorForest, selectorGB], names)
if (mean > bestMean):
    bestModel, bestName, bestMean = model, name, mean
    x_best = x_norm
    scenario = "all"

print("###########################################")
print("The best model is: %s with and average accuracy of: %0.5f" % (bestName, bestMean))

# Saving the best model
joblib.dump(bestModel, "Best%s.joblib" % bestName)

# train best suited model
bestModel.fit(x_best, y)
scaler.fit(X_test)
x_test_norm=scaler.transform(X_test)
if scenario == "variance":
    x_test_norm = sel.transform(x_test_norm)
testScore = bestModel.score(x_test_norm,Y_test)
recall = recall_score(Y_test, bestModel.predict(x_test_norm), average=None)

print("Best suited model %s, Testing set Accuracy: %0.5f" %(bestName,testScore))
print("Recall: ")
print(recall)

