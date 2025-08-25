# Anime API (Flask + MongoDB Atlas)

This is a simple Flask-based API connected to MongoDB Atlas, deployed using [Render](https://render.com/). It supports basic operations such as listing featured products (e.g. anime items), querying MongoDB collections, and serving endpoints via a lightweight backend.

---

## Features

- Python Flask backend
- MongoDB Atlas cloud database
- Environment variable management using `.env` and Render Env tab
- Render cloud deployment
- MongoDB Compass-compatible connection

---

## 🚀 Live Demo

Deployed on **Render**:  
👉 [https://animecosplay.onrender.com](https://animecosplay.onrender.com)

---

## 🛠 Technologies

- Python 3.11+
- Flask
- PyMongo
- MongoDB Atlas
- Render
- `python-dotenv` (for local development)

---

## 📁 Project Structure

.
├── app.py # Main Flask app
├── .env # Local dev environment variables (not pushed)
├── requirements.txt # Python dependencies
├── README.md
└── ...

---

## 💾 Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/your-username/anime-api.git
cd anime-api
```

### 2. Create & activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```


### 3. Install dependencies
```bash
pip install -r requirements.txt
```


### 4. Add a .env file
Create a .env file in the root directory with:

```env
MONGO_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority
```
###  Use your MongoDB Atlas connection string
###  Never commit this file — it’s already in .gitignore

### 5. Run the app locally
```bash
python app.py
```
Then open http://localhost:5000
