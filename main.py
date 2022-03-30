from flask import Flask, render_template, redirect, request, url_for

app = Flask(__name__)


@app.route('/in', methods=['POST', 'GET'])
def sign_in():
    if request.method == 'GET':
        return render_template('registration.html')
    elif request.method == 'POST':
        print(request.form['login'])
        print(request.form['password'])
        return redirect(url_for('home'))


@app.route('/', methods=['POST', 'GET'])
@app.route('/up', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'GET':
        return render_template('verification.html')
    elif request.method == 'POST':
        print(request.form['login'])
        print(request.form['password'])
        return redirect(url_for('home'))


@app.route('/home', methods=['POST', 'GET'])
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')