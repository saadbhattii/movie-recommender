# Movie Recommender System

A content-based movie recommendation system built with Python, Pandas, and FastAPI.  
Input a movie title and get similar movie recommendations based on tags including overview, genres, cast, director, and keywords.

---

## Project Structure

```
movie-recommender/
 ├─ data/
 │   ├─ raw/               # Original CSV datasets (not included in repo)
 │   └─ processed/         # Cleaned & processed data (generated locally)
 ├─ models/                # Saved similarity matrix and indices
 ├─ src/
 │   ├─ api/
 │   │   └─ main.py        # FastAPI application
 │   ├─ data/
 │   │   └─ preprocess.py  # Data cleaning pipeline
 │   └─ models/
 │       └─ build_similarity.py # Vectorization & similarity computation
 ├─ venv/                  # Python virtual environment
 └─ README.md
```

---

## Dataset

This project uses the [TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata) from Kaggle.  

After downloading, place the files here:

```
data/raw/tmdb_5000_movies.csv
data/raw/tmdb_5000_credits.csv
```

---

## Installation

1. Clone the repository:

```bash
git clone <repo_url>
cd movie-recommender
```

2. Create and activate virtual environment:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
# Or manually:
pip install pandas scikit-learn nltk fastapi uvicorn
```

---

## Usage

### 1. Preprocess Data

```bash
python src/data/preprocess.py
```

This will:

- Merge raw movie and credits CSVs  
- Extract relevant features (genres, keywords, cast, director)  
- Build a combined `tags` column  
- Save cleaned CSV to `data/processed/movies_cleaned.csv`

---

### 2. Build Similarity Matrix

```bash
python src/models/build_similarity.py
```

This will:

- Vectorize the `tags` column  
- Compute cosine similarity between all movies  
- Save `similarity.pkl` and `movie_indices.pkl` for API use

---

### 3. Run FastAPI

```bash
uvicorn src.api.main:app --reload
```

- Open browser: `http://127.0.0.1:8000/`  
- Test recommendations:  
  ```
  http://127.0.0.1:8000/recommend?movie=Inception&top_n=5
  ```

---

## Example

**Request:**

```
/recommend?movie=Inception&top_n=5
```

**Response:**

```json
{
  "movie": "Inception",
  "recommendations": [
    "Duplex",
    "The Helix... Loaded",
    "Star Trek II: The Wrath of Khan",
    "Transformers: Revenge of the Fallen",
    "Timecop"
  ]
}
```

---

## Notes

- Content-based recommendations rely on movie features only; no user data is used  
- Refinements like **TF-IDF weighting** or **genre filtering** can improve recommendation relevance  
- Entire system runs locally; no external API required  

---

