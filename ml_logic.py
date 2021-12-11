#!/usr/bin/env python
# coding: utf-8

## Importing Libraries

import pickle
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
#import numpy as np
import pandas as pd
from pathlib import Path
import seaborn as sns
import os


def machinelearning():

    print("Python script in progress..")
    base_path = Path(__file__)

    # Loading random forest model
    rf = pickle.load(open((base_path/"../pickle_global/rf_model.pkl").resolve(),'rb'))

    # Loading global variables
    selected_feat = pickle.load(open((base_path/"../pickle_global/selected_feat.pkl").resolve(),'rb'))

    # Loading input data
    input_data = pd.read_csv((base_path/"../static/dataset/input_data.csv").resolve())

    input_data1 = input_data.copy(deep=True)
    id_patient = input_data.pop("id")
    email_patient = input_data.pop("email")
    name_patient = input_data.pop("name")

    # Prediction
    print("Predicting for input data..")

    # Selecting important features
    input_data = input_data[selected_feat]
    pred = rf.predict(input_data)

    # Changing 0 to NO, 1 to YES
    pred = pd.DataFrame(pred, columns = ["high_risk"])
    pred.loc[pred["high_risk"] == 0, "high_risk"] = "NO"
    pred.loc[pred["high_risk"] == 1, "high_risk"] = "YES"



    # Merging id, name, email with y_pred
    result = pd.concat([id_patient, name_patient, email_patient, pred], axis=1, join="outer")

    # Exporting result
    result.to_csv((base_path/"../static/dataset/result.csv").resolve(), encoding='utf-8', index=False)
    print("Result generated")

    ## Exporting list of emails for email sending
    to_send_email = result[result.high_risk== "YES"] #list of emails of patients with high_risk=="YES"

    to_send_email_list = to_send_email["email"].tolist() #extracting email list
    name_list = to_send_email["name"].tolist() #extracting name list

    # Adding patient's name with their email
    for i in range(len(to_send_email_list)):
        to_send_email_list[i] = [to_send_email_list[i], name_list[i]] #format: [['email', 'name'], ... ]

    # Generating graph for individual patients with high_risk=="YES"
    for em, risk, nm in zip(result["email"], result["high_risk"], result["name"]):
        if(risk=="YES"):
            p = input_data1.loc[input_data1["email"]==em]
            p = p[['intubed', 'pneumonia', 'diabetes', 'copd', 'asthma', 'hypertension', 'other_disease', 'cardiovascular', 'obesity', 'renal_chronic', 'tobacco', 'covid_res']]
            long_p = pd.melt(p)
            plt.figure(figsize=(9,6))
            sns.barplot(y = long_p.variable, x = long_p.value, palette="hls").set_title(nm+" - Affecting factors for severe COVID-19").figure.savefig(os.path.join("static/images/graphs/"+str(em)+".png"), dpi=100)

    return to_send_email_list
