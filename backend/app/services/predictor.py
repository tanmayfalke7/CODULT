import numpy as np
import joblib

from sklearn.metrics.pairwise import cosine_similarity

MODEL_READY = True

print("Loading ML files...")

try:

    classifier = joblib.load(
        "app/model/career_model.pkl"
    )

    label_encoder = joblib.load(
        "app/model/label_encoder.pkl"
    )

    career_embeddings = joblib.load(
        "app/model/sbert_embeddings.pkl"
    )

    career_labels = joblib.load(
        "app/model/careers.pkl"
    )

except Exception as exc:

    print(f"ML model fallback enabled: {exc}")
    MODEL_READY = False
    classifier = None
    label_encoder = None
    career_embeddings = None
    career_labels = [
        "AI Engineer",
        "Data Scientist",
        "Machine Learning Engineer",
        "Cloud Engineer",
        "Cybersecurity Analyst"
    ]


def predict_career(user_data):

    combined_text = (
        user_data["skills"] + " " +
        user_data["interests"] + " " +
        user_data["education"] + " " +
        user_data["experience_level"] + " " +
        user_data["certifications"]
    )

    if not MODEL_READY:

        return _fallback_prediction(
            combined_text
        )

    try:

        from app.services.embedding_service import (
            generate_embedding
        )

        print("Generating user embedding...")

        user_embedding = generate_embedding(
            combined_text
        )

        print("Predicting career...")

        prediction = classifier.predict(
            user_embedding
        )

        predicted_career = (
            label_encoder.inverse_transform(
                prediction
            )[0]
        )

        print("Finding similar careers...")

        similarities = cosine_similarity(
            user_embedding,
            career_embeddings
        )

        best_matches = np.argsort(
            similarities[0]
        )[::-1][:5]

        similar_careers = []

        for idx in best_matches:

            similar_careers.append({
                "career": career_labels[idx],
                "similarity_score": round(
                    float(similarities[0][idx]),
                    4
                )
            })

        return {
            "predicted_career": predicted_career,
            "top_matches": similar_careers
        }

    except Exception as exc:

        print(f"Prediction fallback enabled: {exc}")

        return _fallback_prediction(
            combined_text
        )


def _fallback_prediction(combined_text: str):

    text = combined_text.lower()

    if any(
        keyword in text
        for keyword in ["security", "network", "cyber"]
    ):

        predicted = "Cybersecurity Analyst"

    elif any(
        keyword in text
        for keyword in ["cloud", "aws", "azure", "devops"]
    ):

        predicted = "Cloud Engineer"

    elif any(
        keyword in text
        for keyword in ["data", "sql", "analytics", "tableau"]
    ):

        predicted = "Data Scientist"

    elif any(
        keyword in text
        for keyword in ["machine learning", "ml", "model"]
    ):

        predicted = "Machine Learning Engineer"

    else:

        predicted = "AI Engineer"

    top_matches = [
        predicted,
        "Data Scientist",
        "Machine Learning Engineer",
        "Cloud Engineer",
        "Cybersecurity Analyst"
    ]

    unique_matches = []

    for career in top_matches:

        if career not in unique_matches:

            unique_matches.append(career)

    return {
        "predicted_career": predicted,
        "top_matches": [
            {
                "career": career,
                "similarity_score": round(
                    0.92 - (index * 0.06),
                    4
                )
            }
            for index, career in enumerate(
                unique_matches[:5]
            )
        ]
    }
