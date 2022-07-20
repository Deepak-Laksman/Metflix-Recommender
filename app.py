import config
import mod
import pandas as pd
import streamlit as st
import pickle
import requests

def fetch_poster(movie_id):
    response = requests.get(config.api_key.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data["poster_path"]

def recommend(movie):
    # Getting movie index from dataframe
    movie_index = movies[movies["title"] == movie].index[0]
    # finding the vector with similarity values for that movie w.r.t all other movies
    distances = cosine_sim[movie_index]
    # sorting the similarity values in descending order along with their indices and taking top 5 movies
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []
    # Traversing the movies list
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        # Using the get_title_from_index function to get movie_name from the index in dataframe
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

movie_dict = pickle.load(open("movie_dict.pkl", "rb"))
cosine_sim = pickle.load(open("cosine_similarity.pkl", "rb"))

movies = pd.DataFrame(movie_dict)
st.title("Movie Recommender System")

selected_movie_name = st.selectbox(
    'Select movie to get recommendations',
    movies["title"].values
)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])
