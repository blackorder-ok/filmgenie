import streamlit as st
import pandas as pd
import pickle
import requests
from urllib.request import urlopen
import json

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=89d2b56de40f0f51fdd83b175835229b&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    #st.text(data)
    poster_path = data['poster_path']
    # st.text(data['imdb_id'])
    # response=urlopen(url)
    # data_json=json.loads(response.read())
    # print(data_json)
    # data=data_json.json()
    # st.text(data)
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path #"/k4Rx1dwoKkZrtSD0mZBRBo22jmb.jpg"
    return full_path

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances=similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key = lambda x: x[1])[1:6]
    
    recommended_movies=[]
    recommended_movies_posters=[]

    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id
        #st.text(movie_id)
        recommended_movies_posters.append(fetch_poster(movie_id))
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies,recommended_movies_posters

movies_dict=pickle.load(open('movie_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommender System')

selected_movie_name=st.selectbox(
'Select a movie',movies['title'].values
)

if st.button('Recommend'):
    recommended_movie_names,recommended_movie_posters=recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])
    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])

