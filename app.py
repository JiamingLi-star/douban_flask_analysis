import sqlite3

from flask import Flask,render_template,request

app = Flask(__name__)


@app.route('/')
def index():  # put application's code here
    return render_template('index.html')

@app.route('/index')
def home():
    return render_template('index.html')


@app.route('/movie')
def movie():
    datalist = []
    con = sqlite3.connect('movie.db')
    cur = con.cursor()

    # 获取当前页码，默认为第 1 页
    page = request.args.get('page', 1, type=int)
    per_page = 10  # 每页显示 10 条数据

    # 查询所有数据
    sql = "SELECT * FROM movie250"
    data = cur.execute(sql)
    for i in data:
        datalist.append(i)

    cur.close()
    con.close()

    # 分页数据
    total_movies = len(datalist)  # 总电影数
    total_pages = (total_movies + per_page - 1) // per_page  # 总页数

    start = (page - 1) * per_page
    end = start + per_page
    page_movies = datalist[start:end]  # 当前页数据

    return render_template(
        'movie.html',
        movies=page_movies,
        page=page,
        total_pages=total_pages
    )

    return render_template('movie.html')

@app.route('/score')
def score():
    score = [] #评分有多少种
    num = []   #每个评分所统计出的电影数量
    con = sqlite3.connect('movie.db')
    cur = con.cursor()
    sql = ("SELECT score,count(score) FROM movie250 GROUP BY score")
    data = cur.execute(sql)
    for item in data:
        score.append(str(item[0]))
        num.append(item[1])

    cur.close()
    con.close()
    return render_template('score.html', score=score, num=num)

@app.route('/word')
def word():
    return render_template('word.html')

@app.route('/teams')
def teams():
    return render_template('teams.html')



if __name__ == '__main__':
    app.run()
