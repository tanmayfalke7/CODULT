import pandas as pd
import joblib

from sentence_transformers import SentenceTransformer

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report

print("Loading dataset...")

df = pd.read_csv("career_dataset.csv")

# Fill missing values
columns = [
    "skills",
    "interests",
    "education",
    "experience_level",
    "certifications"
]

for col in columns:
    df[col] = df[col].fillna("")

print("Combining features...")

df["combined_text"] = (
    df["skills"] + " " +
    df["interests"] + " " +
    df["education"] + " " +
    df["experience_level"] + " " +
    df["certifications"]
)

X = df["combined_text"]
y = df["career"]

print("Encoding labels...")

label_encoder = LabelEncoder()

y_encoded = label_encoder.fit_transform(y)

print("Loading SBERT model...")

sbert_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("Generating embeddings...")

embeddings = sbert_model.encode(
    X.tolist(),
    show_progress_bar=True
)

print("Splitting dataset...")

X_train, X_test, y_train, y_test = train_test_split(
    embeddings,
    y_encoded,
    test_size=0.2,
    random_state=42
)

print("Training Logistic Regression...")

model = LogisticRegression(
    max_iter=2000,
    multi_class="multinomial"
)

model.fit(X_train, y_train)

print("Evaluating model...")

predictions = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    predictions
)

print(f"\nAccuracy: {accuracy * 100:.2f}%\n")

print(
    classification_report(
        y_test,
        predictions,
        target_names=label_encoder.classes_
    )
)

print("Saving model files...")

joblib.dump(
    model,
    "../app/model/career_model.pkl"
)

joblib.dump(
    label_encoder,
    "../app/model/label_encoder.pkl"
)

joblib.dump(
    embeddings,
    "../app/model/sbert_embeddings.pkl"
)

joblib.dump(
    df["career"].tolist(),
    "../app/model/careers.pkl"
)

print("\nAll files saved successfully!")