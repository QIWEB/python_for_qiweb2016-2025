# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#qiweb 20180902 16:26
# 读取数据实现增删改查api接口



# 使用 Python 和 Flask 设计 RESTful API
# http://www.pythondoc.com/flask-restful/first.html
# Flask 框架的简介
# 如果你读过 Flask Mega-Tutorial 系列，就会知道 Flask 是一个简单却十分强大的 Python web 框架。
# 什么是一个 RESTful 的 web service？
# RESTful web services 概念的核心就是“资源”。 资源可以用 URI 来表示。客户端使用 HTTP 协议定义的方法来发送请求到这些 URIs，当然可能会导致这些被访问的”资源“状态的改变。
# 我们的任务资源将要使用 HTTP 方法如下:
# ==========  ===============================================  =============================
# HTTP 方法   URL                                              动作
# ==========  ===============================================  ==============================
# GET         http://[hostname]/qiweb/api/v1.0/tasks            检索任务列表
# GET         http://[hostname]/todo/api/v1.0/tasks/[task_id]  检索某个任务
# POST        http://[hostname]/todo/api/v1.0/tasks            创建新任务
# PUT         http://[hostname]/todo/api/v1.0/tasks/[task_id]  更新任务
# DELETE      http://[hostname]/todo/api/v1.0/tasks/[task_id]  删除任务
# ==========  ================================================ =============================
# 我们定义的任务有如下一些属性:
# id: 任务的唯一标识符。数字类型。
# title: 简短的任务描述。字符串类型。
# description: 具体的任务描述。文本类型。
# done: 任务完成的状态。布尔值。

#!flask/bin/python
import sqlite3,json

from flask import Flask,jsonify,abort,make_response,request,url_for

from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

#我们现在拥有一个 get_tasks 的函数，访问的 URI 为 /todo/api/v1.0/tasks，并且只允许 GET 的 HTTP 方法。
@app.route('/qiweb/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    # 我们使用    JSON    数据格式来响应，Flask    的    jsonify    函数从我们的数据结构中生成。
    # return jsonify({'tasks': tasks})
    #转换id 成url比较直观
    return jsonify({'tasks': map(make_public_task, tasks)})
# $ curl -i http://localhost:5000/qiweb/api/v1.0/tasks

#URL 中任务的 id，接着 Flask 把它转换成 函数中的 task_id 的参数。
@app.route('/qiweb/api/v1.0/tasks/<int:task_id>', methods=['GET'])
@auth.login_required #需要http用户名和密码验证
def get_task(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)#404页面
    return jsonify({'task': task[0]})

#这是因为 Flask 按照默认方式生成 404 响应。由于这是一个 Web service 客户端希望我们总是以 JSON 格式回应，所以我们需要改善我们的 404 错误处理程序:
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

# 只有当请求以 JSON 格式形式，request.json 才会有请求的数据。如果没有数据，或者存在数据但是缺少 title 项，我们将会返回 400，这是表示请求无效
# 接着我们会创建一个新的任务字典，使用最后一个任务的 id + 1 作为该任务的 id。我们允许 description 字段缺失，并且假设 done 字段设置成 False。
# 我们把新的任务添加到我们的任务数组中，并且把新添加的任务和状态 201 响应给客户端。
@app.route('/qiweb/api/v1.0/tasks', methods=['POST'])
#curl -i -H "Content-Type: application/json" -X POST -d "{"""title""":"""Read a book"""}" http://localhost:5000/todo/api/v1.0/tasks
@auth.login_required #需要http用户名和密码验证
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201
#更新
@auth.login_required #需要http用户名和密码验证
@app.route('/qiweb/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})

#删除
@auth.login_required #需要http用户名和密码验证
@app.route('/qiweb/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])

def delete_task(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})

# 优化 web service 接口
# 目前 API 的设计的问题就是迫使客户端在任务标识返回后去构造 URIs。这对于服务器是十分简单的，但是间接地迫使客户端知道这些 URIs 是如何构造的，这将会阻碍我们以后变更这些 URIs。
# 不直接返回任务的 ids，我们直接返回控制这些任务的完整的 URI，以便客户端可以随时使用这些 URIs。为此，我们可以写一个小的辅助函数生成一个 “公共” 版本任务发送到客户端:

def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task

#欢迎首页
@app.route('/')
def index():
    return make_response(jsonify({'qiweb': 'Hello, World!','hi':'welcome to python flask restful api for qiweb'}))
    # return "Hello, World!"
# 加强 RESTful web service 的安全性

@auth.get_password
def get_password(username):
    if username == 'qiweb':
        return 'python'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)
# 获取所有api
@app.route('/all_api', methods=['GET'])
def all_api():
    # return str(app.url_map).replace(',','<br>')
    #print app.url_map.converters['string']
    return jsonify({'msg': str(app.url_map).replace(',','<br>')})
    # return jsonify(app.url_map)


def extc_sql(sql):
    #os.path.exists('windowskey.db')
    conn = sqlite3.connect('windowskey.db')
    print "Opened database successfully";
    c = conn.cursor()
    c.execute(sql)
    print "db  successfully";
    conn.commit()
    conn.close()

#查询数据库
def query_sql(conn,sql):
    #os.path.exists('windowskey.db')

    c = conn.cursor()
    res=c.execute(sql)
    print "db query successfully";

    return res


@app.route('/qiweb/api/v1.0/emails', methods=['GET'])
def get_emails():
    emails = []
    conn = sqlite3.connect('windowskey.db')
    qsql='select * from email'
    cursor=query_sql(conn,qsql)
    for row in cursor:
        email = {
            'id': row[0],
            'email': row[1],
            'password': row[2],
            'add_date': row[3],
            'update_date': row[4],
            'state': row[5],
            'type': row[6]
        }
        emails.append(email)
    conn.close()
    # 我们使用    JSON    数据格式来响应，Flask    的    jsonify    函数从我们的数据结构中生成。
    # return jsonify({'tasks': tasks})
    #转换id 成url比较直观
    return jsonify({'email': map(make_public_email, emails)})
def make_public_email(email):
    new_task = {}
    for field in email:
        if field == 'id':
            new_task['uri'] = url_for('get_email', email_id=email['id'], _external=True)
        else:
            new_task[field] = email[field]
    return new_task

def getEmailfromDb(email_id):
    conn = sqlite3.connect('windowskey.db')
    qsql = 'select * from email where id=%d' % email_id
    cursor = query_sql(conn, qsql)
    email = {}
    for row in cursor:
        email = {
            'id': row[0],
            'email': row[1],
            'password': row[2],
            'add_date': row[3],
            'update_date': row[4],
            'state': row[5],
            'type': row[6]
        }
    conn.close()
    return email

#URL 中任务的 id，接着 Flask 把它转换成 函数中的 task_id 的参数。
@app.route('/qiweb/api/v1.0/emails/<int:email_id>', methods=['GET'])
@auth.login_required #需要http用户名和密码验证
def get_email(email_id):
    email= getEmailfromDb(email_id)
    if len(email) == 0:
        abort(404)#404页面
    return jsonify({'email': email})

#更新
@auth.login_required #需要http用户名和密码验证
@app.route('/qiweb/api/v1.0/emails/<int:email_id>', methods=['PUT'])
def update_email(email_id):
    email = getEmailfromDb(email_id)
    if len(email) == 0:
        abort(404)  # 404页面
    if not request.json:
        abort(400)
    if 'email' in request.json and type(request.json['email']) != unicode:
        abort(400)
    if 'password' in request.json and type(request.json['password']) is not unicode:
        abort(400)
    if 'add_date' in request.json and type(request.json['add_date']) != unicode:
        abort(400)
    if 'update_date' in request.json and type(request.json['update_date']) is not unicode:
        abort(400)
    if 'state' in request.json and type(request.json['state']) != unicode:
        abort(400)
    if 'type' in request.json and type(request.json['type']) is not unicode:
        abort(400)
    updatesql="update email set email='%s',password='%s',add_date='%s',update_date='%s',state='%s',type='%s' where id=%d"%(
        request.json.get('email', email['email']),
        request.json.get('password', email['password']),
        request.json.get('add_date', email['add_date']),
        request.json.get('update_date', email['update_date']),
        request.json.get('state', email['state']),
        request.json.get('type', email['type']),
        email_id,
    )
    extc_sql(updatesql)
    return jsonify({'result': True,'msg':'update email id %s successfully'%email_id})

@app.route('/qiweb/api/v1.0/emails/<int:email_id>', methods=['DELETE'])
def delete_email(email_id):
    dsql = 'delete from email where id=%d' % email_id
    extc_sql(dsql)
    return jsonify({'result': True,'msg':'delete email id %s successfully'%email_id})

import random
import string
import datetime
#生成随机邮箱和密码
seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+=-"
types=['windows 10','office 2013','office 2016','windows xp','windows 7','office for mac','office 365']
states=['其他','未提取','已提取']

@app.route('/add_test', methods=['GET'])
def add_email_data():
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # 现在
    insert2 = '''
        INSERT INTO email (email,password,add_date,update_date,state,type) 
         
         VALUES ('%s@outlook.com', '%s', '%s', '%s', '%s','%s' ) ;
         
        '''%(''.join(random.sample(string.ascii_letters + string.digits, 8)),
             ''.join(random.sample(string.ascii_letters + string.digits, 10)),
             nowTime,nowTime
             ,states[random.randint(0,len(states))]
                           , types[random.randint(0, len(types))]
             )
    # VALUES ('tsoasislouqjbo@outlook.com', 'pEMucs0AwCWTW', '2018-09-02 22:12:12', '2018-09-05 12:12:12', '未提取','Windows 10' ) ;
    extc_sql(insert2)
    return jsonify({'msg': 'add testemail successfully'})
@app.route('/init_db', methods=['GET'])
def init_db():
    createEmail = '''CREATE TABLE email ( 
            id          INTEGER         PRIMARY KEY AUTOINCREMENT
                                        NOT NULL
                                        UNIQUE,
            email       CHAR( 50 )      NOT NULL
                                        UNIQUE,
            password    CHAR( 50 )      NOT NULL,
            add_date    DATETIME( 30 ),
            update_date DATETIME( 30 ),
            state       CHAR( 10 ),
            type        CHAR( 200 ) 
        );'''
    createKeyCode = '''CREATE TABLE key_code ( 
            id       INTEGER      PRIMARY KEY AUTOINCREMENT,
            email_id INTEGER,
            email    CHAR( 50 ),
            keycode  CHAR( 100 ),
            add_date CHAR( 30 ) 
        );'''
    insert1 ='''
    INSERT INTO email (email,password,add_date,update_date,state,type) 
      VALUES ('t2hileenbg@outlook.com', 'vDpQhIonwPzyzy', '2018-09-02 12:12:12', '2018-09-02 12:12:12', '已提取','Office 2016' );
    '''
    insert2 = '''
    INSERT INTO email (email,password,add_date,update_date,state,type) 
      VALUES ('tsoasislouqjbo@outlook.com', 'pEMucs0AwCWTW', '2018-09-02 22:12:12', '2018-09-05 12:12:12', '未提取','Windows 10' ) ;   
    '''
    extc_sql(createEmail)
    extc_sql(createKeyCode)
    extc_sql(insert1)
    extc_sql(insert2)
    return jsonify({'msg': 'init db successfully'})
if __name__ == '__main__':
    app.run(host= '0.0.0.0',port=80,debug=True)
    # app.run()