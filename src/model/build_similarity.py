import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle  # optional, for saving similarity matrix and indices

df = pd.read_csv("data/processed/movies_cleaned.csv")

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

# -----------------------------
# Load cleaned dataset
# -----------------------------
df = pd.read_csv("data/processed/movies_cleaned.csv")

# -----------------------------
# Vectorize the 'tags' column
# -----------------------------
# max_features limits vocabulary size
# stop_words='english' removes common words
vectorizer = CountVectorizer(max_features=5000, stop_words='english')
vectors = vectorizer.fit_transform(df['tags']).toarray()

# -----------------------------
# Compute cosine similarity
# -----------------------------
similarity = cosine_similarity(vectors)

# -----------------------------
# Create mapping from title -> index
# -----------------------------
movie_indices = pd.Series(df.index, index=df['title']).to_dict()

# -----------------------------
# Recommendation function
# -----------------------------
def recommend(movie_name, top_n=5):
    if movie_name not in movie_indices:
        print(f"Movie '{movie_name}' not found in dataset.")
        return []
    
    idx = movie_indices[movie_name]
    sim_scores = list(enumerate(similarity[idx]))
    
    # Sort by similarity score descending, skip the movie itself
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    recommended_indices = [i for i, score in sim_scores[1:top_n+1]]
    
    recommended_movies = df['title'].iloc[recommended_indices].values.tolist()
    return recommended_movies

# -----------------------------
# Example usage
# -----------------------------
if __name__ == "__main__":
    movie = "Inception"  # change to any title in your dataset
    recommendations = recommend(movie, top_n=5)
    print(f"Movies similar to '{movie}':")
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec}")

# -----------------------------
# Optional: Save objects for FastAPI
# -----------------------------
with open("models/similarity.pkl", "wb") as f:
    pickle.dump(similarity, f)

with open("models/movie_indices.pkl", "wb") as f:
    pickle.dump(movie_indices, f)
