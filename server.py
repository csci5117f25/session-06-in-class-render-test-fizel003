from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

writings = []

@app.route('/guestbook', methods=['GET'])
def hello_world3():
    name = request.args.get("name", "")
    message = request.args.get("message", "")
    writings.append([name, message])
    print(writings)
    return render_template('hello.html', writings=writings)