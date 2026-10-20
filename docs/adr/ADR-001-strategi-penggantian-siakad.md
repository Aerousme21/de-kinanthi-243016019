# ADR-001: Strategi penggantian SIAKAD kampus

**Status** : diusulkan

**Konteks** : SIAKAD kampus berjalan di atas teknologi lama yang sulit dikembangkan dan dirawat. Sistem ini melayani proses akademik yang tidak boleh terhenti, misalnya pengisian KRS dan input nilai. Kampus memerlukan sistem yang lebih mudah dikembangkan tanpa mengganggu layanan yang sedang berjalan.

**Opsi** :

| Opsi | Uraian | Biaya | Latensi manfaat | Kompleksitas |
|------|--------|-------|-----------------|--------------|
| A. Big-bang rewrite | Seluruh SIAKAD ditulis ulang, lalu semua pengguna dipindah dalam satu waktu | Besar di muka, dibayar sebelum ada manfaat | Lama: manfaat baru terasa setelah go-live | Tinggi pada migrasi data dan cutover. Bila gagal, sistem lama sudah dimatikan |
| B. Strangler pattern | Fungsi diganti modul demi modul di belakang lapisan routing yang mengarahkan permintaan ke sistem lama atau baru | Tersebar mengikuti jadwal tiap modul | Cepat: modul pertama sudah memberi manfaat lebih awal | Sedang: dua sistem berjalan paralel dan data harus disinkronkan sementara |
| C. Pertahankan dan tambal sistem lama | Sistem lama tetap dipakai dan diperbaiki seperlunya | Rendah di awal | Segera, tetapi tidak menyelesaikan akar masalah | Rendah sekarang, utang teknis terus bertambah |

**Keputusan** : Opsi B, strangler pattern. Opsi A ditolak karena seluruh risiko menumpuk pada satu hari pergantian, dan kegagalan tidak dapat dibatalkan dengan murah. Opsi C ditolak karena hanya menunda masalah. Opsi B memungkinkan setiap modul dicoba, diukur, dan dikembalikan bila bermasalah.

**Tipe** : One-way door untuk opsi A (big-bang rewrite). Opsi B yang dipilih memecah keputusan itu menjadi serangkaian langkah two-way door.

**Konsekuensi** :
- Dampak: layanan akademik tetap berjalan selama migrasi, dan manfaat diperoleh bertahap.
- Risiko: periode dua sistem paralel menambah beban operasional dan risiko data tidak sinkron. Perlu pemantauan konsistensi data antarsistem.
- Exit plan: selama sistem lama belum dimatikan, setiap modul dapat dialihkan kembali ke sistem lama lewat pengaturan routing. Sistem lama baru dimatikan setelah seluruh modul stabil dan data tervalidasi.
