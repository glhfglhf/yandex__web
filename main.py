from flask import Flask, render_template

app = Flask(__name__)


@app.route('/in', methods=['POST', 'GET'])
def sign_in():
    return render_template('registration.html')
#     return f"""<!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <link rel= "stylesheet" type= "text/css" href="static/styles/ver_reg.css">
#     <title>Title</title>
# </head>
# <body>
#     <div class="form">
#             <h1 class="tit">Регистрация</h1>
#             <div class="input-form">
#                 <input class="login" type="text" placeholder="Придумайте логин">
#             </div>
#             <div class="input-form">
#                 <input class="password" type="password" placeholder="Пароль">
#             </div>
#             <div class="input-form">
#                 <button class="ver">Войти</button>
#                 <button class="reg">Зарегистрироваться</button>
#             </div>
#         </div>
# </body>
# </html>"""


@app.route('/', methods=['POST', 'GET'])
@app.route('/up', methods=['POST', 'GET'])
def sign_up():
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel= "stylesheet" type= "text/css" href="static/styles/ver_reg.css">
    <title>Title</title>
</head>
<body>
    <div class="form">
            <h1 class="tit">Вход</h1>
            <div class="input-form">
                <input class="login" type="text" placeholder="Логин">
            </div>
            <div class="input-form">
                <input class="password" type="password" placeholder="Пароль">
            </div>
            <div class="input-form">
                <button class="ver">Войти</button>
                <button class="reg">Зарегистрироваться</button>
            </div>
    </div>
</body>
</html>"""


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
