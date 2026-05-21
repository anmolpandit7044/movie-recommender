import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---------------- LOAD DATA ----------------
movies = pd.read_csv("data/tmdb_5000_movies.csv")

movies = movies[['title', 'genres', 'keywords', 'overview']]
movies.dropna(inplace=True)

# ---------------- CREATE TAGS ----------------
movies['tags'] = movies['genres'] + " " + movies['keywords'] + " " + movies['overview']

# ---------------- VECTORIZATION ----------------
tfidf = TfidfVectorizer(stop_words='english')
vector = tfidf.fit_transform(movies['tags'])

# ---------------- SIMILARITY ----------------
similarity = cosine_similarity(vector)

# reset index
movies = movies.reset_index(drop=True)

# ---------------- RECOMMEND FUNCTION ----------------
def recommend(movie):
    if movie not in movies['title'].values:
        return ["Movie not found in dataset"]

    idx = movies[movies['title'] == movie].index[0]
    distances = similarity[idx]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommendations = []
    for i in movie_list:
        recommendations.append(movies.iloc[i[0]].title)

    return recommendations

# export dataset for UI
new_data = movies