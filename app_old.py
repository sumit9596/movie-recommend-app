import pickle
import streamlit as st
import requests

# Configure page
st.set_page_config(
    page_title="🎬 Movie Recommender",
    page_icon="🍿",
    layout="wide",
    initial_sidebar_state="auto"
)

# Custom CSS styling
st.markdown("""
    <style>
    /* Dark gradient background */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        color: #e0e0e0;
    }
    
    /* Override default backgrounds */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    }
    
    /* Header styling */
    .header-title {
        text-align: center;
        background: linear-gradient(135deg, #ff6b6b 0%, #ff8c42 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3.5em;
        font-weight: bold;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .header-subtitle {
        text-align: center;
        color: #b0b0ff;
        font-size: 1.2em;
        margin-bottom: 2rem;
    }
    
    /* Recommendation cards - modern glass effect */
    .movie-card {
        background: transparent;
        border: none;
        border-radius: 20px;
        padding: 0px;
        margin: 10px;
        transition: transform 0.3s ease;
        text-align: center;
    }
    
    .movie-card:hover {
        transform: translateY(-15px);
    }
    
    .movie-title {
        color: #ffffff;
        font-weight: bold;
        font-size: 1em;
        margin-top: 10px;
        text-align: center;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #ffa500 0%, #ff6b6b 100%);
        color: white;
        border: none;
        padding: 15px 40px;
        font-size: 1.1em;
        border-radius: 50px;
        cursor: pointer;
        width: 100%;
        transition: transform 0.2s, box-shadow 0.2s;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.4);
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 25px rgba(255, 107, 107, 0.6);
    }
    
    /* Selectbox styling */
    .stSelectbox {
        margin-bottom: 1.5rem;
    }
    
    .stSelectbox [data-testid="stSelectbox"] {
        background-color: rgba(255, 255, 255, 0.08);
        border-radius: 10px;
        border: 2px solid rgba(255, 255, 255, 0.15);
    }
    
    /* Text styling */
    label {
        color: #e0e0e0 !important;
    }
    
    /* Divider */
    hr {
        border-color: rgba(255, 150, 0, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

def fetch_poster(movie_id):
    try:
        url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
        data = requests.get(url, timeout=5)
        data = data.json()
        if data.get('poster_path'):
            poster_path = data['poster_path']
            full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
            return full_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster"
    except Exception as e:
        print(f"Error fetching poster for movie_id {movie_id}: {e}")
        return "https://via.placeholder.com/500x750?text=No+Poster"

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:16]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters


st.markdown("<div class='header-title'>🎬 Movie Recommender System</div>", unsafe_allow_html=True)
st.markdown("<div class='header-subtitle'>Discover your next favorite movie! 🍿</div>", unsafe_allow_html=True)

# Divider
st.divider()

# Load data
movies = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

movie_list = movies['title'].values

# Create selection layout
col1, col2 = st.columns([3, 1])

with col1:
    selected_movie = st.selectbox(
        "🎥 Select or type a movie name:",
        movie_list,
        help="Choose a movie to get recommendations"
    )

with col2:
    st.write("")  # Add spacing
    st.write("")  # Add spacing
    button_pressed = st.button('🎯 Get Recommendations', use_container_width=True)

st.markdown("")

if button_pressed:
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    
    st.markdown("---")
    st.markdown("<h2 style='text-align: center; color: #ffa500;'>✨ Recommended Movies for You (Top 15) ✨</h2>", unsafe_allow_html=True)
    st.markdown("")
    
    # Display recommendations in 3 rows of 5 columns
    for row in range(3):
        cols = st.columns(5, gap="medium")
        for col_idx, col in enumerate(cols):
            movie_idx = row * 5 + col_idx
            with col:
                st.markdown(f"<div class='movie-card'>", unsafe_allow_html=True)
                st.image(recommended_movie_posters[movie_idx], width=250)
                st.markdown(f"<div class='movie-title'>{recommended_movie_names[movie_idx]}</div>", unsafe_allow_html=True)
                st.markdown(f"</div>", unsafe_allow_html=True)
