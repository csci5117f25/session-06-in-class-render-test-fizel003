from flask import Flask, request, render_template
import db
db.setup()

app = Flask(__name__)

@app.route('/')
@app.route('/<name>')
def hello(name=None):
    return render_template('hello.html', name=name, writings=db.get_guestbook())

writings = []

@app.post('/guestbook')
def hello_world3():
    name = request.form.get("name", "")
    message = request.form.get("message", "")
    db.add_entry(name, message)
    writings.append([name, message])
    print(writings)
    return render_template('hello.html', writings=db.get_guestbook())