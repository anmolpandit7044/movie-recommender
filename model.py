import pandas as pd
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---------------- LOAD DATA ----------------

movies = pd.read_csv("data/tmdb_5000_movies.csv")
credits = pd.read_csv("data/tmdb_5000_credits.csv")

# ---------------- MERGE DATASETS ----------------

movies = movies.merge(credits, on='title')

# ---------------- SELECT IMPORTANT COLUMNS ----------------

movies = movies[['movie_id',
                 'title',
                 'overview',
                 'genres',
                 'keywords',
                 'cast',
                 'crew']]

# ---------------- REMOVE NULL VALUES ----------------

movies.dropna(inplace=True)

# ---------------- HELPER FUNCTIONS ----------------

# genres / keywords convert
def convert(text):
    L = []

    for i in ast.literal_eval(text):
        L.append(i['name'])

    return L


# cast top 3 actors
def convert3(text):
    L = []
    counter = 0

    for i in ast.literal_eval(text):

        if counter != 3:
            L.append(i['name'])
            counter += 1
        else:
            break

    return L


# fetch director name
def fetch_director(text):
    L = []

    for i in ast.literal_eval(text):

        if i['job'] == 'Director':
            L.append(i['name'])

    return L


# ---------------- APPLY FUNCTIONS ----------------

movies['genres'] = movies['genres'].apply(convert)

movies['keywords'] = movies['keywords'].apply(convert)

movies['cast'] = movies['cast'].apply(convert3)

movies['crew'] = movies['crew'].apply(fetch_director)

# ---------------- CLEAN OVERVIEW ----------------

movies['overview'] = movies['overview'].apply(lambda x: x.split())

# ---------------- REMOVE SPACES ----------------

movies['genres'] = movies['genres'].apply(
    lambda x: [i.replace(" ", "") for i in x]
)

movies['keywords'] = movies['keywords'].apply(
    lambda x: [i.replace(" ", "") for i in x]
)

movies['cast'] = movies['cast'].apply(
    lambda x: [i.replace(" ", "") for i in x]
)

movies['crew'] = movies['crew'].apply(
    lambda x: [i.replace(" ", "") for i in x]
)

# ---------------- CREATE TAGS ----------------

movies['tags'] = (
        movies['overview'] +
        movies['genres'] +
        movies['keywords'] +
        movies['cast'] +
        movies['crew']
)

# ---------------- NEW DATAFRAME ----------------

new_df = movies[['movie_id', 'title', 'tags']]

# ---------------- CONVERT LIST TO STRING ----------------

new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x))

# lowercase
new_df['tags'] = new_df['tags'].apply(lambda x: x.lower())

# ---------------- VECTORIZATION ----------------

cv = CountVectorizer(max_features=5000, stop_words='english')

vectors = cv.fit_transform(new_df['tags']).toarray()

# ---------------- COSINE SIMILARITY ----------------

similarity = cosine_similarity(vectors)

# ---------------- RECOMMEND FUNCTION ----------------

def recommend(movie):

    if movie not in new_df['title'].values:
        print("Movie not found")
        return

    movie_index = new_df[new_df['title'] == movie].index[0]

    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    print("\nRecommended Movies:\n")

    for i in movies_list:
        print(new_df.iloc[i[0]].title)

# ---------------- TEST ----------------

recommend("Avatar")