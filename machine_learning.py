#verzija sa svim modelima zajedno
import csv
import random
import datetime
import matplotlib.pyplot as plt
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn import preprocessing
from sklearn import linear_model
from read_file import *

random.seed(10)
startTime=datetime.datetime.now()
print ("Proccess start: %s" %(startTime))
features=[]
values=[]
labels=[]

make_dateset()
tempArr = dataset

random.shuffle(tempArr)
print "Shuffle complete"
l = len(tempArr[0])
for row in tempArr:
    features.append(row[:l-1])
    labels.append(int(row[l-1]))

features=preprocessing.scale(features)
print "Preprocessing done"

trainingFeatures, testFeatures, trainingLabels, testLabels = train_test_split(features, labels, test_size = 0.2) 

testFeatures=preprocessing.scale(testFeatures)

print "Datasets generated"

models=[]
results=[]
names=[]
models.append(('SVM', SVC()))
#models.append(('LSS', linear_model.Lasso(alpha=0.1, copy_X=True, fit_intercept=True, max_iter=1000,normalize=True, positive=False, precompute=False, random_state=None,selection='cyclic', tol=0.0001, warm_start=False)))
#models.append(('LDA', LinearDiscriminantAnalysis()))
models.append(('KNN', KNeighborsClassifier()))
models.append(('CART', DecisionTreeClassifier()))
models.append(('NB', GaussianNB()))
#models.append(('SGD', linear_model.SGDClassifier()))
print "Models loaded"
predLabels=[]
for name,model in models:
    model.fit(trainingFeatures,trainingLabels)
    '''if (name=='LSS'):
        print(model.coef_)'''
    #predLabel=model.predict(testFeatures) 
    #predLabels.append(predLabel)
    result=model.score(testFeatures,testLabels)
    results.append(result)
    names.append(name)
    print (">Prediction with %s method complete with %f (%f)" %(name, result.mean(),result.std()))

endTime=datetime.datetime.now()
print ("Proccess end: %s" %(endTime))