import flask
import json

app = flask.Flask(__name__)

@app.route('/')
def index():
    return 'Server is running on port 5000.'

@app.route('/threads')
def threads():
    with open('user_data/threads2.json', 'r') as f:
        threads = json.load(f)
    return flask.jsonify(threads)

@app.route('/users')
def users():
    with open('user_data/users2.json', 'r') as f:
        users = json.load(f)
    return flask.jsonify(users)

@app.route('/messages')
def messages():
    with open('user_data/messages2.json', 'r') as f:
        messages = json.load(f)
    return flask.jsonify(messages)

@app.route('/user-threads')
def user_threads():
    with open('user_data/user_threads2.json', 'r') as f:
        user_threads = json.load(f)
    return flask.jsonify(user_threads)

@app.route('/thread-users')
def thread_users():
    with open('user_data/thread_users2.json', 'r') as f:
        thread_users = json.load(f)
    return flask.jsonify(thread_users)

if __name__ == '__main__':
    app.run(debug=True)