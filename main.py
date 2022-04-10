from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash

from web_project.base import app, db
from web_project.models import User

MAX_CONTENT_LENGTH = 1024 * 1024
base_cash = 100


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    global base_cash
    login = request.form.get('login')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    user = User.query.filter_by(login=login).first()
    if request.method == 'POST':
        if not (login or password or password2):
            flash('Please, fill all fields!')
        elif password != password2:
            flash('Passwords are not equal!')
        elif user:
            flash('Этот логин уже занят. Пожалуйста, выберите другой')
        else:
            try:
                with app.open_resource(app.root_path + url_for('static', filename='pictures/default.png'), 'rb') as f:
                    avatar = f.read()
            except FileNotFoundError as e:
                print('Not found' + str(e))
            hash_pwd = generate_password_hash(password)
            new_user = User(login=login, password=hash_pwd, avatar=avatar, cash=base_cash)
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
            return redirect(url_for('home'))
        else:
            flash('Login or password is not correct')
    else:
        flash('Please fill login and password fields')
    return render_template('login.html')


@app.route('/home', methods=['POST', 'GET'])
@login_required
def home():
    return render_template('home.html')


def user_login():
    login = current_user.login()
    return print(str(login))


@app.route('/add_picture', methods=['POST', 'GET'])
@login_required
def add_picture():
    if request.method == 'POST':
        file = request.files['file']
        if not file:
            flash('Не указан файл!')
        else:
            try:
                avatar = file.read()
                User.query.filter_by(id=current_user.get_id()).update({'avatar': avatar})
                db.session.commit()
                flash('Успешная смена аватара!')
                return render_template('add_picture.html', avatar=None)
            except FileNotFoundError as e:
                print('Ошибка смены аватара' + str(e))
    return render_template('add_picture.html', avatar=None, login=None)


@app.route('/', methods=['POST', 'GET'])
def start():
    return render_template('index.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login_page'))


if __name__ == '__main__':
    app.run(port=8080, host='localhost')
