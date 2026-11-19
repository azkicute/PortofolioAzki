import os
import sqlite3
from functools import wraps
from flask import (Flask, render_template, request, redirect,
                   url_for, flash, session, abort)

app = Flask(__name__)
# Di server, nilai ini diatur lewat environment (dijelaskan di Langkah 8)
app.secret_key = os.environ.get("SECRET_KEY", "kunci-lokal-ganti-nanti")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")

# Alamat file database, selalu di folder yang sama dengan app.py
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "proyek.db")

# Data portofolio disimpan di Python, lalu dikirim ke HTML.
# Mau ubah isi website? Cukup edit bagian ini.
PROFIL = {
    "nama_depan": "Fikrotul",
    "nama_belakang": "Azkia",
    "inisial": "FA",
    "lokasi": "Yogyakarta, Indonesia",
    "kampus": "Universitas Nahdlatul Yogyakarta",
    "jurusan": "Teknik Informatika",
    "minat": "Web, Jaringan Komputer",
    "email": "fikrotulazkia0@gmail.com",
}

SKILLS = [
    {"nama": "HTML & CSS", "nilai": 85},
    {"nama": "Flask (Python)", "nilai": 75},
    {"nama": "JavaScript", "nilai": 70},
    {"nama": "Basis data (SQL)", "nilai": 65},
    {"nama": "Git & GitHub", "nilai": 72},
]

PROYEK_AWAL = [
    {"ikon": "Web", "judul": "Toko Online UMKM",
     "isi": "Website katalog produk untuk usaha kecil, lengkap dengan pesan lewat WhatsApp.",
     "tag": ["HTML", "CSS", "Flask"]},
    {"ikon": "App", "judul": "Aplikasi Catatan Kuliah",
     "isi": "Menyimpan catatan per mata kuliah dengan pencarian cepat dan pengingat tugas.",
     "tag": ["Python", "SQL"]},
    {"ikon": "JarKom", "judul": "Belajar komponen komputer",
     "isi": "Rancangan komponen komputer yang dipelajari secara matang.",
     "tag": ["CPU", "PC"]},
]
CV = {
    "ringkasan": "Mahasiswa Teknik Informatika yang tertarik pada pengembangan web dan desain antarmuka. Terbiasa bekerja dalam tim, cepat belajar, dan senang menyelesaikan proyek dari ide sampai jadi.",
    "telepon": "0813-2633-1279",

    # Setiap item berisi: judul, tempat, waktu, dan keterangan
    "pendidikan": [
        {"judul": "S1 Teknik Informatika", "tempat": "UNU Yogyakarta",
         "waktu": "2025 – sekarang", "isi": "IPK 3,75. Fokus pada pemrograman web dan Jaringan Komputer."},
        {"judul": "SMA Jurusan TKJ", "tempat": "Syubbanul Wathon",
         "waktu": "2022 – 2025", "isi": "Lulus dengan nilai rata-rata 90."},
    ],
    "pengalaman": [
        {"judul": "Coding dan Criping kabel", "tempat": "SMK Syubbanul Wathon",
         "waktu": "2024", "isi": "Mempelajari Website ,codingan,dan komponen perangkat keras."},
    ],
    "organisasi": [
        {"judul": "Anggota Badan Pengurus Harian (BPH)", "tempat": "Himpunan Mahasiswa Informatika",
         "waktu": "2025 – sekarang", "isi": "Mengelola Keuangan Himpunan."},
        {"judul": "Anggota Dewan Ambalan Kejuruan", "tempat": "SMK Syubbanul Wathon",
                 "waktu": "2023 – 2024", "isi": "Mengelola Keuangan Ambalan."},
    ],
    "sertifikat": [
        "Viera and Toeic – english(2024)",
        "LSP Teknik Jaringan Komputer – LSP (2024)",
    ],
    "bahasa": ["Indonesia (aktif)", "Inggris (menengah)"],
}
def get_db():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row   # hasil query bisa dibaca per nama kolom
    return db


def init_db():
    """Buat tabel kalau belum ada, lalu isi data awal sekali saja."""
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS proyek (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ikon TEXT NOT NULL,
            judul TEXT NOT NULL,
            isi TEXT NOT NULL,
            tag TEXT NOT NULL DEFAULT ''
        )
    """)
    if db.execute("SELECT COUNT(*) FROM proyek").fetchone()[0] == 0:
        for p in PROYEK_AWAL:
            db.execute(
                "INSERT INTO proyek (ikon, judul, isi, tag) VALUES (?, ?, ?, ?)",
                (p["ikon"], p["judul"], p["isi"], ", ".join(p["tag"])),
            )
    db.commit()
    db.close()


init_db()   # dijalankan sekali saat aplikasi dimuat


def login_required(f):
    """Pembungkus: halaman hanya bisa dibuka kalau sudah login."""
    @wraps(f)
    def bungkus(*args, **kwargs):
        if not session.get("admin"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return bungkus

# Route = alamat URL. "/" adalah halaman utama.
@app.route("/")
def home():
    db = get_db()
    baris = db.execute("SELECT * FROM proyek ORDER BY id").fetchall()
    db.close()
    # Ubah tag "HTML, CSS" menjadi daftar ["HTML", "CSS"] agar cocok dengan index.html
    proyek = [{
        "ikon": b["ikon"], "judul": b["judul"], "isi": b["isi"],
        "tag": [t.strip() for t in b["tag"].split(",") if t.strip()],
    } for b in baris]
    return render_template("index.html", p=PROFIL, skills=SKILLS, proyek=proyek)
@app.route("/cv")
def cv():
    return render_template("cv.html", p=PROFIL, cv=CV, skills=SKILLS)

# Route untuk menerima form. methods=["POST"] artinya hanya menerima kiriman form.
@app.route("/kirim", methods=["POST"])
def kirim():
    nama = request.form.get("nama", "").strip()
    email = request.form.get("email", "").strip()
    pesan = request.form.get("pesan", "").strip()

    if not nama or not email or not pesan:
        flash("Isi nama, email, dan pesan dulu ya.")
    elif "@" not in email:
        flash("Alamat email belum benar. Contoh: nama@email.com")
    else:
        # Simpan pesan ke file teks supaya kamu bisa membacanya
        with open("pesan.txt", "a", encoding="utf-8") as f:
            f.write(f"{nama} | {email} | {pesan}\n")
        flash(f"Terima kasih, {nama}! Pesanmu sudah terkirim.")

    # Kembali ke halaman utama, tepat di bagian kontak
    return redirect(url_for("home", _anchor="kontak"))
# ===== LOGIN =====
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("password") == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect(url_for("admin"))
        flash("Password salah.")
    return render_template("login.html", p=PROFIL)


@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("home"))


# ===== READ: daftar proyek untuk admin =====
@app.route("/admin")
@login_required
def admin():
    db = get_db()
    daftar = db.execute("SELECT * FROM proyek ORDER BY id").fetchall()
    db.close()
    return render_template("admin.html", p=PROFIL, daftar=daftar)


# ===== CREATE =====
@app.route("/admin/tambah", methods=["GET", "POST"])
@login_required
def tambah():
    if request.method == "POST":
        ikon = request.form.get("ikon", "").strip()
        judul = request.form.get("judul", "").strip()
        isi = request.form.get("isi", "").strip()
        tag = request.form.get("tag", "").strip()
        if not (ikon and judul and isi):
            flash("Ikon, judul, dan deskripsi wajib diisi.")
            return render_template("form.html", p=PROFIL,
                                   judul_halaman="Tambah proyek", data=request.form)
        db = get_db()
        db.execute("INSERT INTO proyek (ikon, judul, isi, tag) VALUES (?, ?, ?, ?)",
                   (ikon, judul, isi, tag))
        db.commit()
        db.close()
        flash("Proyek berhasil ditambahkan.")
        return redirect(url_for("admin"))
    return render_template("form.html", p=PROFIL, judul_halaman="Tambah proyek", data=None)


# ===== UPDATE =====
@app.route("/admin/edit/<int:proyek_id>", methods=["GET", "POST"])
@login_required
def edit(proyek_id):
    db = get_db()
    data = db.execute("SELECT * FROM proyek WHERE id = ?", (proyek_id,)).fetchone()
    if data is None:
        db.close()
        abort(404)   # proyek tidak ditemukan
    if request.method == "POST":
        ikon = request.form.get("ikon", "").strip()
        judul = request.form.get("judul", "").strip()
        isi = request.form.get("isi", "").strip()
        tag = request.form.get("tag", "").strip()
        if not (ikon and judul and isi):
            db.close()
            flash("Ikon, judul, dan deskripsi wajib diisi.")
            return render_template("form.html", p=PROFIL,
                                   judul_halaman="Ubah proyek", data=request.form)
        db.execute("UPDATE proyek SET ikon=?, judul=?, isi=?, tag=? WHERE id=?",
                   (ikon, judul, isi, tag, proyek_id))
        db.commit()
        db.close()
        flash("Proyek berhasil diubah.")
        return redirect(url_for("admin"))
    db.close()
    return render_template("form.html", p=PROFIL, judul_halaman="Ubah proyek", data=data)


# ===== DELETE =====
@app.route("/admin/hapus/<int:proyek_id>", methods=["POST"])
@login_required
def hapus(proyek_id):
    db = get_db()
    db.execute("DELETE FROM proyek WHERE id = ?", (proyek_id,))
    db.commit()
    db.close()
    flash("Proyek dihapus.")
    return redirect(url_for("admin"))


if __name__ == "__main__":
    app.run(debug=True)  # debug=True: server restart otomatis saat kode diubah