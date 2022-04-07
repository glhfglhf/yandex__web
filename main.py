from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from web_project.base import app, db
from web_project.models import User

MAX_CONTENT_LENGTH = 1024 * 1024
user_name = ''


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    global user_name
    login = request.form.get('login')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    if request.method == 'POST':
        if not (login or password or password2):
            flash('Please, fill all fields!')
        elif password != password2:
            flash('Passwords are not equal!')
        else:
            try:
                with app.open_resource(app.root_path + url_for('static', filename='pictures/default.png'), 'rb') as f:
                    avatar = f.read()
            except FileNotFoundError as e:
                print('Not found' + str(e))
            user_name = str(login)
            hash_pwd = generate_password_hash(password)
            new_user = User(login=login, password=hash_pwd, avatar=avatar)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login_page'))
    return render_template('registration.html')


@app.route('/login', methods=['POST', 'GET'])
def login_page():
    global user_name
    login = request.form.get('login')
    password = request.form.get('password')
    user_name = login
    if login and password:
        user = User.query.filter_by(login=login).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Login or password is not correct')
    else:
        flash('Please fill login and password fields')
    return render_template('login.html')


@app.route('/home', methods=['POST', 'GET'])
def home():
    return render_template('home.html')


@app.route('/add_picture', methods=['POST', 'GET'])
def add_picture():
    global user_name
    if request.method == 'POST':
        file = request.files['file']
        if not file:
            flash('Не указан файл!')
        try:
            avatar = file.read()
            User.query.filter_by(login=user_name).update({'avatar': avatar})
            db.session.commit()
            flash('Успешная смена аватара!')
            return render_template('add_picture.html', avatar=file)
        except FileNotFoundError as e:
            print('Ошибка смены аватара' + str(e))
    return render_template('add_picture.html', avatar=url_for('static', filename='pictures/default.png'))


@app.route('/', methods=['POST', 'GET'])
def start():
    return render_template('index.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('login_page'))


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
