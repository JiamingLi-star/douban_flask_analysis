# Douban Movie Data Visualization 🎬

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Web%20Framework-lightgrey)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

This is a full-stack mini project that crawls data from **Douban Top 250 Movies**, stores it in a local **SQLite** database, and presents the results via a **Flask** web application.

> ✨ This is my first full-stack Python web project. I'm excited to share it, and I welcome anyone to use, modify, or suggest improvements!

---

## 📌 Features

- 🎯 **Crawler**: Automatically fetches movie title, rating, number of reviews, description, and more
- 🛢️ **Database**: Stores data in a `movie.db` SQLite database
- 🌐 **Web App**: Built with Flask, with multiple pages and routing
- 📊 **Visualization**:
  - Paginated movie list table
  - ECharts bar chart for rating distribution
  - Word cloud of movie descriptions
- 👤 **Teams Page**: A fun mock display of fictional team members

---

## 🔧 Tech Stack

- Python 3.9+
- Flask
- SQLite3
- BeautifulSoup (for HTML parsing)
- ECharts (rating visualization)
- WordCloud (static image generation)

---

## 🚀 How to Run

1. **Install dependencies**

```bash
pip install flask bs4 xlwt
```

2. **Run the crawler**

```bash
python crawler.py
```

This will populate `movie.db`.

3. **Start the Flask app**

```bash
python app.py
```

4. **Visit in browser**

Go to [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🗂 Project Structure

```
├── app.py                 ← Flask backend
├── crawler.py             ← Web scraper and DB writer
├── movie.db               ← Local SQLite database
├── templates/             ← HTML templates (Jinja2)
│   ├── index.html
│   ├── movie.html
│   ├── score.html
│   ├── word.html
│   └── teams.html
├── static/                ← CSS / JS / images
│   └── ...
└── README.md              ← This file
```

---

## 📷 Screenshots

> You can include screenshots of the movie list, chart, and word cloud pages here!

---

## 📄 License

This project is licensed under the MIT License.

