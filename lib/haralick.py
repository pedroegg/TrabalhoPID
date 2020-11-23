import cv2.cv2 as cv2
import numpy as np
import os
import glob
import mahotas as mt
from sklearn.svm import LinearSVC
from sklearn.metrics import confusion_matrix
from sklearn.metrics import homogeneity_score
import time
import random

def convert(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if not (len(image.shape) == 2) else image

# function to extract haralick textures from an image
def extract_features(image, selected_caracteristics):
    # convert the image to grayscale
    gray = convert(image)
    gray = gray // 8
    
    # calculate haralick texture features for 4 types of adjacency
    textures = mt.features.haralick(gray)

     # take the mean of it and return it
    ht_mean = textures.mean(axis=0)
    
    new_textures = []
    for position in selected_caracteristics:
        new_textures.append(ht_mean[position])

    new_textures = np.array(new_textures)

    return new_textures

def separate_images(imagesByPath):
    images_files = []

    for path in imagesByPath:
        tam_dir_train = len(imagesByPath[path])
        for _ in range(int(tam_dir_train*0.25)):
            image_file = random.choice(imagesByPath[path])
            images_files.append(image_file)
            imagesByPath[path].remove(image_file)

    return images_files

def test(test_array, clf_svm, selected_caracteristics):
    hits = 0
    misses = 0

    y_true = []
    y_pred = []

    time_init = time.time()

    for file_obj in test_array:
        y_true.append(int(file_obj['BIRADS']))
        answer, _ = classify(file_obj, clf_svm, True, selected_caracteristics)
        y_pred.append(int(answer))
        
        if int(answer) == int(file_obj['BIRADS']):
            hits += 1
        else:
            misses += 1

    time_end = time.time()
    
    hits_percentage = hits/len(test_array) * 100

    especificity = 1 - (misses/hits+misses) / 300

    homogeneity = homogeneity_score(y_true, y_pred)

    matrix = confusion_matrix(y_true, y_pred, labels=[1, 2, 3, 4])

    return round(hits_percentage, 2), round(time_end - time_init, 2), matrix, round(especificity, 2), round(homogeneity, 2)

def train(imagesByPath, selected_caracteristics):
    # empty list to hold feature vectors and train labels
    train_features = []
    train_labels   = []

    # loop over the training dataset
    print("[STATUS] Started extracting haralick textures..")

    temp_ini = time.time()
    
    test_images = separate_images(imagesByPath)

    for path in imagesByPath:
        print("Path atual = {}".format(path))
        for image in imagesByPath[path]:
            filename_parts = image['filename'].split('/')
            print("Processing Image {} with BIRADS {}".format(filename_parts[len(filename_parts)-1], image['BIRADS']))

            # extract haralick texture from the image
            features = extract_features(image['image'], selected_caracteristics)

            # append the feature vector and label
            train_features.append(features)
            train_labels.append(path)

    # have a look at the size of our feature vector and labels
    print("Training features: {}".format(np.array(train_features).shape))
    print("Training labels: {}".format(np.array(train_labels).shape))

    # create the classifier
    print( "[STATUS] Creating the classifier..")
    clf_svm = LinearSVC()

    # fit the training data and labels
    print( "[STATUS] Fitting data/label to model..")
    clf_svm.fit(train_features, train_labels)

    temp_fim = time.time()

    print('Testing...')

    hits_percentage, time_took, matrix, especificity, homogeneity = test(test_images, clf_svm, selected_caracteristics)

    print('Test finished!')
    
    return clf_svm, round(temp_fim - temp_ini, 2), hits_percentage, time_took, matrix, especificity, homogeneity

def classify(file, clf_svm, isTest, selected_caracteristics):
    if isTest:
        image = file['image']
    else:
        image = cv2.imread(file)

    features = extract_features(image, selected_caracteristics)

    temp_ini = time.time()
    prediction = clf_svm.predict(features.reshape(1, -1))[0]
    temp_fim = time.time()

    if not isTest:
        cv2.putText(image, prediction, (20,30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,128,128), 3)
        cv2.imshow("Image", image)
        cv2.waitKey(0)
        cv2.destroyWindow("Image")
    
    return prediction, round(temp_fim - temp_ini, 7)