from fastapi import FastAPI, HTTPException
import pandas as pd
import pickle

# -----------------------------
# Load data
# -----------------------------
df = pd.read_csv("data/processed/movies_cleaned.csv")

with open("models/similarity.pkl", "rb") as f:
    similarity = pickle.load(f)

with open("models/movie_indices.pkl", "rb") as f:
    movie_indices = pickle.load(f)

# -----------------------------
# FastAPI app
# -----------------------------
app = FastAPI(title="Movie Recommender")

# -----------------------------
# Recommendation function
# -----------------------------
def recommend(movie_name: str, top_n: int = 5):
    if movie_name not in movie_indices:
        raise HTTPException(status_code=404, detail=f"Movie '{movie_name}' not found")
    
    idx = movie_indices[movie_name]
    sim_scores = list(enumerate(similarity[idx]))
    
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    recommended_indices = [i for i, score in sim_scores[1:top_n+1]]
    
    recommended_movies = df['title'].iloc[recommended_indices].tolist()
    return recommended_movies

# -----------------------------
# API endpoints
# -----------------------------
@app.get("/")
def home():
    return {"message": "Welcome to the Movie Recommender API!"}

@app.get("/recommend")
def recommend_movies(movie: str, top_n: int = 5):
    recommendations = recommend(movie, top_n)
    return {"movie": movie, "recommendations": recommendations}

