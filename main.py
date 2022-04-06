from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user
from werkzeug.security import check_password_hash, generate_password_hash

from web_project.base import app, db
from web_project.models import User


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    login = request.form.get('login')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    if request.method == 'POST':
        if not (login or password or password2):
            flash('Please, fill all fields!')
        elif password != password2:
            flash('Passwords are not equal!')
        else:
            hash_pwd = generate_password_hash(password)
            new_user = User(login=login, password=hash_pwd)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login_page'))
    return render_template('registration.html')


@app.route('/login', methods=['POST', 'GET'])
def login_page():
    login = request.form.get('login')
    password = request.form.get('password')
    if login and password:
        user = User.query.filter_by(login=login).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page)
        else:
            flash('Login or password is not correct')
    else:
        flash('Please fill login and password fields')
    return render_template('login.html')


@app.route('/home', methods=['POST', 'GET'])
def home():
    return render_template('home.html')


# @app.route('/add_picture', methods=['POST', 'GET'])
# @login_required
# def add_picture():
#     return render_template('add_picture.html')


# @app.route('/', methods=['POST', 'GET'])
# def start():
#     return render_template('index.html')


# @app.route('/logout', methods=['GET', 'POST'])
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('hello_world'))


# @app.after_request
# def redirect_to_signing(response):
#     if response.status_code == 401:
#         return redirect(url_for('login_page') + '?next=' + request.url)
#     return response


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
