#!/usr/bin/env python
# coding: utf-8

# # Importing Libraries

# In[1]:
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# In[3]:
print("Python script in progress..")
base_path = Path(__file__)
dataset = pd.read_csv((base_path/"../static/dataset/covid_new.csv").resolve())
dataset = pd.concat([dataset], ignore_index=True)

# In[4]:
#dataset.shape

# # EDA (Exploratory Data Analysis)

# In[5]:
print("Processing the data..")
# dropping unwanted columns
dataset.drop('date_symptoms', inplace=True, axis=1)
dataset.drop('inmsupr', inplace=True, axis=1)
dataset.drop('covid_res', inplace=True, axis=1)
dataset.drop('patient_type', inplace=True, axis=1)
dataset.drop('entry_date', inplace=True, axis=1)
dataset.drop('other_disease', inplace=True, axis=1)
dataset.drop('contact_other_covid', inplace=True, axis=1)
dataset.drop('icu', inplace=True, axis=1)
try:
    dataset.drop('Unnamed: 0', inplace=True, axis=1)
except:
    print("Unnamed column does not exist.")

# In[6]:
# printing dataset
# print(dataset.shape)
# dataset.head(10)

# In[7]:
# checking null values
#print(dataset.isna().sum())

# ## Checking types of values in all columns

# In[8]:
#female - 1
#male - 2
#print('sex')
#print(dataset['sex'].value_counts())

# In[9]:
#Died - actual date
#Alive - 9999-99-99
#print('date_died')
#print(dataset['date_died'].value_counts())

# In[10]:
#Yes - 1
#No - 2
#print('intubed')
#print(dataset['intubed'].value_counts())

# In[11]:
#Yes - 1
#No - 2
#print('pneumonia')
#print(dataset['pneumonia'].value_counts())

# In[12]:
#Yes - 1
#No - 2
#print('pregnancy')
#print(dataset['pregnancy'].value_counts())

# In[13]:
#Yes - 1
#No - 2
#print('diabetes')
#print(dataset['diabetes'].value_counts())

# In[14]:
#Yes - 1
#No - 2
#print('copd')
#print(dataset['copd'].value_counts())

# In[15]:
#Yes - 1
#No - 2
#print('asthma')
#print(dataset['asthma'].value_counts())

# In[16]:
#Yes - 1
#No - 2
#print('hypertension')
#print(dataset['hypertension'].value_counts())

# In[17]:
#Yes - 1
#No - 2
#print('cardiovascular')
#print(dataset['cardiovascular'].value_counts())

# In[18]:
#Yes - 1
#No - 2
#print('obesity')
#print(dataset['obesity'].value_counts())

# In[19]:
#Yes - 1
#No - 2
#print('renal_chronic')
#print(dataset['renal_chronic'].value_counts())

# In[20]:
#Yes - 1
#No - 2
#print('tobacco')
#print(dataset['tobacco'].value_counts())

# ## Checking outliers

# In[21]:
#print('Age Mean and Median :')
#print(dataset['age'].mean())
#print(dataset['age'].median())

# # Data Preprocessing

# In[22]:
#removing null values
print("Cleaning the data..")
dataset = dataset[dataset.intubed != 99]
dataset = dataset[dataset.intubed != 97]
dataset = dataset[dataset.pneumonia != 99]
dataset = dataset[dataset.pregnancy != 98]
dataset = dataset[dataset.pregnancy != 97]
dataset = dataset[dataset.diabetes != 98]
dataset = dataset[dataset.copd != 98]
dataset = dataset[dataset.asthma != 98]
dataset = dataset[dataset.hypertension != 98]
dataset = dataset[dataset.cardiovascular	 != 98]
dataset = dataset[dataset.obesity != 98]
dataset = dataset[dataset.renal_chronic != 98]
dataset = dataset[dataset.tobacco != 98]
dataset = dataset.dropna()

# In[23]:
# renaming date_died column and replacing the values
dataset.rename({'date_died': 'high_risk'}, axis=1, inplace=True)
dataset.loc[dataset["high_risk"] == "9999-99-99", "high_risk"] = 0
dataset.loc[dataset["high_risk"] != 0, "high_risk"] = 1

#print(dataset.shape)
#dataset.head(10)

# In[24]:
#Yes - 1
#No - 2
#print('high_risk')
#print(dataset['high_risk'].value_counts())

# In[25]:
# saving usable dataset csv
#dataset.to_csv('F:/Anshul/FYP/Dataset/covid_refined.csv', encoding='utf-8', index=False)

# ## Rearranging dataset

# In[26]:
cols = dataset.columns.tolist()
cols = cols[0:2]+cols[3:]+[cols[2]]
dataset = dataset[cols]
#dataset.head(10)

# In[27]:
# checking datatypes of each column
#print(dataset.dtypes)

# ## Extracting x and y

# In[28]:
# y = dependent variable / target variable
# x = independent variables
id_1 = dataset.pop("id")
email = dataset.pop("email")
y = dataset.pop("high_risk")
x = dataset
x = pd.DataFrame(x)
x = pd.concat([x], ignore_index=True)

# In[29]:
#x.head(10)

# In[30]:
y = y.astype('int64')
#y.head(10)

# ## Splitting x and y into training and test set

# In[31]:
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, random_state = 42, test_size = 0.25)

# ## Creating and training ML model

# In[32]:
print("Training the model..")
from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier(n_estimators = 100, random_state = 100, bootstrap = True)
rf.fit(x_train, y_train)

# In[33]:
y_pred = rf.predict(x_test)
#print(y_pred)

# In[34]:
from sklearn.metrics import roc_curve, auc, accuracy_score
false_positive_rate, true_positive_rate, thresholds = roc_curve(y_test, y_pred)
roc_auc = auc(false_positive_rate, true_positive_rate)
print("Model's AUC value : ", roc_auc)
print("Model's Accuracy Score is : ", accuracy_score(y_test, y_pred))

# In[35]:
# printing importance of features
feature_list = list(x.columns)
feature_imp = pd.Series(rf.feature_importances_, index = feature_list).sort_values(ascending = False)
print("Feature importance: \n",feature_imp)

# In[36]:
'''
n_estimators = [1, 2, 4, 8, 15, 25, 50, 100, 200]
train_results = []
test_results = []

for estimator in n_estimators:
    rf_ = RandomForestClassifier(n_estimators = estimator, random_state = 100, n_jobs = -1, bootstrap = True)
    rf_.fit(x_train, y_train)
    train_pred = rf_.predict(x_train)
    false_positive_rate_, true_positive_rate_, thresholds = roc_curve(y_train, train_pred)
    roc_auc_ = auc(false_positive_rate_, true_positive_rate_)
    train_results.append(roc_auc_)
    y_pred_ = rf_.predict(x_test)
    false_positive_rate_, true_positive_rate_, thresholds = roc_curve(y_test, y_pred_)
    roc_auc_ = auc(false_positive_rate_, true_positive_rate_)
    test_results.append(roc_auc_)

print(train_results)
print(test_results)
    
from matplotlib.legend_handler import HandlerLine2D
line1, = plt.plot(n_estimators, train_results, "b", label = "Train AUC")
line2, = plt.plot(n_estimators, test_results, "r", label = "Test AUC")
plt.legend(handler_map = {line1: HandlerLine2D(numpoints = 2)})
plt.ylabel("AUC Score")
plt.xlabel("n_estimators")
plt.show()
'''

# # Predicting for the input dataset and Adding information in result

# In[37]:
input_data = pd.read_csv((base_path/"../static/dataset/input_data.csv").resolve())
id_patient = input_data.pop("id")
email_patient = input_data.pop("email")

#input_data.head(10)

# In[38]:
print("Predicting for input data..")
pred = rf.predict(input_data)
print("Accuracy Score is : ", accuracy_score(y, pred))

pred = pd.DataFrame(pred, columns = ["high_risk"])
pred.loc[pred["high_risk"] == 0, "high_risk"] = "NO"
pred.loc[pred["high_risk"] == 1, "high_risk"] = "YES"
pred.head(10)

# In[39]:
result = pd.concat([id_patient, email_patient, pred], axis=1, join="outer")

# In[40]:
#result.head(20)

# # Exporting result

# In[41]:
result.to_csv((base_path/"../static/dataset/result.csv").resolve(), encoding='utf-8', index=False)
