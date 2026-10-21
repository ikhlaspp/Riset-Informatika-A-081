# Riset Informatika A 081

## Deteksi Halusinasi pada Ringkasan RAGTruth

Perbandingan pemotongan awal dan pemilihan bukti BM25 dengan DeBERTa-v3-base pada anggaran 512 token. Isi lima dokumen berasal dari `Draft_ETS_Riset_Informatika_Halusinasi_RAG.docx`; struktur mengikuti ZIP contoh.

| Direktori | Isi |
|---|---|
| [01-Proposal-Penelitian](UTS/01-Proposal-Penelitian/Proposal_Penelitian.md) | Proposal Markdown dan PDF |
| [02-Dataset](UTS/02-Dataset/README.md) | Dokumentasi, distribusi agregat, visualisasi, template metadata, skrip audit, folder sampel |
| [03-Research-Gap](UTS/03-Research-Gap/Research_Gap.md) | Peta literatur dan gap operasional Markdown dan PDF |
| [04-Research-Mind-Map](UTS/04-Research-Mind-Map/Research_Mind_Map.md) | Mind map asli draft, peta detail, Mermaid, PDF |
| [05-Evaluation-Metric](UTS/05-Evaluation-Metric/Rencana_Evaluation_Metric.md) | Protokol evaluasi Markdown/PDF dan empat template CSV pilot |
| [06-Kode](UTS/06-Kode/README.md) | Skrip audit dan evaluasi serta konfigurasi eksperimen |

## Status kelengkapan

Dokumentasi dan struktur folder telah dibuat. Data mentah dan eksperimen belum tersedia dalam bahan yang diterima. Angka distribusi berasal dari draft, bukan hasil audit baru. Daftar pustaka dipertahankan dari draft dan tidak diverifikasi ulang.

- `train.jsonl`, `validation.jsonl`, `test.jsonl`, dan `contoh_6_respons.jsonl` disebut dalam draft, tetapi tidak dilampirkan pada DOCX atau direktori sumber.
- `dataset_metadata.csv`, `sampel_metadata.csv`, dan `label_halusinasi.csv` hanya berisi header sampai data nyata tersedia. Folder `sampel` memuat petunjuk pengisian.
- Empat CSV `pilot_*` hanya berisi header; model belum dilatih dan tidak ada hasil eksperimen yang diklaim.
- Kode tersedia untuk audit metadata dan evaluasi prediksi. Pelatihan B1/B2, pemilihan bukti, audit token, bootstrap, dan pengukuran latensi masih berupa rencana.
- Nama aset Digimon dari contoh diganti menjadi RAGTruth. Data, identitas penulis, dan hasil eksperimen teman tidak disalin.

## Penggunaan

1. Baca lima dokumen melalui tautan di atas.
2. Letakkan split JSONL asli di `UTS/02-Dataset/`.
3. Jalankan `python UTS/02-Dataset/build_metadata.py` untuk memvalidasi data dan membangun metadata serta enam sampel latihan.
4. Baca [petunjuk kode](UTS/06-Kode/README.md) untuk evaluasi prediksi.

PDF mempertahankan isi dan tabel draft dengan tata letak ulang per bagian. Nama `_FIX.pdf` mengikuti pola contoh, bukan tanda eksperimen telah selesai.
