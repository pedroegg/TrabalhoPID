import cv2.cv2 as cv2
import numpy as np
import os
import glob
import mahotas as mt
from sklearn.svm import LinearSVC
import time

# function to extract haralick textures from an image
def extract_features(image):
    # calculate haralick texture features for 4 types of adjacency
    textures = mt.features.haralick(image)

    # take the mean of it and return it
    ht_mean  = textures.mean(axis=0)
    return ht_mean


def train(train_path):

    # load the training dataset
    train_names = os.listdir(train_path)

    # empty list to hold feature vectors and train labels
    train_features = []
    train_labels   = []

    # loop over the training dataset
    print("[STATUS] Started extracting haralick textures..")

    temp_ini = time.time()
    
    for train_name in train_names:
        cur_path = train_path + "/" + train_name
        cur_label = train_name
        i = 1

        for file in glob.glob(cur_path + "/*.png"):
            print("Processing Image - {} in {}".format(i, cur_label))
            # read the training image
            image = cv2.imread(file)

            # convert the image to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # extract haralick texture from the image
            features = extract_features(gray)

            # append the feature vector and label
            train_features.append(features)
            train_labels.append(cur_label)

            # show loop update
            i += 1

    # have a look at the size of our feature vector and labels
    print("Training features: {}".format(np.array(train_features).shape))
    print("Training labels: {}".format(np.array(train_labels).shape))

    # create the classifier
    print( "[STATUS] Creating the classifier..")
    clf_svm = LinearSVC(random_state=9)

    # fit the training data and labels
    print( "[STATUS] Fitting data/label to model..")
    clf_svm.fit(train_features, train_labels)

    temp_fim = time.time()
    
    return clf_svm, round(temp_fim - temp_ini, 2)


def classify(file, clf_svm):
    image = cv2.imread(file)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    features = extract_features(gray)

    temp_ini = time.time()
    prediction = clf_svm.predict(features.reshape(1, -1))[0]
    temp_fim = time.time()

    cv2.putText(image, prediction, (20,30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,128,128), 3)

    cv2.imshow("Test_Image", image)

    cv2.waitKey(5000)
    
    return prediction, round(temp_fim - temp_ini, 2)