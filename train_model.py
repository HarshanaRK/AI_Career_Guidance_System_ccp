import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
from sklearn import metrics

# Load dataset
career = pd.read_csv(r'D:\cpp2\dataset9000.data', header=None)

# Define column names
career.columns = [
    "Database Fundamentals", "Computer Architecture", "Distributed Computing Systems",
    "Cyber Security", "Networking", "Development", "Programming Skills", "Project Management",
    "Computer Forensics Fundamentals", "Technical Communication", "AI ML", "Software Engineering",
    "Business Analysis", "Communication skills", "Data Science", "Troubleshooting skills",
    "Graphics Designing", "Roles"
]

# Drop missing values
career.dropna(inplace=True)

# Split Features (X) and Target (y)
X = career.iloc[:, :-1].values  # All columns except last
y = career.iloc[:, -1].values   # Last column (Roles)

# Encode Target Labels (Convert text labels to numbers)
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Split into Training & Testing
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.3, random_state=524, stratify=y_encoded)

# Train SVM Model
model = SVC(kernel='poly', probability=True)
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)
accuracy = metrics.accuracy_score(y_test, y_pred)
print(f'✅ Accuracy = {accuracy * 100:.2f}%')

# Save Model & Label Encoder
with open("careerlast.pkl", "wb") as f:
    pickle.dump(model, f)

with open("label_encoder.pkl", "wb") as f:
    pickle.dump(label_encoder, f)

print("✅ Model & Label Encoder saved as `careerlast.pkl` and `label_encoder.pkl`.")
