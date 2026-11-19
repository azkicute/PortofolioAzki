from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "ganti-dengan-kata-rahasia-bebas"  # dibutuhkan untuk flash()

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

PROYEK = [
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

# Route = alamat URL. "/" adalah halaman utama.
@app.route("/")
def home():
    # render_template membuka templates/index.html dan mengisinya dengan data
    return render_template("index.html", p=PROFIL, skills=SKILLS, proyek=PROYEK)
@app.route("/cv")
def cv():
    # Mengirim data profil, CV, dan skill ke templates/cv.html
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


if __name__ == "__main__":
    app.run(debug=True)  # debug=True: server restart otomatis saat kode diubah