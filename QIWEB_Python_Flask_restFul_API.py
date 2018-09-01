# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#qiweb 20180901 22:26
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
# GET         http://[hostname]/todo/api/v1.0/tasks            检索任务列表
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

if __name__ == '__main__':
    # app.run(host= '192.168.0.33',port=80,debug=True)
    app.run()