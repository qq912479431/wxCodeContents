from datetime import datetime
from flask import render_template, request
from run import app
from wxcloudrun.dao import delete_counterbyid, query_counterbyid, insert_counter, update_counterbyid
from wxcloudrun.model import Counters
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response
import pymysql
def sqlInput(sql):
    db =pymysql.connect(host="sh-cynosdbmysql-grp-a3li6o72.sql.tencentcdb.com",user="root",
                   password="x.Y(2hBq",database="flask_demo",
                   charset="utf8",port=23610)
#2.利用db方法创建游标对象
    cur = db.cursor()
    cur.execute(sql)
    re=cur.fetchall()
    d=[]
    for i in re:
        l={}
        for b in range(len(i)):
            l[cur.description[b][0]]=str(i[b])
        d.append(l)
    cur.close()
    db.close()
    return d
@app.route('/')
def index():
    """
    :return: 返回index页面
    """
    return render_template('index.html')


@app.route('/api/maxId', methods=['GET'])
def getMaxId():
    dt=sqlInput('select max(id) as maxId from wxCodeData')
    return make_succ_response(dt[0]['maxId'])



@app.route('/api/count', methods=['GET'])
def get_count():
    """
    :return: 计数的值
    """
    counter = Counters.query.filter(Counters.id == 1).first()
    return make_succ_response(0) if counter is None else make_succ_response(counter.count)
