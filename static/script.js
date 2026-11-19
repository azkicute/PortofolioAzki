// ===== 1. Teks peran yang diketik otomatis =====
var roles = ['web developer pemula', 'desainer antarmuka', 'mahasiswa yang suka belajar'];
var ri = 0, ci = 0, hapus = false;
var el = document.getElementById('peran');

function ketik() {
  var teks = roles[ri];
  el.textContent = teks.slice(0, ci);   // tampilkan huruf 0 sampai ci

  if (!hapus && ci < teks.length) { ci++; setTimeout(ketik, 80); }
  else if (!hapus) { hapus = true; setTimeout(ketik, 1400); }   // jeda sebelum menghapus
  else if (ci > 0) { ci--; setTimeout(ketik, 40); }
  else { hapus = false; ri = (ri + 1) % roles.length; setTimeout(ketik, 300); }
}

// el hanya ada di halaman utama. Di halaman lain (CV, admin) dilewati.
if (el) {
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) {
    el.textContent = roles[0];
  } else {
    ketik();
  }
}

// ===== 2. Bar skill terisi saat terlihat di layar =====
var bars = document.querySelectorAll('.bar i');

function isi(b) { b.style.width = b.dataset.w + '%'; }   // data-w="90" jadi lebar 90%

if ('IntersectionObserver' in window) {
  var pengamat = new IntersectionObserver(function (daftar) {
    daftar.forEach(function (x) {
      if (x.isIntersecting) { isi(x.target); pengamat.unobserve(x.target); }
    });
  }, { threshold: 0.4 });
  bars.forEach(function (b) { pengamat.observe(b); });
} else {
  bars.forEach(isi);
}

// ===== 3. Tombol ganti tema terang/gelap =====
var root = document.documentElement;
document.getElementById('tema').addEventListener('click', function () {
  var gelap = root.dataset.theme
    ? root.dataset.theme === 'dark'
    : matchMedia('(prefers-color-scheme: dark)').matches;
  root.dataset.theme = gelap ? 'light' : 'dark';
});