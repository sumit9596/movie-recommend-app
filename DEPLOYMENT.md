# 🎬 Movie Recommender System - Deployment Guide

## 📋 Overview
This is a Streamlit-based Movie Recommender System that uses cosine similarity to suggest movies based on user preferences.

### Features
- 🎭 Movie recommendations based on content similarity
- 🎯 Multiple filters (Genre, Year, Rating)
- 🌙/☀️ Dark/Light theme toggle
- 📱 Fully responsive (Mobile, Tablet, Desktop)
- ⚡ Optimized with caching for fast performance

---

## 🚀 Quick Start (Local)

### Prerequisites
- Python 3.8+
- pip or conda

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd ML_Project
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**
   ```bash
   streamlit run app.py
   ```

5. **Open in browser**
   - Local: http://localhost:8501
   - Network: http://<your-ip>:8501

---

## 🌐 Deploy to Heroku

### Prerequisites
- Heroku account (free tier available)
- Heroku CLI installed
- Git installed

### Deployment Steps

1. **Login to Heroku**
   ```bash
   heroku login
   ```

2. **Create Heroku app**
   ```bash
   heroku create your-app-name
   ```

3. **Initialize Git repository** (if not already done)
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Movie Recommender App"
   ```

4. **Add Heroku remote**
   ```bash
   heroku git:remote -a your-app-name
   ```

5. **Deploy to Heroku**
   ```bash
   git push heroku main
   # or
   git push heroku master
   ```

6. **View your live app**
   ```bash
   heroku open
   ```

   Or visit: `https://your-app-name.herokuapp.com`

---

## 📦 Project Files

```
ML_Project/
├── app.py                  # Main Streamlit app
├── movie_list.pkl          # Pre-processed movies dataset
├── similarity.pkl          # Similarity matrix (cached)
├── tmdb_5000_movies.csv    # Raw movie data
├── tmdb_5000_credits.csv   # Raw credits data
├── requirements.txt        # Python dependencies
├── Procfile                # Heroku deployment config
├── .gitignore              # Git ignore rules
└── .streamlit/
    └── config.toml         # Streamlit configuration
```

---

## ⚙️ Configuration

### Environment Variables (Optional)
For production, you can set these in Heroku:
```bash
heroku config:set VAR_NAME=value
```

### Streamlit Config
Edit `.streamlit/config.toml` for customization:
- Theme colors
- Font settings
- Server configuration
- Logger level

---

## 🔧 Troubleshooting

### Issue: App too slow
**Solution:** Make sure caching is enabled (already in code with `@st.cache_resource`)

### Issue: Large file size
**Solution:** The `.pkl` files are large. Ensure `.gitignore` is working:
```bash
git status  # Check if .csv and .pkl files are ignored
```

### Issue: Heroku deployment fails
**Check logs:**
```bash
heroku logs --tail
```

**Common fixes:**
- Ensure `requirements.txt` is in root directory
- Check `Procfile` syntax (no extra spaces/lines)
- Verify Python version compatibility

---

## 📊 Data Processing

The app uses pre-processed pickle files:
- **movie_list.pkl**: Processed movies with tags
- **similarity.pkl**: 4865x4865 cosine similarity matrix

These are generated from:
- `tmdb_5000_movies.csv`: 5000 movies metadata
- `tmdb_5000_credits.csv`: Cast and crew information

---

## 🎨 Features Explained

### Dark/Light Theme
Click the 🌙/☀️ button at top-right to toggle themes

### Filters
- **Genre**: Filter by movie genre
- **Release Year**: Filter by year range
- **Minimum Rating**: Filter by vote average

### Responsive Design
- **Mobile** (< 600px): Single column layout
- **Tablet** (600-1000px): 3-column layout
- **Desktop** (> 1000px): 5-column layout

---

## 📈 Performance Metrics

- **Initial Load**: ~2-3 seconds
- **Theme Toggle**: < 500ms
- **Filter Change**: ~1 second
- **Recommendations**: ~2 seconds (with 15 results)

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

---

## 📄 License

This project uses TMDB movie data and is for educational purposes.

---

## 📞 Support

For issues or questions:
1. Check Heroku logs: `heroku logs --tail`
2. Test locally: `streamlit run app.py`
3. Check requirements.txt matches installed packages

---

**Deployed on:** Heroku  
**Built with:** Streamlit, Python, Pandas, Scikit-learn  
**Last Updated:** April 2026
