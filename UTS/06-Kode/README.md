# Kode pendukung riset RAGTruth

`research_protocol.json` merekam rencana eksperimen dalam draft. Skrip pada folder ini menghitung metrik dari prediksi yang sudah tersedia. Pelatihan DeBERTa, pembentukan konteks B1/B2, audit token, loss agregat respons, bootstrap, dan pengukuran latensi belum diimplementasikan. Tidak ada model yang sudah dilatih di paket ini.

## Audit dataset

Letakkan tiga split JSONL asli di `UTS/02-Dataset`, lalu dari root repositori:

```powershell
python UTS/02-Dataset/build_metadata.py
```

Skrip memeriksa kolom, kualitas, konsistensi label, duplikasi ID respons, dan kebocoran source_id serta hash teks yang dinormalisasi. Audit ini belum mencakup kemiripan nonidentik. Metadata dibuat hanya setelah semua split lolos pemeriksaan. Data sumber dan offset anotasi tidak diubah. Bandingkan hitungan audit aktual dengan angka kandidat dalam draft sebelum membekukan split.

## Evaluasi prediksi

CSV wajib memuat `response_id,source_id,strategy,seed,label,probability`. Satu baris per respons per strategi dan seed. Probabilitas harus sudah diagregasi maksimum antarjendela. Jangan memasukkan prediksi per jendela.

```powershell
python UTS/06-Kode/ragtruth_pipeline.py prediksi_uji.csv --validation prediksi_validasi.csv --output hasil/metrik.json
```

Skrip memilih ambang 0,05 sampai 0,95 dari validasi berdasarkan macro-F1, lalu menerapkan ambang itu pada uji. Jika skor setara, ambang terdekat dengan 0,5 dipilih, kemudian yang lebih kecil. Pemilihan checkpoint pada ambang 0,5 harus dilakukan terpisah sebelum menyiapkan prediksi. Source_id validasi dan uji tidak boleh beririsan.

Jika ambang sudah dibekukan dari validasi:

```powershell
python UTS/06-Kode/ragtruth_pipeline.py prediksi_uji.csv --threshold 0.5 --output hasil/metrik.json
```

Output JSON berisi confusion matrix, macro-F1, precision, recall, AP, dan accuracy per strategi/seed. `null` berarti NA karena metrik tidak terdefinisi. AP menangani skor probabilitas yang sama sebagai satu kelompok. CSV pilot kosong sengaja ditolak. Tidak ada hasil yang dibuat tanpa masukan nyata.

Python 3.10+ cukup untuk kedua skrip; tidak perlu paket eksternal. Kebutuhan GPU dan dependensi pelatihan ditentukan saat implementasi/pilot berikutnya.
