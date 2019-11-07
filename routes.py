from flask import Flask, render_template




app = Flask(__name__)

@app.route('/user/<string:username>')


def index(username):
    return render_template('index.html', username=username)


if __name__ == '__main__':
    app.run(debug=True)
