from flask import Flask, request, render_template_string, redirect, url_for
from inference_engine import load_knowledge_base, infer
import os

app = Flask(__name__)

# ===================================================
# 🔧 Muat Knowledge Base
# ===================================================
KB_PATH = os.path.join(os.path.dirname(__file__), "knowledge_base.json")
kb = load_knowledge_base(KB_PATH)

# ===================================================
# 🎯 HALAMAN 1 — PILIH GANGGUAN + IKON INFO
# ===================================================
SELECT_GANGGUAN_HTML = """
<!doctype html>
<html lang="id">
<head>
  <meta charset="utf-8">
  <title>Pilih Jenis Gangguan</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
  <style>
    body {
      font-family: 'Poppins', sans-serif;
      background: #f9f9f9;
      color: #333;
      text-align: center;
      padding: 50px;
    }
    h1 { color: #b30000; margin-bottom: 10px; }
    .icon-container {
      margin-top: 10px;
      text-align: right;
      margin-right: 10%;
    }
    .icon-container a {
      text-decoration: none;
      font-size: 1.2rem;
      color: #b30000;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: #fff3f3;
      padding: 8px 14px;
      border-radius: 8px;
      border: 1px solid #b30000;
      transition: all 0.2s ease;
    }
    .icon-container a:hover {
      background: #b30000;
      color: white;
    }
    form {
      background: white;
      max-width: 600px;
      margin: 40px auto;
      padding: 30px;
      border-radius: 16px;
      box-shadow: 0 8px 20px rgba(0,0,0,0.08);
    }
    select {
      width: 100%;
      padding: 10px;
      font-size: 1rem;
      margin-bottom: 20px;
      border-radius: 8px;
      border: 1px solid #ccc;
    }
    button {
      background: #b30000;
      color: white;
      padding: 12px 24px;
      border: none;
      border-radius: 8px;
      cursor: pointer;
      font-size: 1rem;
    }
    button:hover { background: #800000; }
  </style>
</head>
<body>
  <h1>🧩 Pilih Jenis Gangguan Kepribadian</h1>

  <div class="icon-container">
    <a href="{{ url_for('info') }}">📘 Penjelasan Gangguan</a>
  </div>

  <form method="post" action="{{ url_for('questions') }}">
    <select name="gangguan_id" required>
      {% for gid, gname in gangguan.items() %}
        <option value="{{ gid }}">{{ gname }}</option>
      {% endfor %}
    </select>
    <button type="submit">➡️ Lanjut ke Pertanyaan</button>
  </form>
</body>
</html>
"""

# ===================================================
# 🧠 HALAMAN 2 — FORMULIR PERTANYAAN DENGAN OPSI SEJAJAR
# ===================================================
QUESTIONS_HTML = """
<!doctype html>
<html lang="id">
<head>
  <meta charset="utf-8">
  <title>Pertanyaan Gangguan {{ gangguan_nama }}</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
  <style>
    body {
      font-family: 'Poppins', sans-serif;
      background: #fdf8f8;
      color: #333;
      padding: 20px;
    }
    main {
      max-width: 1100px;
      margin: 0 auto;
      background: white;
      padding: 40px;
      border-radius: 16px;
      box-shadow: 0 8px 20px rgba(0,0,0,0.08);
    }
    h1 {
      color: #b30000;
      text-align: center;
      margin-bottom: 30px;
    }
    .q {
      margin: 20px 0;
      padding: 16px;
      border-left: 5px solid #b30000;
      background: #fff3f3;
      border-radius: 10px;
    }
    .options {
      display: grid;
      grid-template-columns: repeat(6, 1fr);
      gap: 8px;
      margin-top: 10px;
    }
    .options label {
      text-align: center;
      border: 1px solid #ccc;
      border-radius: 8px;
      padding: 10px 4px;
      cursor: pointer;
      transition: all 0.2s ease;
      background: #fff;
      font-size: 0.9rem;
      user-select: none;
    }
    .options label:hover {
      background: #ffe6e6;
      border-color: #b30000;
    }
    .options input[type="radio"] { display: none; }
    .options input[type="radio"]:checked + span {
      background: #b30000;
      color: white;
      border-radius: 8px;
      padding: 6px 10px;
      display: inline-block;
    }
    .btn {
      display: inline-block;
      padding: 12px 24px;
      background: #b30000;
      color: white;
      border: none;
      border-radius: 8px;
      font-size: 1rem;
      cursor: pointer;
      transition: background 0.3s;
      text-decoration: none;
      font-weight: 600;
    }
    .btn:hover { background: #800000; }
    .btn-container {
      text-align: center;
      margin-top: 30px;
      display: flex;
      justify-content: center;
      gap: 20px;
      flex-wrap: wrap;
    }
  </style>
</head>
<body>
  <main>
    <h1>🧠 Pertanyaan untuk {{ gangguan_nama }}</h1>
    <form method="post" action="{{ url_for('evaluate', gangguan_id=gangguan_id) }}">
      {% for gid, data in gejala %}
        <div class="q">
          <div><strong>{{ loop.index }}. {{ data['text'] }}</strong></div>
          <div class="options">
            {% for label, val in data['cf_options'].items() %}
              <label>
                <input type="radio" name="{{ gid }}" value="{{ val }}" required>
                <span>{{ label }}</span>
              </label>
            {% endfor %}
          </div>
        </div>
      {% endfor %}
      <div class="btn-container">
        <button type="submit" class="btn">🚀 Proses Hasil</button>
        <a href="{{ url_for('index') }}" class="btn">🔙 Kembali</a>
      </div>
    </form>
  </main>
</body>
</html>
"""


# ===================================================
# 📚 HALAMAN PENJELASAN GANGGUAN + FITUR PENCARIAN
# ===================================================
INFO_HTML = """
<!doctype html>
<html lang="id">
<head>
  <meta charset="utf-8">
  <title>Penjelasan Gangguan Kepribadian</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
  <style>
    body { font-family: 'Poppins', sans-serif; background: #fffaf9; color: #333; padding: 40px; }
    main { max-width: 900px; margin: 0 auto; background: white; padding: 30px; border-radius: 16px; box-shadow: 0 8px 20px rgba(0,0,0,0.08); }
    h1 { color: #b30000; text-align: center; margin-bottom: 30px; }
    input[type="text"] { width: 100%; padding: 12px; margin: 20px 0; border-radius: 8px; border: 1px solid #ccc; font-size: 1rem; }
    .gangguan { background: #fff3f3; padding: 20px; border-left: 5px solid #b30000; border-radius: 10px; margin-bottom: 16px; }
    h2 { color: #b30000; margin-top: 0; }
    .btn { display: block; text-align: center; background: #b30000; color: white; padding: 10px 20px; border-radius: 8px; text-decoration: none; font-weight: 600; margin-top: 30px; }
    .btn:hover { background: #800000; }
  </style>
</head>
<body>
  <main>
    <h1>📘 Penjelasan Singkat Setiap Gangguan</h1>
    <input type="text" id="searchBox" placeholder="🔍 Cari gangguan..." onkeyup="filterGangguan()">
    <div id="gangguanList">
      {% for gid, gname in gangguan.items() %}
        <div class="gangguan">
          <h2>{{ gname }}</h2>
          <p>{{ deskripsi.get(gid, "Belum ada deskripsi untuk gangguan ini.") }}</p>
        </div>
      {% endfor %}
    </div>
    <a href="{{ url_for('index') }}" class="btn">🔙 Kembali ke Menu Utama</a>
  </main>

  <script>
    function filterGangguan() {
      const input = document.getElementById('searchBox');
      const filter = input.value.toLowerCase();
      const items = document.getElementsByClassName('gangguan');
      for (let i = 0; i < items.length; i++) {
        const text = items[i].textContent || items[i].innerText;
        items[i].style.display = text.toLowerCase().includes(filter) ? '' : 'none';
      }
    }
  </script>
</body>
</html>
"""

# ===================================================
# 🧭 ROUTES
# ===================================================
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        selected = request.form.get("gangguan_id")
        return redirect(url_for("questions", gangguan_id=selected))
    return render_template_string(SELECT_GANGGUAN_HTML, gangguan=kb["gangguan"])

@app.route("/info")
def info():
    deskripsi = {
        "P1": """Gangguan Antisosial (Antisocial Personality Disorder)
        Gangguan ini ditandai oleh pola perilaku yang mengabaikan atau melanggar hak orang lain secara berulang. 
        Penderita sering menipu, manipulatif, impulsif, dan tidak menunjukkan rasa bersalah atas perbuatannya. 
        Biasanya dimulai sejak masa remaja dan berlanjut hingga dewasa. 
        Ciri khas: mudah marah, tidak menghormati norma sosial, berbohong, agresif, dan kurang empati.""",

        "P2": """Gangguan Schizotypal (Schizotypal Personality Disorder)
        Ditandai oleh pola pikir dan perilaku eksentrik, kepercayaan aneh, serta kecemasan sosial yang parah. 
        Orang dengan gangguan ini sering memiliki keyakinan magis (seperti kemampuan supranatural), berbicara dengan cara yang tidak biasa, dan sulit membentuk hubungan dekat.
        Ciri khas: cara berpikir aneh, kesulitan sosial, dan sering tampak “unik” atau “aneh” bagi orang lain.""",

        "P3": """Gangguan Schizoid (Schizoid Personality Disorder)
        Penderita menunjukkan ketidakminatan terhadap hubungan sosial dan cenderung menarik diri dari interaksi dengan orang lain. 
        Mereka tampak dingin secara emosional, lebih suka menyendiri, dan jarang mengekspresikan perasaan.
        Ciri khas: tidak tertarik menjalin hubungan dekat, tampak acuh, dan lebih nyaman sendirian.""",

        "P4": """Gangguan Paranoid (Paranoid Personality Disorder)
        Penderita cenderung sangat curiga terhadap motif orang lain dan yakin bahwa orang lain memiliki niat buruk terhadapnya. 
        Mereka sering salah menafsirkan tindakan orang lain sebagai ancaman atau penghinaan.
        Ciri khas: mudah tersinggung, sulit percaya pada orang lain, menyimpan dendam, dan selalu waspada berlebihan.""",

        "P5": """Gangguan Obsessive-Compulsive (Obsessive-Compulsive Personality Disorder)
        Bukan sama dengan OCD, gangguan ini ditandai dengan kebutuhan berlebihan akan keteraturan, kesempurnaan, dan kontrol. 
        Penderitanya terlalu fokus pada aturan dan efisiensi hingga mengorbankan fleksibilitas dan hubungan sosial.
        Ciri khas: perfeksionis, sulit delegasi tugas, kaku terhadap perubahan, dan bekerja berlebihan.""",

        "P6": """Gangguan Narcissistic (Narcissistic Personality Disorder)
        Orang dengan gangguan ini memiliki rasa penting diri yang sangat tinggi, kebutuhan ekstrem untuk dikagumi, dan kurang empati terhadap orang lain. 
        Mereka sering melebih-lebihkan pencapaian dan menganggap diri lebih istimewa dari orang lain.
        Ciri khas: arogan, haus pujian, mudah tersinggung bila dikritik, dan cenderung memanfaatkan orang lain.""",

        "P7": """Gangguan Histrionic (Histrionic Personality Disorder)
        Ditandai oleh perilaku yang sangat emosional dan pencarian perhatian yang berlebihan. 
        Penderitanya sering berperilaku dramatis, mudah terpengaruh, dan ingin menjadi pusat perhatian di setiap situasi.
        Ciri khas: ekspresif berlebihan, manipulatif secara emosional, dan sangat memperhatikan penampilan.""",

        "P8": """Gangguan Dependent (Dependent Personality Disorder)
        Gangguan ini ditandai oleh ketergantungan yang ekstrem terhadap orang lain untuk mengambil keputusan atau memberikan dukungan emosional. 
        Penderitanya takut ditinggalkan dan sulit mandiri.
        Ciri khas: sulit membuat keputusan tanpa nasihat orang lain, takut ditolak, dan rela mengorbankan kebutuhan sendiri agar tidak ditinggalkan.""",

        "P9": """Gangguan Borderline (Borderline Personality Disorder)
        Orang dengan gangguan ini mengalami ketidakstabilan ekstrem dalam emosi, hubungan, dan citra diri. 
        Mereka sering mengalami perubahan mood yang cepat, perilaku impulsif, dan ketakutan ditinggalkan.
        Ciri khas: perubahan suasana hati drastis, perilaku impulsif, dan hubungan intens tapi tidak stabil.""",

        "P10": """Gangguan Avoidant (Avoidant Personality Disorder)
        Penderita merasa tidak layak, sangat sensitif terhadap kritik, dan cenderung menghindari interaksi sosial karena takut ditolak atau diejek.
        Mereka ingin memiliki hubungan, tetapi rasa takut dan cemas sosial menghambatnya.
        Ciri khas: rendah diri, cemas berlebihan dalam situasi sosial, dan menghindari aktivitas dengan risiko penilaian negatif."""
    }

    return render_template_string(INFO_HTML, gangguan=kb["gangguan"], deskripsi=deskripsi)


@app.route("/questions", methods=["POST", "GET"])
def questions():
    gangguan_id = request.form.get("gangguan_id") or request.args.get("gangguan_id")
    gangguan_nama = kb["gangguan"].get(gangguan_id, gangguan_id)
    relevant_rules = [r for r in kb["rules"] if r["then"] == gangguan_id]
    relevant_gejala = sorted(set(g for r in relevant_rules for g in r["if"]))
    gejala = []
    for gid in relevant_gejala:
        if gid in kb["gejala"]:
            data = kb["gejala"][gid]
            if "cf_options" not in data:
                data["cf_options"] = {
                    "Tidak Sama Sekali": 0.0,
                    "Tidak Tahu": 0.2,
                    "Kadang": 0.4,
                    "Cukup Sering": 0.6,
                    "Sering": 0.8,
                    "Sangat Sering": 1.0
                }
            gejala.append((gid, data))
    return render_template_string(QUESTIONS_HTML, gangguan_id=gangguan_id, gangguan_nama=gangguan_nama, gejala=gejala)

@app.route("/evaluate/<gangguan_id>", methods=["POST"])
def evaluate(gangguan_id):
    answers = {gid: float(v) for gid, v in request.form.items()}
    results = infer(answers, kb)
    filtered = [r for r in results if r.get("gangguan_id") == gangguan_id or r.get("bakat_id") == gangguan_id]

    RESULT_HTML = """
    <!doctype html>
    <html lang="id">
    <head>
      <meta charset="utf-8">
      <title>Hasil Diagnosa</title>
      <meta name="viewport" content="width=device-width,initial-scale=1">
      <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
      <style>
        body {
          font-family: 'Poppins', sans-serif;
          background: #fdf8f8;
          color: #333;
          padding: 40px;
        }
        main {
          max-width: 800px;
          margin: 0 auto;
          background: white;
          padding: 30px;
          border-radius: 16px;
          box-shadow: 0 8px 20px rgba(0,0,0,0.08);
        }
        h1 {
          color: #b30000;
          text-align: center;
          margin-bottom: 30px;
        }
        .result {
          background: #fff3f3;
          border-left: 5px solid #b30000;
          padding: 20px;
          border-radius: 10px;
          margin-bottom: 20px;
        }
        h2 {
          color: #b30000;
          margin-top: 0;
        }
        .btn {
          display: block;
          text-align: center;
          background: #b30000;
          color: white;
          padding: 12px 20px;
          border-radius: 8px;
          text-decoration: none;
          font-weight: 600;
          margin-top: 30px;
          transition: background 0.3s ease;
        }
        .btn:hover {
          background: #800000;
        }
      </style>
    </head>
    <body>
      <main>
        <h1>📊 Hasil Diagnosa Gangguan Kepribadian</h1>
        {% if results %}
          <div class="result">
            <h2>🏆 Gangguan Dominan: {{ results[0]['gangguan'] }}</h2>
            <p>Nilai Keyakinan (CF): <strong>{{ results[0]['cf'] }}</strong></p>
          </div>
          <h3>Detail Semua Gangguan:</h3>
          <ul>
          {% for r in results %}
            <li>{{ loop.index }}. {{ r['gangguan'] }} — CF: {{ r['cf'] }}</li>
          {% endfor %}
          </ul>
        {% else %}
          <p>Tidak ada aturan yang terpenuhi.</p>
        {% endif %}
        <a href="{{ url_for('index') }}" class="btn">🔙 Kembali ke Menu Utama</a>
      </main>
    </body>
    </html>
    """

    return render_template_string(RESULT_HTML, results=filtered or results)


if __name__ == "__main__":
    app.run(debug=True)
