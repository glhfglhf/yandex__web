from flask import Flask, render_template

app = Flask(__name__)


@app.route('/sign_in')
def sign_in():
    return render_template('verification.html')


@app.route('/sign_up')
def sign_up():
    return render_template('registration.html')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
