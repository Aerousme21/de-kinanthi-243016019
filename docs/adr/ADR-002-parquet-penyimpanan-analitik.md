# ADR-002: Parquet sebagai format penyimpanan data analitik

**Status** : diusulkan

**Konteks** : Pipeline Batik Kinanthi saat ini menyimpan salinan mentah transaksi sebagai CSV di `data/raw`, dan bucket `raw` di MinIO disiapkan untuk modul berikutnya. Data transaksi akan terus bertambah dan dibaca berulang oleh Data Analyst untuk agregasi per kanal dan per produk. Diperlukan format penyimpanan yang efisien untuk analitik dan tidak mengikat ke satu alat.

**Opsi** :

| Opsi | Uraian | Biaya | Latensi baca | Kompleksitas |
|------|--------|-------|--------------|--------------|
| A. CSV | Teks biasa, satu baris per record | Ruang penyimpanan besar karena tanpa kompresi | Lambat: seluruh berkas dibaca meski hanya perlu beberapa kolom | Rendah, tetapi tipe data tidak tersimpan dan harus ditebak saat dibaca |
| B. Parquet | Format kolumnar terkompresi dengan skema tertanam | Ruang lebih hemat | Cepat: hanya kolom yang dibutuhkan yang dibaca | Sedang: butuh pustaka seperti pyarrow dan isinya tidak bisa dibaca langsung sebagai teks |
| C. Tabel format internal satu vendor | Data disimpan di format milik warehouse tertentu | Bergantung pada tarif vendor | Cepat di dalam ekosistem vendor itu | Tinggi bila suatu saat berpindah, karena data terkunci pada format vendor |

**Keputusan** : Opsi B, Parquet. Format ini terbuka dan dibaca banyak mesin (Spark, DuckDB, pandas), sehingga pilihan alat analitik tetap bebas. Kompresi dan pembacaan per kolom sesuai dengan pola kueri agregasi yang dominan.

**Tipe** : Two-way door. Mengganti format hanya memerlukan konversi data, dan sumbernya tidak berubah karena salinan mentah tetap disimpan.

**Konsekuensi** :
- Dampak: kueri analitik lebih cepat dan hemat ruang. Skema ikut tersimpan bersama data.
- Risiko: berkas tidak dapat dibuka dengan editor teks, dan pembaruan baris tunggal tidak efisien, karena Parquet dirancang untuk tulis sekali dan baca banyak.
- Exit plan: konversi Parquet ke format lain (CSV atau format warehouse) dengan satu skrip. Data mentah tetap disimpan di lapisan `raw`, dan skema didokumentasikan sehingga konversi ulang dapat dilakukan kapan saja.
