import hmac
import os
import secrets

from flask import Flask, jsonify, render_template, request


def create_app():
    app = Flask(__name__)
    app.config['MAX_CONTENT_LENGTH'] = 4096
    username = os.environ.get('APP_USERNAME', '')
    password = os.environ.get('APP_PASSWORD', '')
    if not username or not password or password == 'CHANGE_ME':
        raise RuntimeError('Set APP_USERNAME and APP_PASSWORD before starting.')

    @app.after_request
    def no_cache(response):
        response.headers['Cache-Control'] = 'no-store'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        return response

    @app.get('/')
    def index():
        # No persistent login: refreshing always returns an empty login form.
        return render_template('auth.html')

    @app.post('/login')
    def login():
        # JSON is sent by fetch, so refreshing cannot resubmit the login POST.
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return jsonify(error='Ожидается JSON.'), 400
        supplied_user = data.get('username')
        supplied_password = data.get('password')
        if not isinstance(supplied_user, str) or not isinstance(supplied_password, str):
            return jsonify(error='Укажите логин и пароль.'), 400
        valid_user = hmac.compare_digest(supplied_user.encode(), username.encode())
        valid_password = hmac.compare_digest(supplied_password.encode(), password.encode())
        if not (valid_user and valid_password):
            return jsonify(error='Неверный логин или пароль.'), 401
        return jsonify(code=secrets.randbelow(9000) + 1000)

    return app


if __name__ == '__main__':
    create_app().run(host='127.0.0.1', port=8002)
