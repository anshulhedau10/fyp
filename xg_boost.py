import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import roc_curve, auc, confusion_matrix, classification_report, accuracy_score
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

# Results
print("Results:\n")

model = XGBClassifier(use_label_encoder=False)
model.fit(x_train, y_train)
y_pred = model.predict(x_test)

false_positive_rate, true_positive_rate, thresholds = roc_curve(y_test, y_pred)
roc_auc = auc(false_positive_rate, true_positive_rate)
roc_auc = round(roc_auc, 4)
print("XGB Model's ROC AUC value : ", roc_auc)
report = classification_report(y_test, y_pred)
print(report)
cnf_matrix = confusion_matrix(y_test, y_pred)
print(cnf_matrix)
accuracy = accuracy_score(y_test, y_pred)
accuracy = round(accuracy, 4)

# Save ROC curve image
plt.title('XGB ROC Curve')
plt.plot(false_positive_rate, true_positive_rate, 'b', label = 'AUC = %0.2f' % roc_auc)
plt.legend(loc = 'lower right')
plt.plot([0, 1], [0, 1],'r--')
plt.xlim([0, 1])
plt.ylim([0, 1])
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')
plt.savefig((base_path/"../static/images/ROC_Curve_XGB.png").resolve(), dpi=100, pad_inches=0.5, bbox_inches="tight")
plt.clf()

# Saving confusion matrix
sns.heatmap(cnf_matrix/np.sum(cnf_matrix), annot=True, fmt='.2%', cmap='Blues').set_title("XGB Confusion Matrix").figure.savefig((base_path/"../static/images/Confusion_Matrix_XGB.png").resolve(), dpi=100)

# Saving ML model and result
pickle.dump(model, open((base_path/"../pickle_global/xgb_model.pkl").resolve(),'wb'))
pickle.dump(roc_auc, open((base_path/"../pickle_global/xgb_roc_auc.pkl").resolve(),'wb'))
pickle.dump(cnf_matrix, open((base_path/"../pickle_global/xgb_cnf_matrix.pkl").resolve(),'wb'))
pickle.dump(report, open((base_path/"../pickle_global/xgb_report.pkl").resolve(),'wb'))
pickle.dump(accuracy, open((base_path/"../pickle_global/xgb_accuracy.pkl").resolve(),'wb'))