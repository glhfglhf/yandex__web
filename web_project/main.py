import sqlite3
import random
from datetime import date
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from web_project.base import app, db
from web_project.models import User

user_name = ''
base_cash = 100
result_game = '0'


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    db_coins = sqlite3.connect('base_money.db')
    cursor = db_coins.cursor()
    db_col_cash = sqlite3.connect('collect_cash.db')
    cur = db_col_cash.cursor()
    login = request.form.get('login')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    user = User.query.filter_by(login=login).first()
    if request.method == 'POST':
        if not (login or password or password2):
            flash('Пожалуйста заполните оба поля')
        elif password != password2:
            flash('Пароли не похожи')
        elif user:
            flash('Этот логин уже занят. Пожалуйста, выберите другой')
        else:
            cursor.execute("INSERT INTO cash VALUES(?, ?);", (login, base_cash))
            cur.execute("INSERT INTO take_cash VALUES(?, ?);", (login, date.today()))
            db_col_cash.commit()
            db_coins.commit()
            hash_pwd = generate_password_hash(password)
            new_user = User(login=login, password=hash_pwd)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login_page'))
    return render_template('registration.html')


@app.route('/login', methods=['POST', 'GET'])
def login_page():
    global user_name
    login = request.form.get('login')
    user_name = login
    password = request.form.get('password')
    if login and password:
        user = User.query.filter_by(login=login).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Логин или пароль некорректны')
    else:
        flash('Пожалуйста заполните оба поля')
    return render_template('login.html')


@app.route('/home', methods=['POST', 'GET'])
@login_required
def home():
    global user_name
    global result_game
    bet = request.form.get('bet')
    cash = 0
    user_avatar = ''
    db_coins = sqlite3.connect('base_money.db')
    cursor = db_coins.cursor()
    result = cursor.execute(f"""SELECT cash
                                  FROM cash
                                 WHERE login = "{user_name}" 
                                """)
    db_coins.commit()
    for i in result:
        cash = int(i[0])
    with open('user_prof_image_accordance.txt', 'r+', encoding='utf-8') as f:
        for i in f:
            if i.split('-')[0] == user_name:
                user_avatar = i.split('-')[1]
    if not user_avatar:
        user_avatar = 'default.png'
    if request.method == 'POST':
        if not bet:
            flash('Сделайте ставку')
        elif int(bet) > cash:
            flash('У вас недостаточно монет, возвращайтесь завтра!')
        elif int(bet) <= 0:
            flash('Нельзя поставить число меньшее либо равное нулю')
        else:
            sign_r = random.randint(0, 1)
            if sign_r == 0:
                sign = '-'
            else:
                sign = '+'
            part = round(random.random(), 2)
            cash_of_bet = int(sign + str(round(part * int(bet))))
            result_game = sign + str(round(part * int(bet)))
            total = cash + cash_of_bet
            cursor.execute(f'UPDATE cash SET cash = {total} WHERE login = "{user_name}"')
            result = cursor.execute(f"""SELECT cash
                                              FROM cash
                                             WHERE login = "{user_name}" 
                                            """)
            db_coins.commit()
            for i in result:
                cash = int(i[0])
            return redirect(url_for('home', avatar=user_avatar, login=user_name,
                                    cash=cash, result=str(result_game)))
    return render_template('home.html', avatar=user_avatar, login=user_name, cash=cash, result=result_game)


def user_login():
    login = current_user.login()
    return print(str(login))


@app.route('/add_picture', methods=['POST', 'GET'])
@login_required
def add_picture():
    extensions = ['png', 'bmp', 'tif', 'psd', 'gif', 'jpg', 'jpeg']
    user_avatar = ''
    global user_name
    if request.method == 'POST':
        file = request.files['file']
        if not file:
            flash('Не указан файл!')
        else:
            try:
                if (str(file.filename).split('.')[-1]).lower() in extensions:
                    file.save(f'static/user_images/{secure_filename(file.filename)}')
                    with open('user_prof_image_accordance.txt', 'a', encoding='utf-8') as f:
                        f.write(f'{user_name}-{file.filename} \n')
                    with open('user_prof_image_accordance.txt', 'r+', encoding='utf-8') as f:
                        for i in f:
                            if i.split('-')[0] == user_name:
                                user_avatar = i.split('-')[1]
                    if not user_avatar:
                        user_avatar = 'default.png'
                    flash('Успешная смена аватара!')
                    return render_template("add_picture.html", name=file.filename,
                                           avatar=user_avatar, login=user_name)
                else:
                    flash('Неверный формат файла, пожалуйста выберите изображение.')
            except FileNotFoundError as e:
                print('Ошибка смены аватара' + str(e))
    with open('user_prof_image_accordance.txt', 'r+', encoding='utf-8') as f:
        for i in f:
            if i.split('-')[0] == user_name:
                user_avatar = i.split('-')[1]
    if not user_avatar:
        user_avatar = 'default.png'
    return render_template('add_picture.html', avatar=user_avatar, login=user_name)


@app.route('/', methods=['POST', 'GET'])
def start():
    return render_template('index.html')


@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login_page'))


@app.route('/take_money', methods=['POST', 'GET'])
@login_required
def take_money():
    global user_name
    db_coins = sqlite3.connect('base_money.db')
    cursor = db_coins.cursor()
    result_cash = cursor.execute(f"""SELECT cash
                                  FROM cash
                                 WHERE login = "{user_name}"
                                """)
    db_coins.commit()
    db_col = sqlite3.connect('collect_cash.db')
    cur = db_col.cursor()
    cash = 0
    data = str(date.today())
    lt_col = ''
    result_col_lt = cur.execute(f"""SELECT last_collect
                                      FROM take_cash
                                     WHERE login = "{user_name}"
                                    """)
    db_col.commit()
    for i in result_col_lt:
        lt_col = str(i[0])
    for i in result_cash:
        cash = int(i[0])
    if request.method == 'GET':
        print(lt_col, data)
        if lt_col != data:
            cur.execute(f'UPDATE take_cash SET last_collect = "{data}" WHERE login = "{user_name}"')
            cursor.execute(f'UPDATE cash SET cash = {int(cash + 100)} WHERE login = "{user_name}"')
            db_coins.commit()
            db_col.commit()
            return render_template('collect_cash.html', cash=int(cash + 100), lt_col=date.today())
        else:
            flash('Вы уже забирали сегодня')
    return render_template('collect_cash.html', cash=cash, lt_col=lt_col)


@app.route('/about_us', methods=['GET'])
@login_required
def about_us():
    return render_template('about_us.html')


if __name__ == '__main__':
    app.run(port=8085, host='localhost')
