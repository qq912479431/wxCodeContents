from datetime import datetime
from flask import Flask,request

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
    db.commit()
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



@app.route('/api/add', methods=['POST'])
def addData():
    try:
        basedata=request.get_json()['basedata']
    except:
        return make_succ_response(str(request.get_json()))
    sqlInput("INSERT INTO `wxCodeData` (`base64data`, `isuse`) VALUES ('"+basedata+"', 0)")
    return make_succ_response('ok')

@app.route('/api/getCodeData', methods=['GET'])
def getCodeData():
    openid=request.headers['X-Wx-Openid']
    id=request.args.get('id')
    dt=sqlInput('select * from wxCodeData where id ='+str(id))
    if len(dt)==0:
        return make_succ_response('nofind')
    else:
        dt[0]['login_openid']=openid
        return make_succ_response(dt[0])

@app.route('/api/update', methods=['POST'])
def updateContent():
    id=request.get_json()['id']
    content=request.get_json()['content']
    open_id=request.headers['X-Wx-Openid']
    try:
        sqlInput('update wxCodeData set content="'+str(content)+'",open_id="'+str(open_id)+'" where id='+str(id))
        return make_succ_response('ok')
    except:
        return make_succ_response('更新失败')
