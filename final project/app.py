import streamlit as st
import pickle
import requests
import base64  # Import base64 to encode the image

def get_base64_image(image_file):
    """Convert an image file to a base64 string."""
    with open(image_file, "rb") as image:
        return base64.b64encode(image.read()).decode()

# Set the path for the background image
image_path = r"C:\Users\USER\Desktop\final project\Untitled design (1).png"

# Add custom CSS for the background image and title styling
page_bg_image = f'''
<style>
.stApp {{
    background-image: url("data:image/jpg;base64,{get_base64_image(image_path)}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}}

h1 {{
    color: yellow;  /* Change the text color to yellow */
    font-size: 3em; /* Increase the font size */
    font-weight: bold; /* Make the font bold */
}}
</style>
'''

st.markdown(page_bg_image, unsafe_allow_html=True)

# Set a custom title
st.markdown("<h1>Movie Recommender System</h1>", unsafe_allow_html=True)

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

movies = pickle.load(open(r"C:\Users\USER\Desktop\final project\movies_list.pkl", 'rb'))
similarity = pickle.load(open(r"C:\Users\USER\Desktop\final project\similarity.pkl", 'rb'))
movies_list = movies['title'].values

selectvalue = st.selectbox("Select movie from dropdown", movies_list)

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
    recommend_movie = []
    recommend_poster = []
    for i in distance[1:6]:
        movies_id = movies.iloc[i[0]].id
        recommend_movie.append(movies.iloc[i[0]].title)
        recommend_poster.append(fetch_poster(movies_id))
    return recommend_movie, recommend_poster

if st.button("Show Recommend"):
    movie_name, movie_poster = recommend(selectvalue)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(movie_name[0])
        st.image(movie_poster[0])
    with col2:
        st.text(movie_name[1])
        st.image(movie_poster[1])
    with col3:
        st.text(movie_name[2])
        st.image(movie_poster[2])
    with col4:
        st.text(movie_name[3])
        st.image(movie_poster[3])
    with col5:
        st.text(movie_name[4])
        st.image(movie_poster[4])
