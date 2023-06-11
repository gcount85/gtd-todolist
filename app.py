# 파이썬 웹 앱 프로그래밍 모듈 

from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient 

app = Flask(__name__)
client = MongoClient('localhost', 27017) # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbjamie 

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/tasklist', methods=["GET"])
def show_task_lists():
    tasklist = list(db.tasklist.find({}, {'_id':0}))
    return jsonify({'result': 'success', 'msg':'할일 목록 연결되었습니다', 'tasklist': tasklist})



@app.route('/add', methods=["POST"])
def add_task():
    status = request.form['status_give']
    content = request.form['content_give']
    db.tasklist.insert_one({'status': status, 'content':content})
    return jsonify({'result': 'success', 'msg':'할일 DB에 추가하였습니다'})


@app.route('/status', methods=['POST'])
def convert_status():
    status = request.form['status_give']
    content = request.form['content_give']
    if status == 'todo':
        db.tasklist.update_one({'content':content}, {'$set':{'status':'done'}})
    else:
        db.tasklist.update_one({'content':content}, {'$set':{'status':'todo'}})
    return jsonify({'result': 'success', 'msg':'할일의 status를 변경했습니다'})



@app.route('/delete', methods=['POST'])
def delete_task():
    content = request.form['content_give']
    db.tasklist.delete_one({'content':content})
    return jsonify({'result': 'success', 'msg':'할일을 삭제했습니다'})



@app.route('/edit', methods=['POST'])
def edit_task():
    old_con = request.form['old_con_give']
    new_con = request.form['new_con_give']
    db.tasklist.update_one({'content':old_con}, {'$set':{'content':new_con}})
    return jsonify({'result': 'success', 'msg':'할일을 수정했습니다'})



@app.route('/quotes', methods=['GET'])
def read_quote():
    quote = list(db.quotes.aggregate([{'$sample': {'size':1}}, {'$project':{'_id':0}}]))
    return jsonify({'result': 'success', 'msg':'문구를 불러왔습니다', 'quote': quote}) #항상 api는 json 형태로 돌려주는거 잊지 말자 


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
