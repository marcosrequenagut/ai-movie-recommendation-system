# streamlit_app.py
import streamlit as st
import requests

st.title("Movie Recommender 🎬")

user_input = st.text_input("What do you want to watch?")
top_k = st.slider("Top K", 1, 20, 5)
genres = st.multiselect(
    "Filter by genres",
    ["Action", "Adventure", "Animation", "Comedy", "Crime", "Documentary", "Drama", "Family", "Fantasy", "History", "Horror", "Music", "Mystery", "Romance", "Science Fiction", "TV Movie", "Thriller", "War", "Western"]
)

if st.button("Recommend"):
    response = requests.post(
        #http://localhost:8000/agent
        "http://api:8000/agent",
        json={
            "message": user_input,
            "top_k": top_k,
            "genres": genres
        }
    )

    data = response.json()
    movies = data.get("movies", [])

    if movies:
        st.subheader("🍿 Recommended Movies")

        for i, movie in enumerate(movies, start=1):
            st.markdown(f"**{i}. 🎬 {movie}**")

    else:
        st.warning("No movies found")

