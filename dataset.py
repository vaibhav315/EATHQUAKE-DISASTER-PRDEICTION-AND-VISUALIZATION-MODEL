import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

file_path = 'C:/Users/Pracheer/Desktop/Earthquake Prediction/earthquake_dataset.csv'
data = pd.read_csv(file_path)

print("Dataset Overview:")
print(data.head())
print(data.info())

data.fillna(data.mean(numeric_only=True), inplace=True)  # Fill numeric missing values with the mean

bins = [0, 4.0, 6.0, 10.0]
labels = ['Low', 'Moderate', 'High'] 
if 'magnitudo' in data.columns:
    data['magnitude_category'] = pd.cut(data['magnitudo'], bins=bins, labels=labels)
else:
    raise KeyError("The target column 'magnitudo' does not exist in the dataset.")

features = ['longitude', 'latitude', 'depth', 'tsunami', 'significance']
target = 'magnitude_category'

data[target] = data[target].cat.codes 


X = data[features]
y = data[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("\nConfusion Matrix:")
conf_matrix = confusion_matrix(y_test, y_pred)
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=labels, yticklabels=labels)
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()

print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=labels))


example = [[78.1, 19.1, 10.0, 0, 300]]
example_df = pd.DataFrame(example, columns=features)
prediction = model.predict(example_df)
predicted_category = labels[prediction[0]]
print(f"\nPrediction for {example}: {predicted_category}")
