import bs4
import re
import urllib.request
import urllib.error
import sqlite3
import xlwt

# Base URL for scraping
base_url = "https://movie.douban.com/top250?start="

def main():
    # Step 1: Crawl web data
    data_list = get_data(base_url)

    # Optional: Save to Excel
    # save_path = "./Douban_Top250.xls"
    # save_data_to_excel(data_list, save_path)

    # Step 3: Save data to SQLite database
    db_path = "movie.db"
    save_data_to_db(data_list, db_path)


# Regular expression patterns
find_link = re.compile(r'<a href=\"(.*?)\">')                         # Movie link
find_img_src = re.compile(r'<img.*src=\"(.*?)\"', re.S)              # Poster image URL
find_title = re.compile(r'<span class="title">(.*)</span>')          # Movie title(s)
find_rating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')  # Rating
find_votes = re.compile(r'<span>(\d*)人评价</span>')                  # Number of votes
find_summary = re.compile(r'<span class="inq">(.*)</span>')          # Short description
find_info = re.compile(r'<p class="">(.*?)</p>', re.S)               # Detailed info


# Fetch and parse data from all pages
def get_data(base_url):
    data_list = []
    for i in range(10):  # 10 pages, 25 movies per page
        url = base_url + str(i * 25)
        html = ask_url(url)

        # Parse HTML using BeautifulSoup
        soup = bs4.BeautifulSoup(html, "html.parser")
        for item in soup.find_all('div', class_="item"):
            movie_data = []
            item = str(item)

            # Extract each field using regex
            link = re.findall(find_link, item)[0]
            movie_data.append(link)

            img_src = re.findall(find_img_src, item)[0]
            movie_data.append(img_src)

            titles = re.findall(find_title, item)
            if len(titles) == 2:
                cname = titles[0]
                ename = titles[1].replace("/", "")
                movie_data.extend([cname, ename])
            else:
                movie_data.extend([titles[0], ""])

            rating = re.findall(find_rating, item)[0]
            movie_data.append(rating)

            votes = re.findall(find_votes, item)[0]
            movie_data.append(votes)

            summary = re.findall(find_summary, item)
            movie_data.append(summary[0].replace("。", "") if summary else "")

            info = re.findall(find_info, item)[0]
            info = re.sub(r'<br(\s+)?/>(\s+)?', " ", info)
            movie_data.append(info.strip())

            data_list.append(movie_data)

    return data_list


# Simulate browser request and return HTML content
def ask_url(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"
    }
    request = urllib.request.Request(url, headers=headers)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(f"Error code: {e.code}")
        if hasattr(e, "reason"):
            print(f"Reason: {e.reason}")
    return html


# Save data to an Excel file
def save_data_to_excel(data_list, save_path):
    print("Saving to Excel...")

    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('Douban Top 250 Movies', cell_overwrite_ok=True)
    columns = ("Movie URL", "Image URL", "Chinese Title", "Foreign Title",
               "Rating", "Votes", "Summary", "Additional Info")

    for col_idx in range(len(columns)):
        sheet.write(0, col_idx, columns[col_idx])

    for row_idx, data in enumerate(data_list):
        print(f"Writing row {row_idx + 1}")
        for col_idx in range(len(data)):
            sheet.write(row_idx + 1, col_idx, data[col_idx])

    book.save(save_path)
    print("Excel file saved.")


# Save data to SQLite database
def save_data_to_db(data_list, db_path):
    print("Saving to database...")
    init_db(db_path)
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    for data in data_list:
        for index in range(len(data)):
            if index in [4, 5]:  # score and rated are numeric
                continue
            data[index] = '"' + data[index].replace('"', '""') + '"'

        sql = '''
            INSERT INTO movie250 (
                info_url, pic_url, cname, ename, score, rated, introduction, info
            ) VALUES (%s)
        ''' % ",".join(data)

        print(sql)
        cur.execute(sql)
        conn.commit()

    cur.close()
    conn.close()
    print("Database save completed.")


# Initialize the SQLite database schema
def init_db(db_path):
    sql = '''
        CREATE TABLE IF NOT EXISTS movie250 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            info_url TEXT,
            pic_url TEXT,
            cname TEXT,
            ename TEXT,
            score NUMERIC,
            rated NUMERIC,
            introduction TEXT,
            info TEXT
        )
    '''
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    main()
    print("Scraping completed.")
