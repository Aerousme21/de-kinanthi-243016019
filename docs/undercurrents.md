# Identifikasi Undercurrents pada pipeline_mini.py

| Undercurrent | Bukti penerapan di kode | Kekurangan | Usulan perbaikan |
|--------------|-------------------------|------------|------------------|
| Security | Kredensial dibaca dari `.env` lewat `load_dotenv()` | Pipeline memakai user `de_user` yang punya hak penuh | Buat user khusus pipeline yang hanya boleh membaca `transaksi` dan menulis `mart_omzet_harian` |
| Data management | `check_quality()` memeriksa `id_transaksi` ganda, `total` kurang dari atau sama dengan 0, dan `kanal` kosong | Aturan terbatas: kanal di luar toko, web, dan marketplace serta tanggal di masa depan lolos. Tidak ada dokumentasi skema atau lineage, dan data gagal tidak dikarantina | Tambah validasi nilai kanal dan tanggal, buat data dictionary, dan pindahkan data gagal ke folder karantina |
| DataOps | Logging lewat `logging.basicConfig` dan `log.info` di setiap tahap. Pipeline berhenti saat kualitas gagal | Tidak ada pengujian otomatis, pemantauan, maupun notifikasi kegagalan | Tulis unit test (pytest) untuk `check_quality` dan `transform`, jalankan lewat GitHub Actions, dan kirim notifikasi saat gagal |
| Data architecture | Satu fungsi per tahap lifecycle. Ada lapisan mentah (`data/raw`) dan lapisan siap pakai (`mart_omzet_harian`) | Full load seluruh transaksi di setiap eksekusi. CSV mentah lokal ditimpa tiap eksekusi. Sumber dan mart berada di database yang sama | Gunakan incremental load berdasarkan tanggal, simpan data mentah per tanggal ke bucket `raw` di MinIO, dan pisahkan skema mart dari skema sumber |
| Orchestration | `main()` memanggil tahap-tahap secara berurutan | Dijalankan manual, tanpa penjadwalan, retry, maupun pengelolaan dependensi antartahap | Jadwalkan setiap malam dengan cron atau Airflow, disertai retry dengan batas dan backoff |
| Software engineering | Kode modular dengan docstring dan type hint, konfigurasi dari environment, dan guard `if __name__ == "__main__"` | Belum ada pengujian. `RAW_DIR` ditulis langsung di kode. Error koneksi database belum ditangani | Tambah pengujian, jadikan path dan parameter dapat dikonfigurasi, dan tangani error koneksi dengan pesan yang jelas |

## Pertanyaan Sesi 2

### Mengapa mart_omzet_harian tetap aman saat data rusak masuk?

`check_quality()` dipanggil sebelum `transform()` dan `serve()`, dan melempar `ValueError` ketika menemukan data yang salah. Eksepsi itu menghentikan `main()`, sehingga tahap serving tidak pernah tercapai dan `mart_omzet_harian` tetap berisi hasil eksekusi terakhir yang valid. Analis dan dashboard tidak pernah melihat omzet yang keliru.

### data/raw/transaksi.csv tetap diperbarui walaupun data rusak. Masalah atau justru berguna?

Justru berguna. Salinan mentah disimpan apa adanya sebelum diperiksa, jadi baris penyebab kegagalan bisa dicari langsung, misalnya dengan menyaring `total <= 0`. Setelah sumber diperbaiki, pipeline dapat dijalankan ulang tanpa mengambil data dari awal. Kelemahannya ada pada penimpaan: berkas yang sama ditulis ulang di setiap eksekusi, sehingga salinan dari eksekusi yang sehat ikut hilang. Perbaikannya adalah menyimpan satu berkas per eksekusi dengan stempel waktu pada namanya, atau memindahkan data yang gagal ke folder karantina.
