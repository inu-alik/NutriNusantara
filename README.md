# NutriNusantara

Aplikasi diet dan penghitung kalori dengan database makanan khas Indonesia.

## Fitur Utama (MVP)
- Registrasi & Profil Pengguna
- Perhitungan target kalori otomatis
- Pencatatan makanan harian
- Pelacakan berat badan

## Struktur Proyek
```
nutrinusantara/
├── backend/           # Flask REST API
│   ├── app.py
│   ├── requirements.txt
├── mobile_app/        # Flutter app
│   └── lib/
│       └── main.dart
├── README.md
```

## Cara Menjalankan
### Backend
```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Frontend (Flutter)
```bash
cd mobile_app
flutter pub get
flutter run
```

---

**Lihat dokumentasi lebih lanjut dan cetak biru di repo ini.**
