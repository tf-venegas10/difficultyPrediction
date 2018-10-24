
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
features = [[1,2,3,4,5,6,7,44],[x for x in xrange(8,15)],[31,32,33,34,45,50],[c for c in xrange(35,44)]]

            # sound features are too many  , [x for x in xrange(51,84)]]
features_domain=["speech","display_text", "relation", "visual_aesthetic"]
            #, "sound"]

for set_number in xrange(len(features)):
    set = features[set_number]
    n = len(set)
    size = pow(2,n)
    # Vars to select the best suited model
    bestModel = None
    bestName = "none"
    bestMean = 0.0
    bestSet = []
    for ii in xrange(size):
        subset = []
        for jj in xrange(n):
            if (ii & (1 << jj)) > 0:
                subset.append(set[jj])
        print subset
        if (len(subset)>0):
            X,y,X_test,Y_test= getDataSubSet(subset)
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
                bestSet = subset


    print("###################%s########################"%features_domain[set_number])
    print("The best model is: %s with and average accuracy of: %0.5f"%(bestName,bestMean))
    print("And with the set of features:")
    print (subset)
    print("###########")
