import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_curve, auc, confusion_matrix, classification_report, accuracy_score
from imblearn.over_sampling import SMOTE
from sklearn.feature_selection import SelectFromModel
import seaborn as sns
from pathlib import Path

base_path = Path(__file__)
dataset = pd.read_csv((base_path/"../static/dataset/covid_refined.csv").resolve()) #Reading covid_refined csv file (The model is trained with this file)
dataset.drop('id', inplace=True, axis=1)

# Extracting x and y
# y = dependent variable / target variable
# x = independent variables
y = dataset.pop("high_risk")
x = dataset

y = y.astype('int64')

# Splitting x and y into training and test set
x_train, x_test, y_train, y_test = train_test_split(x, y, random_state = 42, test_size = 0.20)

# SMOTE oversampling method to solve the imbalance problem
x_train_oversampled, y_train_oversampled = SMOTE().fit_resample(x_train, y_train)

# Creating and training ML model
rf = RandomForestClassifier(n_estimators = 100, random_state = 42, bootstrap = True)
rf.fit(x_train_oversampled, y_train_oversampled)

# Prediction
y_pred = rf.predict(x_test)

# Results before
false_positive_rate, true_positive_rate, thresholds = roc_curve(y_test, y_pred)
roc_auc = auc(false_positive_rate, true_positive_rate)
roc_auc = round(roc_auc, 4)
print("Model's ROC AUC value : ", roc_auc)
print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))

feature_imp = pd.Series(rf.feature_importances_,index=x.columns).sort_values(ascending=False)

# Fetaure selection
sel = SelectFromModel(rf, threshold=0.04)
sel.fit(x_train_oversampled, y_train_oversampled)
selected_feat= x_train_oversampled.columns[(sel.get_support())]
x_train_imp = x_train_oversampled[selected_feat]
x_test_imp = x_test[selected_feat]

# Results after
rf_imp = RandomForestClassifier(n_estimators = 100, random_state = 42, bootstrap = True)
rf_imp.fit(x_train_imp, y_train_oversampled)
y_pred = rf_imp.predict(x_test_imp)
false_positive_rate, true_positive_rate, thresholds = roc_curve(y_test, y_pred)
roc_auc = auc(false_positive_rate, true_positive_rate)
roc_auc = round(roc_auc, 4)
print("Model's ROC AUC value : ", roc_auc)
report = classification_report(y_test, y_pred)
print(report)
cnf_matrix = confusion_matrix(y_test, y_pred)
print(cnf_matrix)
accuracy = accuracy_score(y_test, y_pred)
accuracy = round(accuracy, 4)

# Save ROC curve image
plt.title('ROC Curve')
plt.plot(false_positive_rate, true_positive_rate, 'b', label = 'AUC = %0.2f' % roc_auc)
plt.legend(loc = 'lower right')
plt.plot([0, 1], [0, 1],'r--')
plt.xlim([0, 1])
plt.ylim([0, 1])
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')
plt.savefig((base_path/"../static/images/roc_curve.png").resolve(), dpi=100, pad_inches=0.5, bbox_inches="tight")
plt.clf()

# Saving confusion matrix
sns.heatmap(cnf_matrix/np.sum(cnf_matrix), annot=True, fmt='.2%', cmap='Blues').set_title("Confusion Matrix").figure.savefig((base_path/"../static/images/confusionmatrix.png").resolve(), dpi=100)

# Saving ML model and result
pickle.dump(rf_imp, open((base_path/"../pickle_global/rf_model.pkl").resolve(),'wb'))
pickle.dump(selected_feat, open((base_path/"../pickle_global/selected_feat.pkl").resolve(),'wb'))
pickle.dump(roc_auc, open((base_path/"../pickle_global/roc_auc.pkl").resolve(),'wb'))
pickle.dump(cnf_matrix, open((base_path/"../pickle_global/cnf_matrix.pkl").resolve(),'wb'))
pickle.dump(report, open((base_path/"../pickle_global/report.pkl").resolve(),'wb'))
pickle.dump(accuracy, open((base_path/"../pickle_global/accuracy.pkl").resolve(),'wb'))