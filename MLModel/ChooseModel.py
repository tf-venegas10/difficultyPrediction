from sklearn.ensemble import RandomForestRegressor
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing
from GetDataSet import getDataSet
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier


X,Y,X_test,Y_test= getDataSet()
sm = SMOTE()
x, y = sm.fit_sample(X, Y)
x_norm=preprocessing.normalize(x,"l1")

forest= RandomForestClassifier(n_estimators=100, max_depth=20, random_state=111)
forest.fit(x_norm,y)

x_test_norm=preprocessing.normalize(X_test,"l2")
print(forest.score(x_test_norm,y))
