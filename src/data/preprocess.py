import pandas as pd
import ast

# -----------------------------
# Helper functions
# -----------------------------

def normalize_text(text):
    return text.lower().replace(" ", "")

def normalize_list(items):
    return " ".join([item.lower().replace(" ", "") for item in items])

def safe_literal_eval(x):
    """
    Safely convert string representations of lists/dicts into Python objects.
    Returns empty list if parsing fails or if type is unexpected.
    """
    if isinstance(x, str):
        try:
            return ast.literal_eval(x)
        except Exception:
            return []
    elif isinstance(x, list):
        return x
    else:
        return []

# -----------------------------
# Structured column parsing
# -----------------------------

def parse_names(text):
    try:
        items = ast.literal_eval(text)
        return [item['name'] for item in items]
    except:
        return []

def extract_director(text):
    try:
        items = ast.literal_eval(text)
        for person in items:
            if person['job'] == 'Director':
                return person['name']
        return ''
    except:
        return ''
    
def extract_top_cast(text, n=3):
    try:
        items = ast.literal_eval(text)
        return [item['name'] for item in items[:n]]
    except:
        return []

def parse_structured_columns(df):
    df['genres'] = df['genres'].apply(parse_names)
    df['keywords'] = df['keywords'].apply(parse_names)
    df['cast'] = df['cast'].apply(extract_top_cast)
    df['director'] = df['crew'].apply(extract_director)
    df = df.drop(columns=['crew'])
    return df

# -----------------------------
# Build tags column
# -----------------------------

def build_tags(df):
    df['genres'] = df['genres'].apply(lambda x: normalize_list(safe_literal_eval(x)))
    df['keywords'] = df['keywords'].apply(lambda x: normalize_list(safe_literal_eval(x)))
    df['cast'] = df['cast'].apply(lambda x: normalize_list(safe_literal_eval(x)))
    df['director'] = df['director'].fillna('').apply(normalize_text)

    df['tags'] = (
        df['overview'].str.lower() + " " +
        df['genres'] + " " +
        df['keywords'] + " " +
        df['cast'] + " " +
        df['director']
    )

    return df

def drop_intermediate_columns(df):
    return df[['title', 'tags']]

# -----------------------------
# Data loading and cleaning
# -----------------------------

def load_and_merge_data(movies_path, credits_path):
    movies = pd.read_csv(movies_path)
    credits = pd.read_csv(credits_path)

    merged = movies.merge(
        credits,
        left_on='id',
        right_on='movie_id'
    )

    # Resolve duplicate title columns
    merged = merged.rename(columns={'title_x': 'title'})
    merged = merged.drop(columns=['title_y', 'movie_id'])

    return merged

def select_relevant_columns(df):
    return df[['title', 'overview', 'genres', 'keywords', 'cast', 'crew']]

def drop_missing_overview(df):
    return df.dropna(subset=['overview'])

# -----------------------------
# Main pipeline
# -----------------------------

def main():
    movies_path = "data/raw/tmdb_5000_movies.csv"
    credits_path = "data/raw/tmdb_5000_credits.csv"

    df = load_and_merge_data(movies_path, credits_path)
    df = select_relevant_columns(df)
    df = drop_missing_overview(df)
    df = parse_structured_columns(df)
    df = build_tags(df)
    df = drop_intermediate_columns(df)

    df.to_csv("data/processed/movies_cleaned.csv", index=False)
    print(f"Cleaned dataset saved with {df.shape[0]} movies.")

if __name__ == "__main__":
    main()
