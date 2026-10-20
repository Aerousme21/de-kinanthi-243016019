# Pemetaan Peran Batik Kinanthi

| No | Kebutuhan pemilik Batik Kinanthi | Peran utama | Alasan singkat | Tahap lifecycle |
|----|----------------------------------|-------------|----------------|-----------------|
| 1 | Data penjualan dari toko, web, dan marketplace dikumpulkan ke satu tempat setiap malam | Data Engineer | Memindahkan dan menyatukan data dari banyak sumber secara otomatis | Ingestion |
| 2 | Dashboard omzet harian per kanal | Data Analyst | Menyajikan jawaban atas apa yang terjadi, dari tabel siap pakai mart_omzet_harian | Serving |
| 3 | Prediksi kebutuhan stok kain bulan depan | Data Scientist | Membangun model peramalan dari riwayat penjualan | Serving |
| 4 | Tabel pelanggan tidak boleh berisi data ganda | Data Engineer | Menjaga kualitas data lewat deduplikasi dan aturan keunikan | Transformation |
| 5 | Laporan motif terlaris per kota untuk rapat bulanan | Data Analyst | Meringkas data menjadi laporan bagi pengambil keputusan | Serving |
| 6 | Rekomendasi produk untuk pelanggan di situs web | Data Scientist | Membangun model rekomendasi dari pola pembelian pelanggan | Serving |
| 7 | Data transaksi lama tetap tersimpan aman dan hemat biaya | Data Engineer | Merancang penyimpanan berjenjang, pencadangan, dan retensi data | Storage |
| 8 | Analisis penyebab penurunan penjualan marketplace bulan lalu | Data Analyst | Menelusuri penyebab suatu kejadian lewat eksplorasi dan perbandingan data | Serving |

## (a) Mengapa kebutuhan 3 dan 6 tidak dapat dikerjakan sebelum kebutuhan 1 dan 4 selesai?

Model prediksi stok (kebutuhan 3) dan model rekomendasi (kebutuhan 6) hanya sebaik data yang dipakai. Tanpa kebutuhan 1, penjualan tersebar di tiga kanal dan model hanya melihat sebagian permintaan, sehingga prediksi stok cenderung terlalu rendah. Tanpa kebutuhan 4, satu pelanggan dapat tercatat dua kali. Riwayat belinya terpecah menjadi dua profil, dan rekomendasi menjadi tidak akurat. Data Scientist berada di hilir, jadi hasil kerjanya bergantung pada keluaran Data Engineer di hulu.

## (b) Risiko satu orang merangkap tiga peran di UMKM dan bagian yang sebaiknya diotomatisasi lebih dulu

Ada empat risiko. Pertama, orang itu menjadi single point of failure: bila ia berhalangan, seluruh pengelolaan data berhenti. Kedua, tidak ada pemeriksaan silang karena pembuat dan penilai data adalah orang yang sama. Ketiga, pekerjaan hulu yang tidak terlihat, seperti kualitas data, cenderung dikorbankan demi laporan yang dibutuhkan hari itu. Keempat, pengetahuan tidak terdokumentasi dan hanya ada di satu kepala.

Bagian yang sebaiknya diotomatisasi lebih dulu adalah pengumpulan data malam hari (kebutuhan 1) beserta pemeriksaan kualitasnya (kebutuhan 4). Keduanya berulang, rawan salah bila dikerjakan manual, dan menjadi dasar bagi kebutuhan lain.
