#!/usr/bin/env python
# coding: utf-8

## Importing Libraries

import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
from pathlib import Path

def machinelearning():

    print("Python script in progress..")
    base_path = Path(__file__)
    dataset = pd.read_csv((base_path/"../static/dataset/covid_refined.csv").resolve()) #Reading covid_refined csv file (The model is trained with this file)
    dataset = pd.concat([dataset], ignore_index=True)

    ## Extracting x and y

    # y = dependent variable / target variable
    # x = independent variables
    id_1 = dataset.pop("id")
    y = dataset.pop("high_risk")
    x = dataset
    x = pd.DataFrame(x)
    x = pd.concat([x], ignore_index=True)
    #x.head(10)

    y = y.astype('int64')
    #y.head(10)

    ## Splitting x and y into training and test set

    from sklearn.model_selection import train_test_split
    x_train, x_test, y_train, y_test = train_test_split(x, y, random_state = 42, test_size = 0.2)

    ## Creating and Training ML model

    print("Training the model..")
    from sklearn.ensemble import RandomForestClassifier
    rf = RandomForestClassifier(n_estimators = 100, random_state = 100, bootstrap = True)
    rf.fit(x_train, y_train)

    y_pred = rf.predict(x_test)
    #print(y_pred)

    from sklearn.metrics import roc_curve, auc, accuracy_score
    false_positive_rate, true_positive_rate, thresholds = roc_curve(y_test, y_pred)
    roc_auc = auc(false_positive_rate, true_positive_rate)
    print("Model's AUC value : ", roc_auc)
    print("Model's Accuracy Score is : ", accuracy_score(y_test, y_pred))

    # Printing importance of features
    feature_list = list(x.columns)
    feature_imp = pd.Series(rf.feature_importances_, index = feature_list).sort_values(ascending = False)
    print("Feature importance: \n",feature_imp)

    ## Predicting for the input dataset and Adding information in result

    input_data = pd.read_csv((base_path/"../static/dataset/input_data.csv").resolve())
    id_patient = input_data.pop("id")
    email_patient = input_data.pop("email")
    name_patient = input_data.pop("name")
    #input_data.head(10)

    print("Predicting for input data..")
    pred = rf.predict(input_data)
    pred = pd.DataFrame(pred, columns = ["high_risk"])
    pred.loc[pred["high_risk"] == 0, "high_risk"] = "NO"
    pred.loc[pred["high_risk"] == 1, "high_risk"] = "YES"
    #pred.head(10)

    result = pd.concat([id_patient, name_patient, email_patient, pred], axis=1, join="outer") #joining id, email, prediction
    #result.head(20)

    ## Exporting result

    result.to_csv((base_path/"../static/dataset/result.csv").resolve(), encoding='utf-8', index=False)
    print("Result generated")

    ## Exporting list of emails for email sending
    to_send_email = result[result.high_risk== "YES"] #list of emails of patients with high_risk=="YES"

    to_send_email_list = to_send_email["email"].tolist() #extracting email list
    name_list = to_send_email["name"].tolist() #extracting name list

    #adding patient's name with their email
    for i in range(len(to_send_email_list)):
        to_send_email_list[i] = [to_send_email_list[i], name_list[i]] #format: [['email', 'name'], ... ]

    return to_send_email_list
