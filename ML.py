from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn import metrics
import joblib

f = open('out.csv', mode='r')
data = f.read().split('\n')[1:]
f.close()

features = []
labels = []

def train():
    for x in data:
        x = x.split(',')
        # print(x)
        features.append([float(x[0]), float(x[1])])
        labels.append(int(x[2]))

    # === test accuracy ===
    train_X, test_X, train_y, test_y = train_test_split(features, labels, test_size = 0.2)
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(train_X, train_y)

    test_y_predicted = clf.predict(test_X)
    accuracy = metrics.accuracy_score(test_y, test_y_predicted)
    print(accuracy)
    # =======================

    clf = clf.fit(features, labels)
    joblib.dump(clf, 'model.pkl') # save model

def getSatelliteDistance(degree):
    import math
    a = 1
    b = -12734*math.cos(math.radians(90 + degree))
    c = -665266800

    return (-b + math.sqrt(b**2 - 4*a*c)) / (2*a)

def isCovered(sData):
    degree = int(sData[1])
    SNR = int(sData[3])
    distance = getSatelliteDistance(degree)

    sData = [[distance, SNR]]
    clf = joblib.load('./model.pkl') # load model
    wantPredict = clf.predict(sData)

    # print(wantPredict)
    if wantPredict == [1]:
        # print('Covered by buildings.')
        return True
    elif wantPredict == [0]:
        # print('Not Covered by buildings.')
        return False

train()
isCovered(['02', '65', '064', '18']) 