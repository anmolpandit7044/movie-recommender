import streamlit as st
import requests
from model import recommend, new_data

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Netflix Style Recommender",
    page_icon="🎬",
    layout="wide"
)

# ---------------- CSS ----------------
st.markdown("""
<style>

.stApp {
    background-color: #000814;
    color: white;
}

h1 {
    color: #E50914;
    text-align: center;
    font-size: 55px;
    font-weight: 900;
    letter-spacing: 2px;
}

.stButton > button {
    background: linear-gradient(45deg, #E50914, #b00610);
    color: white;
    border-radius: 12px;
    height: 50px;
    width: 220px;
    font-size: 18px;
    font-weight: bold;
}

.stButton > button:hover {
    transform: scale(1.05);
}

.movie-card {
    background: #1c1c1c;
    padding: 12px;
    border-radius: 10px;
    text-align: center;
    min-height: 80px;
    font-size: 16px;
    font-weight: bold;
}

.movie-card:hover {
    background: #2a2a2a;
    transform: translateX(10px);
}

</style>
""", unsafe_allow_html=True)

def fetch_poster(movie):

    try:
        url = f"https://www.omdbapi.com/?t={movie}&apikey=31a92a7c"

        response = requests.get(url)

        data = response.json()

        poster = data.get("Poster", "N/A")

        if poster == "N/A":
            return None

        return poster

    except:
        return None


# ---------------- TITLE ----------------
st.markdown("<h1>🎬 Netflix Style Movie Recommender</h1>", unsafe_allow_html=True)

# ---------------- MOVIE LIST ----------------
movie_list = sorted(new_data['title'].dropna().unique())

# ---------------- SELECT BOX ----------------
selected_movie = st.selectbox(
    "Select Movie",
    options=movie_list,
    index=None,
    placeholder="Choose a movie"
)

# ---------------- BUTTON ----------------
if st.button("Recommend"):

    if not selected_movie:
        st.warning("⚠ Please select a movie")

    else:

        result = recommend(selected_movie)

        if not result:
            st.error("No recommendations found")

        else:

            st.subheader("🍿 Recommended Movies")

            cols = st.columns(3)

            for idx, movie in enumerate(result[:5]):

               with cols[idx % 3]:

                 poster = fetch_poster(movie)

                 if poster:
                    st.image(poster, width=200)
                 else:
                   st.write("🎞 Poster not available")

                 st.markdown(
                    f"""
                    <div style="
                        width:200px;
                        text-align:center;
                        color:white;
                        font-size:20px;
                        font-weight:bold;
                        margin-top:8px;
                    ">
                        🎬 {movie}
                    </div>
                    """,
                    unsafe_allow_html=True
                )