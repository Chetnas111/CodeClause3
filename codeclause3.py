# -*- coding: utf-8 -*-
"""CodeClause3.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1vH3Cjv55uoAkNN6wjRo_CMm3yhzgwnjX

#Project Title - Parkinson's Disease Detection
--Internship Domain - Data Science Intern
#Project Level - Golden Level
"""

# Aim -
# Create a UI where users can input relevant parameters, and the system predicts the
# likelihood of Parkinson's disease using a machine learning model.
# DescriptionDesign a user-friendly interface allowing users to input features like tremors, voice
# recordings, etc., for accurate disease detection.
# TechnologiesPython, Flask/Django for UI, Machine Learning for Parkinson's prediction
# You can use other technologies that you know.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

df=pd.read_csv("/content/parkinsons.data")

df

df.info()

"""-- It can be observed that the column Status is stored as int64 datatype. However, since the column contains only two numeric values 0 & 1, we will be change the datatype to uint8."""

df['status'] = df['status'].astype('uint8')

df.info()

df.describe()

df.shape

df.columns

df.isnull().sum()

#The dataset does not contain any Duplicated Rows
df.duplicated().sum()

print('Number of Features In Dataset :', df.shape[1])
print('Number of Instances In Dataset : ', df.shape[0])

# Dropping The Name Column
df.drop(['name'], axis=1, inplace=True)

print('Number of Features In Dataset :', df.shape[1])
print('Number of Instances In Dataset : ', df.shape[0])

#Balance of Data
sns.countplot(x='status',data=df)

plt.figure(figsize=(12, 10))
sns.heatmap(df.corr(), annot=True, cmap='viridis', fmt=".2f")
plt.title("Correlation Matrix of Parkinson's Disease Features")
plt.show()

# Example of visualizing the distribution of a single feature
plt.figure(figsize=(8, 6))
sns.histplot(df['MDVP:Fo(Hz)'], kde=True) # Replace 'MDVP:Fo(Hz)' with any other feature you want to visualize
plt.title("Distribution of MDVP:Fo(Hz)")
plt.xlabel("MDVP:Fo(Hz)")
plt.ylabel("Frequency")
plt.show()

# Example of visualizing the relationship between two features
plt.figure(figsize=(8, 6))
sns.scatterplot(x='MDVP:Fo(Hz)', y='HNR', hue='status', data=df) # Example: MDVP:Fo(Hz) vs HNR colored by status
plt.title("MDVP:Fo(Hz) vs HNR")
plt.xlabel("MDVP:Fo(Hz)")
plt.ylabel("HNR")
plt.show()

# Example of a boxplot to show the distribution of a feature for different status values
plt.figure(figsize=(8,6))
sns.boxplot(x='status', y='MDVP:Fo(Hz)', data=df) # Example: MDVP:Fo(Hz) grouped by status
plt.title("MDVP:Fo(Hz) Distribution by Status")
plt.show()

#Box Plot
fig,axes=plt.subplots(5,5,figsize=(15,15))
axes=axes.flatten()

for i in range(1,len(df.columns)-1):
    sns.boxplot(x='status',y=df.iloc[:,i],data=df,orient='v',ax=axes[i])
plt.tight_layout()
plt.show()

# This code enhances the visualizations further and provides more insights.

import matplotlib.pyplot as plt
import seaborn as sns

# Pairplot to visualize relationships between multiple features
sns.pairplot(df, hue='status', vars=['MDVP:Fo(Hz)', 'MDVP:Fhi(Hz)', 'MDVP:Flo(Hz)', 'MDVP:Jitter(%)', 'MDVP:Jitter(Abs)'], height=2)
plt.suptitle("Pairplot of Selected Features", y=1.02)
plt.show()

# Violin plot to compare distributions across different status values for multiple features
plt.figure(figsize=(12, 6))
sns.violinplot(x='status', y='MDVP:Fo(Hz)', data=df)  # Example: MDVP:Fo(Hz)
plt.title("Violin Plot of MDVP:Fo(Hz) by Status")
plt.show()

plt.figure(figsize=(12, 6))
sns.violinplot(x='status', y='HNR', data=df) # Example: HNR
plt.title("Violin Plot of HNR by Status")
plt.show()

plt.rcParams['figure.figsize'] = (15, 4)
sns.pairplot(df,hue = 'status', vars = ['MDVP:Jitter(%)','MDVP:Jitter(Abs)','MDVP:RAP','MDVP:PPQ', 'Jitter:DDP'] )
plt.show()

# Extracting Features Into Features & Target
X = df.drop(['status'], axis=1)
y = df['status']

print('Feature (X) Shape Before Balancing :', X.shape)
print('Target (y) Shape Before Balancing :', y.shape)

# Intialising SMOTE Object
from imblearn.over_sampling import SMOTE # Import SMOTE from imblearn.over_sampling
sm = SMOTE(random_state=300)

# Resampling Data
X, y = sm.fit_resample(X, y)

print('Feature (X) Shape After Balancing :', X.shape)
print('Target (y) Shape After Balancing :', y.shape)

from sklearn.preprocessing import MinMaxScaler

# Scaling features between -1 and 1 for normalization
scaler = MinMaxScaler(feature_range=(-1, 1))

# define X_features , Y_labels
X_features = scaler.fit_transform(X)
Y_labels = y

#splitting the dataset into traning and testing sets into 80 - 20
from sklearn.model_selection import train_test_split
X_train , X_test , y_train , y_test = train_test_split(X_features, Y_labels , test_size=0.20, random_state=20)

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from xgboost import XGBClassifier


# Initialize the classifiers
decision_tree = DecisionTreeClassifier()
random_forest = RandomForestClassifier()
logistic_regression = LogisticRegression()
svm = SVC()
naive_bayes = GaussianNB()
knn = KNeighborsClassifier()
xgboost = XGBClassifier()

# Example of training and evaluating the Random Forest model
random_forest.fit(X_train, y_train)
y_pred_rf = random_forest.predict(X_test)
accuracy_rf = accuracy_score(y_test, y_pred_rf)
print(f"Random Forest Accuracy: {accuracy_rf}")

# Similarly train and evaluate other models
decision_tree.fit(X_train,y_train)
y_pred_dt = decision_tree.predict(X_test)
accuracy_dt = accuracy_score(y_test,y_pred_dt)
print(f"Decision Tree Accuracy: {accuracy_dt}")

logistic_regression.fit(X_train,y_train)
y_pred_lr = logistic_regression.predict(X_test)
accuracy_lr = accuracy_score(y_test,y_pred_lr)
print(f"Logistic Regression Accuracy: {accuracy_lr}")

svm.fit(X_train,y_train)
y_pred_svm = svm.predict(X_test)
accuracy_svm = accuracy_score(y_test,y_pred_svm)
print(f"SVM Accuracy: {accuracy_svm}")

naive_bayes.fit(X_train,y_train)
y_pred_nb = naive_bayes.predict(X_test)
accuracy_nb = accuracy_score(y_test,y_pred_nb)
print(f"Naive Bayes Accuracy: {accuracy_nb}")

knn.fit(X_train,y_train)
y_pred_knn = knn.predict(X_test)
accuracy_knn = accuracy_score(y_test,y_pred_knn)
print(f"KNN Accuracy: {accuracy_knn}")

xgboost.fit(X_train,y_train)
y_pred_xgb = xgboost.predict(X_test)
accuracy_xgb = accuracy_score(y_test,y_pred_xgb)
print(f"XGBoost Accuracy: {accuracy_xgb}")

"""#Logistic Regression"""

logmodel = LogisticRegression()
logmodel.fit(X_train, y_train)
predlog = logmodel.predict(X_test)

from sklearn.metrics import classification_report, confusion_matrix
print(classification_report(y_test,predlog))
print(confusion_matrix(y_test,predlog))

# Accessing correlation between 'MDVP:Fo(Hz)' and 'HNR'
correlation_fo_hnr = df['MDVP:Fo(Hz)'].corr(df['HNR'])
print(f"Correlation between MDVP:Fo(Hz) and HNR: {correlation_fo_hnr}")

# Accessing the entire correlation matrix
correlation_matrix = df.corr()
correlation_matrix



