import sqlite3  # Import SQLite library for database interactions
from flask import Flask, render_template, request  # Import necessary Flask modules

app = Flask(__name__)  # Create Flask app instance


@app.route('/')
def index():
    # Render the index (home) page
    return render_template('index.html')


@app.route('/index')
def home():
    # Render the index page (same as root path)
    return render_template('index.html')


@app.route('/movie')
def movie():
    datalist = []  # List to store movie data
    con = sqlite3.connect('movie.db')  # Connect to SQLite database
    cur = con.cursor()  # Create a cursor object for executing SQL queries

    # Get the current page number from the query parameter, default is 1
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Number of items per page

    # Fetch all movie records from the movie250 table
    sql = "SELECT * FROM movie250"
    data = cur.execute(sql)
    for i in data:
        datalist.append(i)  # Append each record to the datalist

    cur.close()  # Close the cursor
    con.close()  # Close the database connection

    # Calculate pagination details
    total_movies = len(datalist)  # Total number of movies
    total_pages = (total_movies + per_page - 1) // per_page  # Total number of pages

    # Get movie data for the current page
    start = (page - 1) * per_page
    end = start + per_page
    page_movies = datalist[start:end]  # Slice the data for the current page

    # Render the movie.html template with paginated data
    return render_template(
        'movie.html',
        movies=page_movies,
        page=page,
        total_pages=total_pages
    )

    # This line is unreachable and can be removed
    return render_template('movie.html')


@app.route('/score')
def score():
    score = []  # List to store distinct score values
    num = []  # List to store count of movies for each score

    con = sqlite3.connect('movie.db')  # Connect to SQLite database
    cur = con.cursor()  # Create a cursor object

    # SQL query to group movies by score and count the number per group
    sql = "SELECT score, count(score) FROM movie250 GROUP BY score"
    data = cur.execute(sql)
    for item in data:
        score.append(str(item[0]))  # Append score as string
        num.append(item[1])  # Append corresponding count

    cur.close()  # Close cursor
    con.close()  # Close database connection

    # Render the score.html template with score distribution data
    return render_template('score.html', score=score, num=num)


@app.route('/word')
def word():
    # Render the word cloud page
    return render_template('word.html')


@app.route('/teams')
def teams():
    # Render the teams information page
    return render_template('teams.html')


if __name__ == '__main__':
    app.run()  # Run the Flask development server
