from sklearn.cluster import KMeans
import joblib
import os

def apply_clustering(df, features):

    model = KMeans(
        n_clusters=4,
        random_state=42,
        n_init=10
    )

    df['CareerCluster'] = model.fit_predict(df[features])

    os.makedirs("models", exist_ok=True)

    joblib.dump(
        model,
        "models/kmeans_model.pkl"
    )

    return df