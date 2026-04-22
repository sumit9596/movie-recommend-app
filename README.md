# 🎬 Movie Recommender System

A content-based movie recommendation system built with Streamlit using TMDB movie data.

## 🌐 Live Deployment

**App URL:** https://movie-recommend-app-9596.streamlit.app/

## 📋 Features

- 🎭 Movie recommendations based on content similarity (cosine similarity)
- 🎯 Multiple filters (Genre, Year, Rating)
- 🌙/☀️ Dark/Light theme toggle
- 📱 Fully responsive (Mobile, Tablet, Desktop)
- ⚡ Optimized with caching for fast performance
- 🎬 Movie posters and details

## 🛠 Tech Stack

- **Frontend:** Streamlit
- **Backend:** Python
- **Data Processing:** Pandas, NumPy
- **Machine Learning:** Cosine Similarity (scikit-learn)
- **API:** TMDB (The Movie Database)

## 📊 Dataset

- **tmdb_5000_movies.csv** - Movie metadata (5000 movies)
- **tmdb_5000_credits.csv** - Cast and crew information
- **movie_list.pkl** - Pre-processed movies with tags
- **similarity.pkl** - 4865x4865 cosine similarity matrix

## 🚀 How to Run Locally

```bash
# Clone the repository
git clone https://github.com/sumit9596/movie-recommend-app.git
cd movie-recommend-app

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 📦 Dependencies

- streamlit>=1.28.0
- requests>=2.31.0
- pandas>=2.0.0
- numpy>=1.23.0

## 🔗 GitHub Repository

https://github.com/sumit9596/movie-recommend-app

## 📝 License

This project is open source and available under the MIT License.

---

**Created with ❤️ by Sumit**
