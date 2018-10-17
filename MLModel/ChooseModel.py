from sklearn.ensemble import RandomForestRegressor
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing
from GetDataSet import getDataSet
from imblearn.over_sampling import SMOTE


X,Y= getDataSet()
sm = SMOTE()
x, y = sm.fit_sample(X, Y)
x_norm=preprocessing.normalize(x,"l1")
print(x_norm)
