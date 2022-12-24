# bukuuntuksemua

Buka terminal.

Kalau belum clone projek ke dalam laptop, boleh clone dengan cara
`git clone https://github.com/juwaini/bukuuntuksemua.git`

Run command berikut:

`python3 -V`

Kalau version python tu 3.9.x, kira terbaik la. Kalau kurang dari tu, cuba upgrade python3 tu pakai brew.

Pergi masuk ke directory bukuuntuksemua, misalnya:

`cd /home/juwaini/bukuuntuksemua`

Run command berikut:

`python3 -m venv venv`

`. ./venv/bin/activate`

Pastikan sebelah kiri command ada tulis `(venv)`.

Run `pip install -r requirements.txt`. Tunggu sampai selesai.

Run `./manage.py runserver` dan buka browser pada `127.0.0.1:8000`.
