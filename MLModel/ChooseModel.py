
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


X,Y,X_test,Y_test= getDataSet()
easyCount = 0
for i in xrange(len(Y_test)):
    if(Y_test[i]=="Easy"):
        easyCount += 1
print("Ratio of Easy over all on testing set: %0.2f"%((easyCount+0.0)/len(Y_test)))
easyCount=0
for i in xrange(len(Y)):
    if(Y[i]=="Easy"):
        easyCount += 1
print("Ratio of Easy over all on training set: %0.2f"%((easyCount+0.0)/len(Y)))
sm = SMOTE()
x, y = sm.fit_sample(X, Y)
scaler = preprocessing.MinMaxScaler()
scaler.fit(x)
x_norm=scaler.transform(x)

#initialize models
forest= RandomForestClassifier(n_estimators=100, max_depth=20, random_state=111)
gdBoost = GradientBoostingClassifier(random_state=111)
mlp = MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(10, 2), random_state=111)
models=[forest,gdBoost,mlp]
names= ["Random Forest", "Gradient Boosting", "MuliLayer Perceptrons"]

##Using all the features
print("------------------------------------------")
print("------All Features -----------------------")
cross_validation(x_norm, y, models, names)


##Removing features with low variance
print("------------------------------------------")
print("------Removing features with low variance -----------------------")
sel = VarianceThreshold(threshold=(0.01))
x_case = sel.fit_transform(x_norm)
cross_validation(x_case, y, models, names)

## Univariate feature selection
print("------------------------------------------")
print("------Univariate feature selection-----------------------")
x_case = SelectKBest(chi2, k=2).fit_transform(x_norm, y)
cross_validation(x_case, y, models, names)

##Recursive Elimination
print("------------------------------------------")
print("------Backwards Elimination-----------------------")
selectorForest = RFECV(forest, step=1, cv=3)
selectorForest = selectorForest.fit(x_norm,y)
print("forest be done")
selectorMLP = RFECV(mlp, step=1, cv=3)
selectorMLP = selectorMLP.fit(x_norm,y)
print("forest mlp done")
selectorGB = RFECV(gdBoost, step=1, cv=3)
selectorGB = selectorGB.fit(x_norm,y)
print("forest gb done")
cross_validation(x_norm,y,[selectorForest,selectorGB,selectorMLP], names)


#train best suited model

#forest.fit(x_norm,y)
#gdBoost.fit(x_norm,y)
#x_test_norm=preprocessing.normalize(X_test,"l2")
#testScore = forest.score(x_test_norm,Y_test)
#print("Best suited model %s, Testing set Accuracy: %0.2f" %("Random Forest",testScore))
