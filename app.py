import pickle
import streamlit as st
import requests
import pandas as pd
import numpy as np
import json
from functools import lru_cache

# Configure page
st.set_page_config(
    page_title="🎬 Movie Recommender",
    page_icon="🍿",
    layout="wide",
    initial_sidebar_state="auto"
)

# Initialize session state for theme
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

# Responsive Grid Function
@st.cache_data
def get_responsive_css():
    """Responsive CSS for mobile, tablet, and desktop"""
    return """
    <style>
    /* Mobile (< 600px) - 1-2 columns */
    @media (max-width: 600px) {
        .header-title {
            font-size: 2em !important;
        }
        .header-subtitle {
            font-size: 0.9em !important;
        }
        .stButton > button {
            padding: 10px 15px !important;
            font-size: 0.9em !important;
        }
    }
    
    /* Tablet (600px - 1000px) - 3 columns */
    @media (min-width: 600px) and (max-width: 1000px) {
        .header-title {
            font-size: 2.5em !important;
        }
        .header-subtitle {
            font-size: 1.05em !important;
        }
        .stButton > button {
            padding: 12px 20px !important;
            font-size: 0.95em !important;
        }
    }
    
    /* Desktop (> 1000px) - 5 columns */
    @media (min-width: 1000px) {
        .header-title {
            font-size: 3.5em !important;
        }
        .header-subtitle {
            font-size: 1.2em !important;
        }
        .stButton > button {
            padding: 15px 40px !important;
            font-size: 1.1em !important;
        }
    }
    
    /* Responsive movie cards */
    .movie-card {
        margin: 5px !important;
        padding: 0 !important;
    }
    
    .movie-title {
        word-break: break-word;
    }
    
    /* Responsive text inputs */
    .stTextInput input {
        font-size: 1em !important;
    }
    
    /* Responsive selectbox */
    .stSelectbox select {
        font-size: 1em !important;
    }
    </style>
    """

# Cache the data loading to avoid reloading on every rerun
@st.cache_resource
def load_data():
    """Load movie and similarity data - cached"""
    movies = pickle.load(open('movie_list.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    return movies, similarity

# Dynamic CSS styling based on theme
def get_theme_css():
    if st.session_state.theme == 'dark':
        return """
    <style>
    /* Dark gradient background */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        color: #e0e0e0;
    }
    
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
    }
    
    .header-subtitle {
        text-align: center;
        color: #b0b0ff;
        font-size: 1.2em;
        margin-bottom: 2rem;
    }
    
    /* Movie card styling */
    .movie-card {
        background: transparent;
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
        font-size: 0.9em;
        margin-top: 8px;
        text-align: center;
        height: 45px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .similarity-score {
        background: linear-gradient(135deg, #ff6b6b 0%, #ff8c42 100%);
        color: white;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 0.8em;
        font-weight: bold;
        margin-top: 5px;
        display: inline-block;
    }
    
    .rating-badge {
        background: #ffd700;
        color: #1a1a2e;
        padding: 4px 10px;
        border-radius: 15px;
        font-size: 0.75em;
        font-weight: bold;
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
    
    /* Filter box */
    .filter-box {
        background: transparent;
        border: none;
        border-radius: 10px;
        padding: 0px;
        margin-bottom: 0px;
    }
    
    /* Movie details panel */
    .movie-details {
        background: rgba(255, 255, 255, 0.08);
        border-left: 4px solid #ffa500;
        padding: 20px;
        border-radius: 10px;
        margin: 15px 0;
        color: #e0e0e0;
    }
    
    label {
        color: #e0e0e0 !important;
    }
    </style>
    """
    else:  # Light theme
        return """
    <style>
    /* Light background */
    .stApp {
        background: #ffffff;
        color: #1a1a1a;
    }
    
    [data-testid="stAppViewContainer"] {
        background: #ffffff;
    }
    
    [data-testid="stSidebar"] {
        background: #f5f5f5;
        border-right: 1px solid #ddd;
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
    }
    
    .header-subtitle {
        text-align: center;
        color: #333333;
        font-size: 1.2em;
        margin-bottom: 2rem;
        font-weight: 500;
    }
    
    /* Movie card styling */
    .movie-card {
        background: transparent;
        padding: 0px;
        margin: 10px;
        transition: transform 0.3s ease;
        text-align: center;
    }
    
    .movie-card:hover {
        transform: translateY(-15px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    }
    
    .movie-title {
        color: #1a1a1a;
        font-weight: 600;
        font-size: 0.9em;
        margin-top: 8px;
        text-align: center;
        height: 45px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .similarity-score {
        background: linear-gradient(135deg, #ff6b6b 0%, #ff8c42 100%);
        color: white;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 0.8em;
        font-weight: bold;
        margin-top: 5px;
        display: inline-block;
    }
    
    .rating-badge {
        background: #ffd700;
        color: #1a1a1a;
        padding: 4px 10px;
        border-radius: 15px;
        font-size: 0.75em;
        font-weight: bold;
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
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 25px rgba(255, 107, 107, 0.5);
    }
    
    /* Filter box */
    .filter-box {
        background: transparent;
        border: none;
        border-radius: 10px;
        padding: 0px;
        margin-bottom: 0px;
    }
    
    /* Movie details panel */
    .movie-details {
        background: #f9f9f9;
        border-left: 4px solid #ffa500;
        padding: 20px;
        border-radius: 10px;
        margin: 15px 0;
        color: #1a1a1a;
    }
    
    /* Text colors for labels and text */
    label {
        color: #333333 !important;
        font-weight: 500;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #1a1a1a !important;
    }
    
    /* Selectbox and input styling */
    .stSelectbox label {
        color: #333333 !important;
    }
    
    .stSlider label {
        color: #333333 !important;
    }
    
    .stTextInput label {
        color: #333333 !important;
    }
    
    /* Divider color */
    hr {
        background-color: #ddd !important;
        border: none !important;
        height: 1px !important;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #f5f5f5;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #333333;
        font-weight: 500;
    }
    </style>
    """

st.markdown(get_theme_css(), unsafe_allow_html=True)
st.markdown(get_responsive_css(), unsafe_allow_html=True)

def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
        data = requests.get(url, timeout=3)  # Reduced timeout
        data = data.json()
        if data.get('poster_path'):
            return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
        return "https://via.placeholder.com/500x750?text=No+Poster"
    except:
        return "https://via.placeholder.com/500x750?text=No+Poster"

@st.cache_data
def get_genres_list():
    """Cache genre list computation"""
    return ["All Genres"] + sorted(movies['genres'].apply(lambda x: x[0] if isinstance(x, list) and len(x) > 0 else "Unknown").unique().tolist())

@st.cache_data
def get_year_range():
    """Cache year range computation"""
    if 'release_date' in movies.columns:
        years = movies['release_date'].apply(lambda x: int(str(x)[:4]) if pd.notna(x) and str(x)[:4].isdigit() else None)
        years = years.dropna()
        min_year = int(years.min()) if len(years) > 0 else 1900
        max_year = int(years.max()) if len(years) > 0 else 2024
    else:
        min_year, max_year = 1900, 2024
    return min_year, max_year

def get_responsive_columns():
    """Get number of columns based on device (default 5 for desktop, adjustable)"""
    # Default to 5 columns, users can adjust if needed
    return 5

def filter_movies_by_criteria(genre_filter=None, year_filter=None, rating_filter=None):
    """Filter movies based on genre, year, and rating"""
    filtered = movies.copy()
    
    # Genre filter
    if genre_filter and genre_filter != "All Genres":
        filtered = filtered[filtered['genres'].apply(lambda x: genre_filter in str(x))]
    
    # Year filter
    if year_filter:
        filtered['year'] = filtered['release_date'].apply(lambda x: int(str(x)[:4]) if pd.notna(x) and str(x)[:4].isdigit() else None)
        filtered = filtered[(filtered['year'] >= year_filter[0]) & (filtered['year'] <= year_filter[1])]
    
    # Rating filter
    if rating_filter:
        filtered = filtered[filtered['vote_average'].fillna(0) >= rating_filter]
    
    return filtered

def recommend(movie, genre_filter=None, year_filter=None, rating_filter=None):
    try:
        index = movies[movies['title'] == movie].index[0]
    except:
        return [], [], []
    
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    similarity_scores = []
    
    count = 0
    for i in distances[1:]:
        if count >= 15:
            break
            
        movie_idx = i[0]
        sim_score = i[1]
        
        # Apply filters
        movie_row = movies.iloc[movie_idx]
        
        # Genre filter
        if genre_filter and genre_filter != "All Genres":
            if genre_filter not in str(movie_row.get('genres', '')):
                continue
        
        # Year filter
        if year_filter:
            try:
                movie_year = int(str(movie_row.get('release_date', ''))[:4])
                if movie_year < year_filter[0] or movie_year > year_filter[1]:
                    continue
            except:
                pass
        
        # Rating filter
        if rating_filter:
            try:
                vote_avg = float(movie_row.get('vote_average', 0))
                if vote_avg < rating_filter:
                    continue
            except:
                pass
        
        movie_id = movie_row.movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movie_row.title)
        similarity_scores.append(sim_score)
        count += 1
    
    return recommended_movie_names, recommended_movie_posters, similarity_scores

# Load data using cache
movies, similarity = load_data()

# Header with optimized theme toggle
header_col1, header_col2 = st.columns([20, 1])

with header_col1:
    st.markdown("<div class='header-title'>🎬 Movie Recommender System</div>", unsafe_allow_html=True)
    st.markdown("<div class='header-subtitle'>Discover your next favorite movie! 🍿</div>", unsafe_allow_html=True)

with header_col2:
    st.write("")
    st.write("")
    if st.button("🌙" if st.session_state.theme == 'light' else "☀️", key="theme_btn", help="Toggle Theme"):
        st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
        st.rerun()

st.divider()

# Sidebar with filters
st.sidebar.markdown("### 🎯 Filters")
st.sidebar.markdown("<div class='filter-box'>", unsafe_allow_html=True)

# Genre filter
genres_list = get_genres_list()
selected_genre = st.sidebar.selectbox("🎭 Genre", genres_list, key="genre_filter")

# Year range filter
min_year, max_year = get_year_range()
year_range = st.sidebar.slider("📅 Release Year", min_year, max_year, (min_year, max_year), key="year_filter")

# Rating filter
min_rating = st.sidebar.slider("⭐ Minimum Rating", 0.0, 10.0, 0.0, step=0.5, key="rating_filter")

st.sidebar.markdown("</div>", unsafe_allow_html=True)

# Get filtered movies for selectbox
genre_filter_for_selectbox = None if selected_genre == "All Genres" else selected_genre
filtered_movies_for_selectbox = filter_movies_by_criteria(genre_filter_for_selectbox, year_range, min_rating)
movie_titles_list = ["🎬 All Movies"] + list(filtered_movies_for_selectbox['title'].values) if len(filtered_movies_for_selectbox) > 0 else ["🎬 All Movies"] + list(movies['title'].values)

# Main navigation tabs
tab1 = st.tabs(["🎥 Recommendations"])[0]

with tab1:
    # Main content
    col1, col2 = st.columns([3, 1])

    with col1:
        selected_movie = st.selectbox(
            "🎥 Select a movie:",
            movie_titles_list,
            index=0,
            help="Choose a movie to get recommendations",
            key="movie_select"
        )

    with col2:
        st.write("")
        st.write("")
        button_pressed = st.button('🎯 Get Recommendations', use_container_width=True)

    st.markdown("")

    # Show all movies by default
    if not button_pressed or selected_movie == "🎬 All Movies":
        st.markdown("---")
        st.markdown("<h2 style='text-align: center; color: #ffa500;'>🎬 Popular Movies</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #b0b0ff;'>Select a movie and click Get Recommendations</p>", unsafe_allow_html=True)
        st.markdown("")
        
        # Get filtered movies based on current filter selections
        genre_filter = None if selected_genre == "All Genres" else selected_genre
        filtered_movies_list = filter_movies_by_criteria(genre_filter, year_range, min_rating)
        
        if len(filtered_movies_list) == 0:
            st.warning("⚠️ No movies found with the selected filters. Try adjusting your filters.")
        else:
            # Limit to first 50 movies for faster loading
            top_50_movies = filtered_movies_list.head(50)
            
            # Display filtered movies in responsive grid
            cols_per_row = get_responsive_columns()
            for row in range(0, len(top_50_movies), cols_per_row):
                cols = st.columns(cols_per_row, gap="medium")
                for col_idx, col in enumerate(cols):
                    movie_idx = row + col_idx
                    if movie_idx < len(top_50_movies):
                        movie_row = top_50_movies.iloc[movie_idx]
                        with col:
                            st.markdown(f"<div class='movie-card'>", unsafe_allow_html=True)
                            st.image(fetch_poster(movie_row.movie_id), width=220)
                            st.markdown(f"<div class='movie-title'>{movie_row.title}</div>", unsafe_allow_html=True)
                            st.markdown(f"</div>", unsafe_allow_html=True)

    if button_pressed and selected_movie != "🎬 All Movies":
        genre_filter = None if selected_genre == "All Genres" else selected_genre
        recommended_names, recommended_posters, sim_scores = recommend(
            selected_movie, 
            genre_filter=genre_filter,
            year_filter=year_range,
            rating_filter=min_rating
        )
        
        if len(recommended_names) == 0:
            st.warning("⚠️ No recommendations found with the selected filters. Try adjusting your filters.")
        else:
            st.markdown("---")
            st.markdown("<h2 style='text-align: center; color: #ffa500;'>✨ Top Recommendations (Top 15) ✨</h2>", unsafe_allow_html=True)
            st.markdown("")
            
            # Display recommendations in responsive grid
            cols_per_row = get_responsive_columns()
            num_rows = (len(recommended_names) + cols_per_row - 1) // cols_per_row
            for row in range(num_rows):
                cols = st.columns(cols_per_row, gap="medium")
                for col_idx, col in enumerate(cols):
                    movie_idx = row * cols_per_row + col_idx
                    if movie_idx < len(recommended_names):
                        with col:
                            st.markdown(f"<div class='movie-card'>", unsafe_allow_html=True)
                            
                            # Movie poster
                            st.image(recommended_posters[movie_idx], width=220)
                            
                            # Movie title
                            st.markdown(f"<div class='movie-title'>{recommended_names[movie_idx]}</div>", unsafe_allow_html=True)
                            
                            st.markdown(f"</div>", unsafe_allow_html=True)
            
            # Show detailed info
            st.markdown("---")
            st.markdown("<h3 style='color: #ffa500;'>📋 Detailed Information</h3>", unsafe_allow_html=True)
            
            # Create tabs for details
            tab1_details, tab2_details, tab3_details = st.tabs(["Top 5", "Top 6-10", "Top 11-15"])
            
            with tab1_details:
                for i in range(min(5, len(recommended_names))):
                    movie_row = movies[movies['title'] == recommended_names[i]].iloc[0]
                    with st.expander(f"🎬 {recommended_names[i]} - Match: {int(sim_scores[i] * 100)}%"):
                        col1, col2 = st.columns([1, 2])
                        with col1:
                            st.image(recommended_posters[i], width=150)
                        with col2:
                            st.write(f"**Rating:** {movie_row.get('vote_average', 'N/A')} ⭐")
                            st.write(f"**Release Date:** {movie_row.get('release_date', 'N/A')}")
                            st.write(f"**Genres:** {', '.join(movie_row.get('genres', []))}")
                            st.write(f"**Overview:** {movie_row.get('overview', 'N/A')[:200]}...")
            
            with tab2_details:
                for i in range(5, min(10, len(recommended_names))):
                    movie_row = movies[movies['title'] == recommended_names[i]].iloc[0]
                    with st.expander(f"🎬 {recommended_names[i]} - Match: {int(sim_scores[i] * 100)}%"):
                        col1, col2 = st.columns([1, 2])
                        with col1:
                            st.image(recommended_posters[i], width=150)
                        with col2:
                            st.write(f"**Rating:** {movie_row.get('vote_average', 'N/A')} ⭐")
                            st.write(f"**Release Date:** {movie_row.get('release_date', 'N/A')}")
                            st.write(f"**Genres:** {', '.join(movie_row.get('genres', []))}")
                            st.write(f"**Overview:** {movie_row.get('overview', 'N/A')[:200]}...")
            
            with tab3_details:
                for i in range(10, min(15, len(recommended_names))):
                    movie_row = movies[movies['title'] == recommended_names[i]].iloc[0]
                    with st.expander(f"🎬 {recommended_names[i]} - Match: {int(sim_scores[i] * 100)}%"):
                        col1, col2 = st.columns([1, 2])
                        with col1:
                            st.image(recommended_posters[i], width=150)
                        with col2:
                            st.write(f"**Rating:** {movie_row.get('vote_average', 'N/A')} ⭐")
                            st.write(f"**Release Date:** {movie_row.get('release_date', 'N/A')}")
                            st.write(f"**Genres:** {', '.join(movie_row.get('genres', []))}")
                            st.write(f"**Overview:** {movie_row.get('overview', 'N/A')[:200]}...")
