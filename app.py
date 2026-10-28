from secrets import randbelow

from flask import Flask, render_template_string

app = Flask(__name__)

HTML = """
<!doctype html>
<html lang="ru">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Генератор кода</title>
<body style="font-family: sans-serif; text-align: center; margin: 80px 20px">
  <h1>Случайный код</h1>
  <p style="font-size: 48px">{{ code }}</p>
  <p>Обнови страницу, чтобы получить новый код.</p>
  <a href="/">Обновить</a>
</body>
</html>
"""


@app.get('/')
def index():
    return render_template_string(HTML, code=randbelow(9000) + 1000), 200, {
        'Cache-Control': 'no-store'
    }


if __name__ == '__main__':
    app.run()
