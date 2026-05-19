# streamlit_app.py
import streamlit as st
import requests

st.title("Movie Recommender 🎬")

user_input = st.text_input("What do you want to watch?")
top_k = st.slider("Top K", 1, 20, 5)

# Select the filters
genres = st.multiselect(
    "Filter by genres",
    ["Action", "Adventure", "Animation", "Comedy", "Crime", "Documentary", "Drama", "Family", "Fantasy", "History", "Horror", "Music", "Mystery", "Romance", "Science Fiction", "TV Movie", "Thriller", "War", "Western"]
)

# Select the user mode
user_mode = st.segmented_control(
    "Mode",
    ["smart", "quality", "taste"],
    default="smart"
)

# Conversation Memory
if "thread_id" not in st.session_state:
    st.session_state.thread_id = None

if st.button("🔁 Continue previous conversation"):
    st.session_state.use_thread = True

if "use_thread" not in st.session_state:
    st.session_state.use_thread = False

thread_id = None

if st.session_state.use_thread:
    thread_id = st.session_state.thread_id

# Year filter
with st.expander("🎞️ Filter by year"):

    mode = st.radio("Quick mode", ["All", "Custom range"])

    years = list(range(2026, 1899, -1))

    if mode == "All":
        year_from, year_to = 1900, 2026

    else:
        col1, col2 = st.columns(2)

        with col1:
            year_from = st.selectbox("From", years, index=len(years)-1)

        with col2:
            year_to = st.selectbox("To", years, index=0)

if st.button("Recommend"):
    response = requests.post(
        #http://localhost:8000/agent
        "http://api:8000/agent",
        json={
            "query": user_input,
            "top_k": top_k,
            "filters": {
                "genres": genres,
                "year_from": year_from,
                "year_to": year_to},
            "user_mode": user_mode,
            "trhead_id": thread_id
        }
    )

    data = response.json()
    movies = data.get("movies", [])
    st.session_state.thread_id = data.get("thread_id")

    if movies:
        st.subheader("🍿 Recommended Movies")

        for i, movie in enumerate(movies, start=1):
            st.markdown(f"**{i}. 🎬 {movie}**")

    else:
        st.warning("No movies found")

