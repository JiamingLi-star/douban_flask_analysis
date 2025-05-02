import bs4
import re
import urllib.request,urllib.error
import sqlite3
import xlwt

baseurl = "https://movie.douban.com/top250?start="
def main():
    #1.爬取网页
    datalist = getData(baseurl)
    #3.保存数据

    #savepath = ".//豆瓣电影Top250.xls"     #保存到Excel
    #saveData(datalist,savepath)

    dbpath = "movie.db"
    saveDataDB(datalist,dbpath)


#创建正则表达式对象，表示规则（字符串模式）

#影片超链接的规则
findLink = re.compile(r'<a href=\"(.*?)\">')

#影片图片的规则
findImgSrc = re.compile(r'<img.*src=\"(.*?)\"', re.S)  #re.s是让换行符包含在字符中

#影片片名
findTitle = re.compile(r'<span class="title">(.*)</span>')

#影片评分
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')

#评价人数
findJudge = re.compile(r'<span>(\d*)人评价</span>')


#概况
findInq = re.compile(r'<span class="inq">(.*)</span>')

#影片相关内容
findBd = re.compile(r'<p class="">(.*?)</p>', re.S)


# 爬取网页
def getData(url):
    datalist = []
    for i in range(0,10):   #调取网页信息10次
        url = baseurl + str(i*25)
        html = askURL(url)  #保存获取到的网页源码

        #2.解析数据
        soup = bs4.BeautifulSoup(html,"html.parser") #用来解析 HTML/XML 文本并生成一个便于操作和查询的解析树对象
        for item in soup.find_all('div',class_="item"):  #查找符合要求的字符串
            data = []   #保存一部电影的所有信息
            item = str(item)

            #获取影片的超链接
            link = re.findall(findLink, item)[0]        #用正则表达式查找指定的字符串
            data.append(link)                           #添加链接
            imgSrc = re.findall(findImgSrc, item)[0]
            data.append(imgSrc)                         #添加图片
            title = re.findall(findTitle, item)
            if len(title) == 2:                        #添加片名，可能只有一个中文名而没有外文名
                Ctitle = title[0]
                data.append(Ctitle)                     #添加中文名
                Otitle = title[1].replace("/","")       #去掉无关符号
                data.append(Otitle)                     #添加外文名
            else:
                data.append(title[0])
                data.append(' ')                        #外文名留空

            Rating = re.findall(findRating, item)[0]
            data.append(Rating)                         #添加评分

            JudgeNum = re.findall(findJudge, item)[0]
            data.append(JudgeNum)                       #添加评价人数

            Inq = re.findall(findInq, item)
            if len(Inq) != 0:
                inq = Inq[0].replace("。","")           #去掉句号
                data.append(inq)                        #添加概述
            else:
                data.append(' ')                        #没有则留空

            Bd = re.findall(findBd, item)[0]
            Bd = re.sub(r'<br(\s+)?/>(\s+)?'," ",Bd) #删掉换行符之类的东西
            data.append(Bd.strip())                      #添加相关内容,".strip()"用来去掉前后的空格

            datalist.append(data)

    # for data in datalist:
    #     print(data)  # 每部电影作为一行输出

    return datalist


#获取一个指定URL网页内容
def askURL(url):
    #模拟浏览器头部向服务器发信息
    head = {
        "User-Agent":"Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 131.0.0.0 Safari / 537.36 Edg / 131.0.0.0"
    }
    #告诉服务我们是什么类型的浏览器，本质上是告诉浏览器我们可以接受什么样的信息
    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        print(e.code)
        print(e.reason)
    return html

# 保存数据
def saveData(datalist,savepath):
    print("save...")

    book = xlwt.Workbook(encoding='utf-8',style_compression=0)  # 创建workbook对象
    sheet = book.add_sheet('豆瓣电影Top250',cell_overwrite_ok=True)  # 创建一个表单名为sheet1
    col = ("电影详情链接","图片链接","电影中文名","电影外文名","评分","评价数","概括","相关信息")
    for i in range(0,8):
        sheet.write(0,i,col[i])         #列名
    for i in range(0,250):
        print("第%d条"%(i+1))
        data = datalist[i]
        for j in range(0,8):
            sheet.write(i+1,j,data[j])   #数据

    book.save(savepath)            #保存到xwlt


def saveDataDB(datalist,dbpath):
    print("save...")
    init_db(dbpath)
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()

    for data in datalist:
        for index in range(len(data)):
            if index == 4 or index == 5:
                continue
            data[index] = '"'+ data[index] +'"'
        sql = '''
            insert into movie250(
            info_url,pic_url,cname,ename,score,rated,introduction,info)
            values (%s)'''%",".join(data)
        print(sql)
        cur.execute(sql)
        conn.commit()
    cur.close()
    conn.close()



def init_db(dbpath):
    sql = '''
        create table movie250
        (
        id integer primary key autoincrement,
        info_url text,
        pic_url text,
        cname varchar,
        ename varchar,
        score numeric,
        rated numeric,
        introduction text,
        info text
        )
    '''   #创建数据表
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    main()
    # init_db("movie.db")
    print("爬取完毕")
