from flask import Flask, render_template_string, request
import secrets

app = Flask(__name__)

HTML = """
<!doctype html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>15問から1つを各被験者に割当（5人）</title>
  <style>
    body { font-family: Arial, sans-serif; background:#f5f7fb; margin:0; padding:24px; }
    .wrap { max-width: 780px; margin:0 auto; background:#fff; border:1px solid #e5e9f2; border-radius:12px; padding:20px 22px; }
    h1 { margin:0 0 6px 0; }
    .muted{ color:#6b7280; }
    .row{ display:flex; gap:12px; flex-wrap:wrap; }
    .col{ flex:1 1 240px; min-width:240px; }
    input, textarea { width:100%; padding:10px; border-radius:10px; border:1px solid #d1d5db; font-size:14px; }
    textarea { min-height: 84px; }
    button { padding:10px 16px; border:none; border-radius:10px; background:#2563eb; color:#fff; font-weight:700; cursor:pointer; }
    button:hover { background:#1d4ed8; }
    table { width:100%; border-collapse: collapse; margin-top:14px; }
    th, td { border:1px solid #e5e7eb; padding:8px 10px; text-align:center; }
    th { background:#f3f4f6; }
    .note { font-size:12px; color:#6b7280; margin-top:6px;}
    .chip { display:inline-block; padding:2px 8px; border-radius:999px; background:#eef2ff; border:1px solid #c7d2fe; font-size:12px; }
  </style>
</head>
<body>
  <div class="wrap">
    <h1>15問から1つを各被験者に割当 <span class="muted">（5人）</span></h1>
    <p class="muted">既定は <span class="chip">被験者=5</span> ・ <span class="chip">プール=15問</span> から各人に支払い対象問題を1つ割当。</p>

    <form method="post">
      <div class="row">
        <div class="col">
          <label>被験者数 (participants)</label>
          <input type="number" name="participants" value="{{ participants }}" min="1" />
        </div>
        <div class="col">
          <label>プール総数 (pool)</label>
          <input type="number" name="pool" value="{{ pool }}" min="1" />
        </div>
        <div class="col">
          <label>グローバルseed（任意・整数）</label>
          <input type="number" name="seed" value="{{ seed if seed is not none else '' }}" />
          <div class="note">SIDを指定すると <code>seed' = hash32(sid) XOR seed</code> で個別に決定</div>
        </div>
      </div>
      <div class="row">
        <div class="col" style="flex:1 1 100%">
          <label>参加者ID（任意・カンマ/改行区切り）</label>
          <textarea name="sids" placeholder="例: 101,102,103,104,105">{{ sids_text }}</textarea>
          <div class="note">空欄なら「1..N」の連番を使用</div>
        </div>
      </div>
      <div style="margin-top:10px">
        <button type="submit">割当を実行</button>
      </div>
    </form>

    {% if assignments %}
      <h2>結果</h2>
      <table>
        <tr><th>被験者</th><th>SID</th><th>seed_effective</th><th>支払い対象の問題番号 (1..{{ pool }})</th></tr>
        {% for row in assignments %}
          <tr>
            <td>{{ loop.index }}</td>
            <td>{{ row.sid }}</td>
            <td>{{ row.eff_seed }}</td>
            <td><strong>{{ row.pick }}</strong></td>
          </tr>
        {% endfor %}
      </table>
      <p class="note">同じ <strong>seed</strong> と同じ <strong>SID</strong> で再現可能（決定論的）。seed未入力の場合は安全な乱数で毎回異なる結果。</p>
    {% endif %}
  </div>
</body>
</html>
"""

def fnv1a_32(s: str) -> int:
    h = 0x811c9dc5
    for ch in s:
        h ^= ord(ch)
        h = (h + ((h << 1) + (h << 4) + (h << 7) + (h << 8) + (h << 24))) & 0xFFFFFFFF
    return h & 0xFFFFFFFF

class XorShift32:
    def __init__(self, seed: int):
        x = seed & 0xFFFFFFFF
        if x == 0:
            x = 1
        self.x = x
    def rand(self) -> float:
        x = self.x
        x ^= (x << 13) & 0xFFFFFFFF
        x ^= (x >> 17) & 0xFFFFFFFF
        x ^= (x << 5)  & 0xFFFFFFFF
        self.x = x & 0xFFFFFFFF
        return (self.x & 0xFFFFFFFF) / 4294967296.0

def pick_one(pool: int, seed_effective: int) -> int:
    rng = XorShift32(seed_effective)
    return int(rng.rand() * pool) + 1

from flask import Flask, render_template_string, request
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    participants = 5
    pool = 15
    seed = None
    sids_text = ""
    assignments = []

    if request.method == "POST":
        try:
            participants = max(1, int(request.form.get("participants", participants)))
        except: pass
        try:
            pool = max(1, int(request.form.get("pool", pool)))
        except: pass
        seed_val = request.form.get("seed", "").strip()
        seed = int(seed_val) if seed_val != "" else None
        sids_text = request.form.get("sids", "").strip()

        if sids_text:
            raw = [x.strip() for x in sids_text.replace("\n", ",").split(",") if x.strip() != ""]
            sids = raw[:participants] if len(raw) >= participants else raw + [str(i+1) for i in range(len(raw), participants)]
        else:
            sids = [str(i+1) for i in range(participants)]

        for sid in sids[:participants]:
            if seed is not None:
                eff = (fnv1a_32(str(sid)) ^ (seed & 0xFFFFFFFF)) & 0xFFFFFFFF
                q = pick_one(pool, eff)
            else:
                import secrets
                q = secrets.choice(range(1, pool+1))
                eff = None
            assignments.append({"sid": sid, "pick": q, "eff_seed": eff})

    return render_template_string(
        HTML,
        participants=participants,
        pool=pool,
        seed=seed,
        sids_text=sids_text,
        assignments=assignments
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
