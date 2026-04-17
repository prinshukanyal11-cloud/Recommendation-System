import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=5173c4a1a23a383bce47cde55e321e0e&language=en-US"
        
        response = requests.get(url, timeout=5)
        response.raise_for_status()   
        
        data = response.json()
        poster_path = data.get('poster_path')

        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"

    except requests.exceptions.RequestException:
        return "https://via.placeholder.com/500x750?text=Connection+Error"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    # new_df[new_df['title'] == 'Avatar']
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True, key = lambda x:x[1])[1:6]

    recommended_movies = []

    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]]['id']

        # Fetching movie poster from API
        recommended_movies.append((movies.iloc[i[0]].title))
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters
    

st.header('Movie Recommender System')

st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}

/* Main Title */
h1 {
    color: #ffffff;
    text-align: center;
    font-size: 42px;
    font-weight: bold;
}
            
h3 {
    color: #ffffff !important;
    text-align: center;
    font-size: 18px;
    font-weight: bold;
    text-shadow: 0px 0px 8px rgba(255,255,255,0.6);
}
            
/* All normal text */
p, label, span, div {
    color: #f1f1f1 !important;
}

/* Dropdown */
div[data-baseweb="select"] {
    background-color: #1e1e2f !important;
    color: black !important;
    border-radius: 10px !important;
}

/* Selected value text */
[data-baseweb="select"] div {
    color: black !important;
}

/* Dropdown menu panel */
div[data-baseweb="popover"] {
    background-color: white !important;
}

/* All dropdown options */
div[data-baseweb="popover"] * {
    color: black !important;
}

/* Option hover */
div[role="option"]:hover {
    background-color: #f2f2f2 !important;
    color: black !important;
}
            

/* Button */
.stButton>button {
    background-color: #ff4b4b;
    color: white;
    font-weight: bold;
    border-radius: 8px;
    padding: 10px 20px;
    border: none;
    transition: 0.3s ease;
}

.stButton>button:hover {
    background-color: #ff1e1e;
    transform: scale(1.05);
}

/* Movie Titles */
h3 {
    color: black !important;
    text-align: center;
    font-size: 18px;
    font-weight: bold;
}

/* Remove faded effect */
.css-1v0mbdj img {
    opacity: 1 !important;
}

/* Hide Streamlit footer */
footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

movies_dict = pickle.load(open('movies_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl','rb'))

movie_list = movies['title'].values
selected_movie_name = st.selectbox(
    'Type or select a movie from the dropdown',
    movie_list
)

if st.button("Show Recommendation"):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)

    cols = st.columns(5)

    for col, name, poster in zip(cols, recommended_movie_names, recommended_movie_posters):
        with col:
            st.image(poster)
            st.markdown(f"<h3>{name}</h3>", unsafe_allow_html=True)

  
     

# 32c8dc792ca49e901873cd72bc4c836c


