# Sistem Posyandu Django

Sistem Posyandu Django adalah sebuah aplikasi web yang dibangun menggunakan framework Django. Aplikasi ini bertujuan untuk membantu mengelola data dan proses administrasi di Posyandu.

## Fitur

- Manajemen data anggota Posyandu
- Pencatatan data pertumbuhan balita
- Pelaporan data statistik
- Manajemen jadwal kegiatan Posyandu

## Instalasi

1. Clone repositori ini ke direktori lokal Anda.
2. Buat virtual environment dan aktifkan:
    ```
    python -m venv env
    source env/bin/activate
    ```
3. Install dependencies:
    ```
    pip install -r requirements.txt
    ```
4. Jalankan migrasi database:
    ```
    python manage.py migrate
    ```
5. Jalankan server lokal:
    ```
    python manage.py runserver
    ```

## Kontribusi

Jika Anda ingin berkontribusi pada proyek ini, silakan ikuti langkah-langkah berikut:

1. Fork repositori ini.
2. Buat branch baru:
    ```
    git checkout -b fitur-baru
    ```
3. Lakukan perubahan yang diperlukan.
4. Commit perubahan Anda:
    ```
    git commit -m "Menambahkan fitur baru"
    ```
5. Push ke branch Anda:
    ```
    git push origin fitur-baru
    ```
6. Buat pull request ke repositori utama.

## Lisensi

Proyek ini dilisensikan di bawah [MIT License](LICENSE).