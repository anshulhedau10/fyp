#!/usr/bin/env python
# coding: utf-8

## Importing Libraries

import pickle
import matplotlib
from numpy import true_divide
matplotlib.use('Agg')
import matplotlib.pyplot as plt
#import numpy as np
import pandas as pd
from pathlib import Path
import seaborn as sns
import os
from flask import request

base_path = Path(__file__)

# Generate result file and patient report
def dataProcess(input_data):
    # Loading XG Boost model
    xgb = pickle.load(open((base_path/"../pickle_global/xgb_model.pkl").resolve(),'rb'))

    # Loading feature selected variables
    # selected_feat = pickle.load(open((base_path/"../pickle_global/selected_feat.pkl").resolve(),'rb'))

    input_data1 = input_data.copy(deep=True)
    id_patient = input_data.pop("id")
    email_patient = input_data.pop("email")
    name_patient = input_data.pop("name")

    # Prediction
    print("Predicting for input data..", flush=True)

    # Selecting important features
    # input_data = input_data[selected_feat]
    pred = xgb.predict(input_data)

    # Changing 0 to NO, 1 to YES
    pred = pd.DataFrame(pred, columns = ["high_risk"])
    pred.loc[pred["high_risk"] == 0, "high_risk"] = "NO"
    pred.loc[pred["high_risk"] == 1, "high_risk"] = "YES"

    # Merging id, name, email with y_pred
    result = pd.concat([id_patient, name_patient, email_patient, pred], axis=1, join="outer")

    # Exporting result
    result.to_csv((base_path/"../static/dataset/result.csv").resolve(), encoding='utf-8', index=False)
    print("Result generated", flush=True)

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
            plt.close('all')
            
    print(to_send_email_list, flush=True)
    return to_send_email_list 


# Logic for Multiple people result generation
def machinelearning1():
    print("Python script in progress..", flush=True)

    # Loading input data
    input_data = pd.read_csv((base_path/"../static/dataset/input_data.csv").resolve())
    
    return dataProcess(input_data)


# Logic for Individual people result generation
def machinelearning2():
    print("Python script in progress..", flush=True)
    userIndividualData = {}

    # Getting data from the form
    userIndividualData['userId'] = str(request.form['userId'])
    userIndividualData['userName'] = str(request.form['userName'])
    userIndividualData['userEmail'] = str(request.form['userEmail'])
    userIndividualData['userSex'] = str(request.form['userSex'])
    userIndividualData['userAgeGrp'] = str(request.form['userAgeGrp'])

    userIndividualData['intubed'] = str(request.form.get('intubed'))
    userIndividualData['pneumonia'] = str(request.form.get('pneumonia'))
    userIndividualData['diabetes'] = str(request.form.get('diabetes'))
    userIndividualData['copd'] = str(request.form.get('copd'))
    userIndividualData['asthma'] = str(request.form.get('asthma'))
    userIndividualData['hypertension'] = str(request.form.get('hypertension'))
    userIndividualData['cardiovascular'] = str(request.form.get('cardiovascular'))
    userIndividualData['obesity'] = str(request.form.get('obesity'))
    userIndividualData['renalChronic'] = str(request.form.get('renalChronic'))
    userIndividualData['tobacco'] = str(request.form.get('tobacco'))
    userIndividualData['covidRes'] = str(request.form.get('covidRes'))
    userIndividualData['otherDisease'] = str(request.form.get('otherDisease'))

    for key in userIndividualData:
        if key not in ['userId', 'userName', 'userEmail', 'userSex', 'userAgeGrp']:
            if userIndividualData[key] == 'None':
                userIndividualData[key] = 0
            elif userIndividualData[key] == 'on':
                userIndividualData[key] = 1
    
    df1 = pd.read_csv((base_path/"../static/dataset/input_data_individual_template.csv").resolve())

    df2 = pd.DataFrame({'id': [userIndividualData['userId']],
    'name': userIndividualData['userName'],
    'email': userIndividualData['userEmail'],
    'sex': userIndividualData['userSex'],
    'age_group': userIndividualData['userAgeGrp'],
    'intubed': userIndividualData['intubed'],
    'pneumonia': userIndividualData['pneumonia'],
    'diabetes': userIndividualData['diabetes'],
    'copd': userIndividualData['copd'],
    'asthma': userIndividualData['asthma'],
    'hypertension': userIndividualData['hypertension'],
    'other_disease': userIndividualData['otherDisease'],
    'cardiovascular': userIndividualData['cardiovascular'],
    'obesity': userIndividualData['obesity'],
    'renal_chronic': userIndividualData['renalChronic'],
    'tobacco': userIndividualData['tobacco'],
    'covid_res': userIndividualData['covidRes']})

    # Generating csv input file
    dff = df1.append(df2, ignore_index=True)
    dff.to_csv((base_path/"../static/dataset/input_data_individual.csv").resolve(), encoding='utf-8', index=False)
    print("Individual file saved successfully..", flush=True)

    input_data = pd.read_csv((base_path/"../static/dataset/input_data_individual.csv").resolve())

    return dataProcess(input_data)
