import pandas as pd
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem.porter import PorterStemmer

# LOAD DATA
movies = pd.read_csv("data/tmdb_5000_movies.csv")
credits = pd.read_csv("data/tmdb_5000_credits.csv")

# MERGE
movies = movies.merge(credits, on='title')

# SELECT COLUMNS
movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]

# REMOVE NULL
movies.dropna(inplace=True)

# FUNCTIONS
ps = PorterStemmer()

# stem function

def stem(text):

    y = []

    for i in text.split():
        y.append(ps.stem(i))

    return " ".join(y)





def convert(obj):
    L = []
    for i in ast.literal_eval(obj):
        L.append(i['name'])
    return L

def convert3(obj):
    L = []
    counter = 0

    for i in ast.literal_eval(obj):
        if counter != 3:
            L.append(i['name'])
            counter += 1
        else:
            break

    return L

def fetch_director(obj):
    L = []

    for i in ast.literal_eval(obj):
        if i['job'] == 'Director':
            L.append(i['name'])

    return L

# APPLY
movies['genres'] = movies['genres'].apply(convert)

movies['keywords'] = movies['keywords'].apply(convert)

movies['cast'] = movies['cast'].apply(convert3)

movies['crew'] = movies['crew'].apply(fetch_director)

# OVERVIEW SPLIT
movies['overview'] = movies['overview'].apply(lambda x: x.split())

# REMOVE SPACES
movies['genres'] = movies['genres'].apply(
    lambda x: [i.replace(" ","") for i in x]
)

movies['keywords'] = movies['keywords'].apply(
    lambda x: [i.replace(" ","") for i in x]
)

movies['cast'] = movies['cast'].apply(
    lambda x: [i.replace(" ","") for i in x]
)

movies['crew'] = movies['crew'].apply(
    lambda x: [i.replace(" ","") for i in x]
)

# CREATE TAGS
movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

# NEW DATAFRAME
new_data = movies[['movie_id','title','tags']]

# LIST TO STRING
new_data['tags'] = new_data['tags'].apply(lambda x: " ".join(x))

# LOWERCASE
new_data['tags'] = new_data['tags'].apply(lambda x: x.lower())

new_data['tags'] = new_data['tags'].apply(stem)

# DEBUG
   # print(new_data['tags'].head())

# VECTORIZATION
cv = TfidfVectorizer(
    max_features=5000,
    stop_words='english'
)

vectors = cv.fit_transform(new_data['tags']).toarray()

# SIMILARITY
similarity = cosine_similarity(vectors)


def recommend(movie):

    if movie is None:
        return []

    movie = movie.strip()

    matched_movies = new_data[
        new_data['title'] == movie
    ]

    # Movie not found
    if matched_movies.empty:
        return []

    movie_index = matched_movies.index[0]

    distances = similarity[movie_index]

    # Sort movies by similarity
    movies_list = sorted(
        list(enumerate(distances)),
        key=lambda x: x[1],
        reverse=True
    )

    recommended_movies = []

    for i in movies_list:

        movie_title = new_data.iloc[i[0]].title

        # Skip selected movie itself
        if movie_title != movie:

            recommended_movies.append(movie_title)

        # Stop after 5 movies
        if len(recommended_movies) == 5:
            break

    return recommended_movies