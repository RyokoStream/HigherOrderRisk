# HigherOrderRisk (Flask + Heroku)

15問のプールから各被験者（既定5人）に支払い対象の問題を1つ割り当てるFlaskアプリ。

## ローカル
```bash
python app.py
# http://127.0.0.1:5000
```

## Heroku デプロイ（GitHub連携）
1. このフォルダ一式をGitHubの `HigherOrderRisk` リポジトリにアップロード
   - 必須ファイル: `app.py`, `requirements.txt`, `Procfile`, `runtime.txt`
2. Heroku dashboard → Create app → Deploy → GitHub → Connect to GitHub → `RyokoStream/HigherOrderRisk` を選択
3. `Enable Automatic Deploys` → `Deploy Branch`
4. Open app で公開URLを確認
