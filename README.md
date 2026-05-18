# Game Traffic Racer 2D

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Library](https://img.shields.io/badge/library-Pygame-green.svg)](https://www.pygame.org/)

**Traffic Racer** adalah sebuah game arcade 2D *endless driving* berbasis jalur (*lane-based*) yang dibangun menggunakan bahasa pemrograman **Python** dan *library* **Pygame**. Di dalam game ini, pemain harus mengendalikan mobil untuk menghindari kemacetan lalu lintas yang melaju secara dinamis dengan tingkat kesulitan yang terus meningkat.

Proyek ini dibuat sebagai bentuk implementasi siklus dasar pengembangan game (*Game Loop*), manajemen status objek (*State Management*), deteksi tabrakan yang presisi (*Collision Detection*), serta optimasi pengalaman pengguna (*User Interface & Experience*).

---

## Fitur Utama

- **Mekanik Gameplay yang Seimbang:** Pemilihan ukuran aset mobil sebesar `60x110px` yang proporsional dengan lebar jalur jalan raya untuk memastikan tidak ada *Safe Spot Exploit* (celah aman untuk diam di garis pembatas tanpa tertabrak).
- **Peningkatan Kesulitan Progresif (Difficulty Progression):** Kecepatan lalu lintas dan pergerakan jalan akan meningkat secara otomatis setiap kelipatan skor tertentu, memberikan tantangan yang adaptif bagi pemain.
- **Sistem High Score Persisten:** Menggunakan operasi *File I/O* lokal untuk membaca dan menulis rekor skor tertinggi ke dalam file `highscore.txt`, sehingga rekor tetap tersimpan meskipun aplikasi ditutup.
- **Desain UI yang Konsisten:** Tampilan layar *Menu Utama (Start Screen)* dan *Game Over* dirancang dengan bahasa visual yang seragam menggunakan *pop-up box* biru tua, bingkai tegas, efek *screen dimming* (transparansi latar belakang), dan fontasi bergaya poster (*Impact* & *Consolas*).
- **Pergerakan Halus (High Performance):** Berjalan stabil pada **120 FPS** untuk menghilangkan efek *jittering* (patah-patah) saat objek bergerak dalam kecepatan tinggi.
- **Variasi Musuh Dinamis:** Memuat dan mengundi secara acak 5 jenis variasi mobil musuh yang berbeda dari direktori lokal saat proses *spawning*.

---

## Cara Menjalankan Game
### Prasyarat
Pastikan komputer kamu sudah terpasang Python 3.x dan library Pygame. Jika belum memiliki Pygame, pasang melalui terminal/CMD:

```bash
pip install pygame
```

### Langkah Instalasi
1. Clone repositori ini ke komputer lokal kamu:
```bash
git clone [https://github.com/username-kamu/traffic-racer.git](https://github.com/username-kamu/traffic-racer.git)
```

2. Masuk ke dalam direktori proyek:
```bash
cd traffic-racer
```

3. Jalankan game menggunakan perintah:
```bash
python main.py
```

---

## Kontrol Game
* **A / Panah Kiri** : Bergerak ke Jalur Kiri
* **D / Panah Kanan** : Bergerak ke Jalur Kanan
* **SPASI** : Memulai Game (di Menu Awal) / Mengulangi Game (di Layar Game Over)
