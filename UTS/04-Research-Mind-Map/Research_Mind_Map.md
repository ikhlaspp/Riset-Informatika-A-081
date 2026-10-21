# 4 Research Mind Map

Peta berikut menghubungkan masalah penelitian dengan data, metode, gap, evaluasi, dan luaran. Semua cabang merujuk pada rancangan riset kecil dalam dokumen ini.

![Research mind map](research_mind_map.png)

Gambar 1. Research mind map deteksi halusinasi berbasis pemilihan bukti.

## Alur kerja penelitian

Dataset kandidat → audit dan split final → pembentukan konteks B1/B2 → pelatihan detektor → pemilihan ambang pada validasi → evaluasi uji → analisis kesalahan.

Cabang evaluasi memberi dasar untuk menilai hipotesis. Cabang luaran mengarah pada simpulan tentang manfaat pemilihan konteks dalam batas eksperimen ini. LOGO baru ditambahkan pada tahap penelitian lanjutan.

## Peta rinci

![Peta rinci](research_mind_map_detail.png)

```mermaid
mindmap
  root((Deteksi halusinasi RAG))
    Masalah
      Ketidaksetiaan terhadap sumber; bukti terpotong
    Dataset
      240 sumber, 1.440 respons; split per sumber
    Metode
      B1 awal vs B2 BM25; DeBERTa-v3-base
    Kontrol
      512 token; respons 192; overlap 32; seed 13/42
    Evaluasi
      Macro-F1; AP; recall; latensi median dan P95
    Ketidakpastian
      2.000 bootstrap berpasangan menurut sumber
    Luaran
      Perbandingan lokal, prediksi, log, analisis FP/FN
    Lanjutan
      LOGO, awal-akhir, dan pembanding MiniCheck
```
