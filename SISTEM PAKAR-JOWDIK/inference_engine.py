import json

# ===================================================
# 🔧 FUNGSI MUAT KNOWLEDGE BASE
# ===================================================
def load_knowledge_base(path):
    """Membaca file knowledge base JSON"""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# ===================================================
# 🧮 FUNGSI HITUNG CF COMBINE
# ===================================================
def combine_cf(cf_old, cf_new):
    """
    Menggabungkan dua CF menggunakan rumus klasik:
    CFcombine = CF1 + CF2 * (1 - CF1)
    """
    return cf_old + cf_new * (1 - cf_old)

# ===================================================
# 🧠 FUNGSI INFERENSI UTAMA
# ===================================================
def infer(user_answers, kb):
    """
    Melakukan inferensi berdasarkan gejala yang diisi user.
    user_answers = { "G01": 0.8, "G02": 0.4, ... }
    """
    results = {}
    rules = kb["rules"]

    for rule in rules:
        gejala_ids = rule["if"]
        gangguan_id = rule["then"]

        # Ambil CF pakar dari rule (jika ada)
        cf_rule = rule.get("cf_rule", 1.0)

        # Ambil CF user untuk gejala di rule ini
        cf_values = []
        for g in gejala_ids:
            if g in user_answers:
                cf_user = user_answers[g]
                # CF final gejala = CF_user * CF_rule
                cf_values.append(cf_user * cf_rule)

        # Kalau ada semua gejala terisi
        if cf_values:
            cf_hasil = min(cf_values)  # metode AND (pakar)
            cf_hasil = round(cf_hasil, 3)

            # Gabungkan CF kalau gangguan muncul di beberapa rule
            if gangguan_id in results:
                results[gangguan_id] = combine_cf(results[gangguan_id], cf_hasil)
            else:
                results[gangguan_id] = cf_hasil

    # Konversi hasil ke bentuk list
    hasil_list = []
    for gid, cf in sorted(results.items(), key=lambda x: x[1], reverse=True):
        hasil_list.append({
            "gangguan_id": gid,
            "gangguan": kb["gangguan"].get(gid, gid),
            "cf": round(cf, 3)
        })

    return hasil_list
