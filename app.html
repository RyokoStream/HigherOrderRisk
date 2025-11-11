from flask import Flask, render_template_string, request
import random

app = Flask(__name__)

# HTMLテンプレート（元の構成を踏襲）
html_template = """
<!doctype html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>1から15の問題から一つを選ぶ（5人）</title>
    <style>
        body {
            display: flex; justify-content: center; align-items: center;
            height: 100vh; margin: 0; background-color: #f5f5f5; font-family: Arial, sans-serif;
        }
        .container { text-align: center; }
        h1 { font-size: 2.0rem; margin-bottom: 12px; }
        h2 { font-size: 1.6rem; color: #333; margin: 6px 0; }
        button {
            font-size: 1.2rem; padding: 12px 24px; background-color: #007BFF;
            color: white; border: none; border-radius: 6px; cursor: pointer;
        }
        button:hover { background-color: #0056b3; }
        .muted { color:#555; font-size: 0.95rem; margin-top: 6px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>1から15の問題から一つを選ぶ（被験者5人）</h1>

        {% if random_numbers %}
            <h2>被験者1: {{ random_numbers[0] }}</h2>
            <h2>被験者2: {{ random_numbers[1] }}</h2>
            <h2>被験者3: {{ random_numbers[2] }}</h2>
            <h2>被験者4: {{ random_numbers[3] }}</h2>
            <h2>被験者5: {{ random_numbers[4] }}</h2>
        {% else %}
            <h2>まだ選択されていません</h2>
        {% endif %}

        <form action="/" method="post" style="margin-top:14px">
            <button type="submit">問題を選ぶ</button>
        </form>

        <div class="muted">※ 各被験者ごとに <strong>1..15</strong> の中から独立に1問を選びます（重複することがあります）。</div>
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    random_numbers = None
    if request.method == "POST":
        # 被験者5人ぶん、1..15から独立に1つずつ
        random_numbers = [random.randint(1, 15) for _ in range(5)]
    return render_template_string(html_template, random_numbers=random_numbers)

if __name__ == "__main__":
    app.run(debug=True)
