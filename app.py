import streamlit as st
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

.main {
    background: radial-gradient(circle at top, #141414, #000);
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
    padding: 15px;
    margin: 10px 0;
    border-radius: 12px;
    border-left: 5px solid #E50914;
    font-size: 18px;
}

.movie-card:hover {
    background: #2a2a2a;
    transform: translateX(10px);
}

</style>
""", unsafe_allow_html=True)

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

        st.subheader("🍿 Recommended Movies")

        cols = st.columns(3)

        for i, movie in enumerate(result):
            with cols[i % 3]:
                st.markdown(f"""
                <div class="movie-card">
                    🎬 {movie}
                </div>
                """, unsafe_allow_html=True)
