import flask
import json
from flask_cors import CORS
from flask import request

app = flask.Flask(__name__)
CORS(app) 

@app.route('/')
def index():
    return 'Server is running on port 5000.'

@app.route('/threads')
def threads():
    with open('user_data/threads.json', 'r') as f:
        threads = json.load(f)
    return flask.jsonify(threads)

@app.route('/users')
def users():
    limit = request.args.get('limit', default=None, type=int)
    with open('user_data/users.json', 'r') as f:
        users_dict = json.load(f)

    if limit is not None:
        # Convert dict to list of tuples, slice, and convert back to dict
        users_dict = dict(list(users_dict.items())[:limit])

    return flask.jsonify(users_dict)

@app.route('/messages')
def messages():
    limit = request.args.get('limit', default=None, type=int)
    with open('user_data/messages.json', 'r') as f:
        messages = json.load(f)
    if limit is not None:
        messages = messages[:limit]
    return flask.jsonify(messages)

@app.route('/user-threads')
def user_threads():
    with open('user_data/user_threads.json', 'r') as f:
        user_threads = json.load(f)
    return flask.jsonify(user_threads)

@app.route('/thread-users')
def thread_users():
    with open('user_data/thread_users.json', 'r') as f:
        thread_users = json.load(f)
    return flask.jsonify(thread_users)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5002)
