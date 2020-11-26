from sense_emu import SenseHat
# from sense_hat import SenseHat

from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello world'


@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/hello/<name>')
def hello(name):
    return render_template('page.html', name=name)


@app.route('/say/', methods=['POST'])
def say():
    sense = SenseHat()
    sense.clear()
    sense.show_message(request.json['name'])
    return request.json['name']


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
