from sklearn.ensemble import RandomForestRegressor
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing
from GetDataSet import getDataSet
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier


X,Y= getDataSet()
sm = SMOTE()
x, y = sm.fit_sample(X, Y)
x_norm=preprocessing.normalize(x,"l1")

forest= RandomForestClassifier(n_estimators=100, max_depth=20, random_state=111)
forest.fit(x_norm,y)
print(forest.score(x,y))
