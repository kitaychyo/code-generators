import secrets

from flask import Flask, render_template

app = Flask(__name__)


@app.after_request
def no_cache(response):
    response.headers['Cache-Control'] = 'no-store'
    return response


@app.get('/')
def index():
    # Each request makes a fresh random draw from 1000 through 9999.
    code = secrets.randbelow(9000) + 1000
    return render_template('public.html', code=code)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8001)
