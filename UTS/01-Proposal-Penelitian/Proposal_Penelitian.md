# 1 Proposal Penelitian

## 1.1 Judul penelitian

Perbandingan Pemotongan Awal dan Pemilihan Bukti BM25 untuk Deteksi Halusinasi pada Ringkasan RAGTruth

## 1.2 Ringkasan rencana

Riset kecil ini membandingkan dua cara menyediakan konteks bagi detektor: mengambil bagian awal dokumen dan memilih potongan yang relevan menggunakan BM25. Kedua strategi memakai model yang sama serta batas masukan 512 token. Dataset kandidat terdiri atas 1.440 pasangan sumber–respons dari 240 sumber RAGTruth. Hasil yang akan dinilai adalah macro-F1 dan biaya pemrosesan. Dataset telah disiapkan, sedangkan audit token, pelatihan, dan pengujian model masih merupakan rencana.

## 1.3 Latar belakang

Retrieval-augmented generation (RAG) menyediakan konteks dokumen untuk membantu model menghasilkan jawaban atau ringkasan. Namun, responsnya masih dapat memuat informasi yang tidak didukung atau bertentangan dengan sumber. RAGTruth menyediakan korpus beranotasi untuk mempelajari masalah tersebut [1]. Dalam penelitian ini, halusinasi dibatasi pada ketidaksetiaan terhadap sumber. Pernyataan yang tidak tercantum dalam dokumen belum tentu salah menurut pengetahuan di luar dokumen.

Cara memasangkan keluaran dengan bukti telah diteliti melalui SummaC [2], InFusE [3], dan FENICE [4]. Posisi informasi dalam konteks juga dapat memengaruhi kinerja model bahasa [5]. Kajian pada ringkasan dokumen panjang menunjukkan bahwa metrik konsistensi sensitif terhadap konteks retrieval [6]. Literatur tersebut menjadi dasar untuk membandingkan strategi konteks dalam kondisi yang terkontrol.

Pemotongan awal dapat menghilangkan bukti pada bagian berikutnya. BM25 memilih potongan yang dekat secara leksikal dengan respons, tetapi kedekatan kata belum menjamin dukungan makna. Manfaatnya akan diuji pada batas token yang sama. MiniCheck [7] menjadi acuan literatur untuk pembanding pada pengembangan berikutnya.

## 1.4 Rumusan masalah

1.Apakah pemilihan bukti BM25 menghasilkan macro-F1 yang berbeda dari pemotongan awal ketika arsitektur, data, dan batas token disamakan?

2.Bagaimana perbedaan recall halusinasi, kesalahan prediksi, dan latensi kedua strategi, khususnya pada sumber yang melebihi alokasi konteks?

## 1.5 Tujuan dan manfaat

Penelitian ini mengukur perbedaan kualitas deteksi dan latensi kedua strategi untuk menilai apakah biaya pemilihan bukti sebanding dengan manfaatnya. Contoh kegagalan akan ditelaah, sedangkan pembagian data dan konfigurasi disimpan agar eksperimen dapat diulang.

## 1.6 Ruang lingkup dan hipotesis kerja

Eksperimen memakai respons berbahasa Inggris pada tugas Summary. Prediksi biner dibuat pada tingkat respons sesuai anotasi sumber, tanpa generasi baru, pencarian web, atau prediksi lokasi span. Enam generator dicampur dalam setiap bagian data; skor per generator digunakan untuk diagnosis.

Hipotesis kerja: BM25 dapat meningkatkan macro-F1 ketika sumber tidak seluruhnya muat, dengan tambahan waktu retrieval. Arah tersebut belum diketahui dari eksperimen ini. Jika skor tidak meningkat, analisis tetap akan memeriksa apakah pemilihan bukti membuang konteks yang diperlukan.

Pengujian leave-one-generator-out (LOGO), strategi awal–akhir, dan anotasi kesalahan berskala besar tetap menjadi perluasan untuk skripsi. Dengan demikian, riset kecil ini tidak digunakan untuk menyimpulkan generalisasi ke generator yang belum pernah masuk pelatihan.

## 1.7 Rancangan eksperimen

| Komponen | Rencana tetap |
| --- | --- |
| B1 | DeBERTa-v3-base dengan klasifikasi biner; konteks diambil dari awal sumber. |
| B2 | Arsitektur sama; BM25 memilih potongan dalam sumber yang sama menggunakan respons lengkap sebagai kueri. |
| Masukan | Maksimum 512 token. Respons dialokasikan sampai 192 token per jendela; sisa untuk sumber dan token khusus. |
| Pelatihan | AdamW, learning rate 2 × 10⁻⁵, maksimum 3 epoch, effective batch 16; seed 13 dan 42. Total empat run utama. |
| Kontrol | Split, checkpoint awal untuk seed yang sama, tokenizer, anggaran token, loss, dan aturan pemilihan model disamakan. |

Checkpoint yang digunakan adalah microsoft/deberta-v3-base [8]. Sumber dibagi menurut kalimat, maksimum 128 token per potongan tanpa overlap. BM25 memakai token leksikal huruf kecil tanpa tanda baca, k1 = 1,5 dan b = 0,75. Skor setara diurutkan menurut posisi awal. Potongan diambil hingga alokasi penuh; kandidat terakhir dipotong bila perlu, lalu semua potongan diurutkan kembali menurut sumber.

Respons di atas 192 token memakai jendela beririsan 32 token. Probabilitas maksimum antarjendela menjadi skor respons, dan loss dihitung pada skor agregat tersebut. Jendela tidak otomatis mewarisi label positif respons. Kedua strategi memakai alokasi sumber sebesar 512 dikurangi 192 dan jumlah token khusus tokenizer. Token aktual dicatat.

## 1.8 Tahapan pelaksanaan

| Minggu | Kegiatan dan luaran |
| --- | --- |
| 1 | Audit kemiripan sumber dan panjang token; tetapkan dataset, label, dan split final. |
| 2 | Implementasi B1/B2 dan pilot 50 respons latihan; ukur kebutuhan memori dan durasi. |
| 3 | Empat run utama; pilih model serta ambang hanya pada validasi. |
| 4 | Evaluasi uji, analisis kesalahan, dan penulisan laporan. |

Jadwal dimulai setelah akses komputasi tersedia. Kebutuhan GPU dan durasi diukur saat pilot; revisi cakupan dilakukan sebelum evaluasi uji.

## Daftar Pustaka

[1] C. Niu et al., “RAGTruth: A Hallucination Corpus for Developing Trustworthy Retrieval-Augmented Language Models,” in Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pp. 10862–10878, 2024, doi: 10.18653/v1/2024.acl-long.585.

[2] P. Laban, T. Schnabel, P. N. Bennett, and M. A. Hearst, “SummaC: Re-Visiting NLI-based Models for Inconsistency Detection in Summarization,” Transactions of the Association for Computational Linguistics, vol. 10, pp. 163–177, 2022, doi: 10.1162/tacl_a_00453.

[3] H. Zhang, Y. Xu, and L. Perez-Beltrachini, “Fine-Grained Natural Language Inference Based Faithfulness Evaluation for Diverse Summarisation Tasks,” in Proceedings of the 18th Conference of the European Chapter of the Association for Computational Linguistics (Volume 1: Long Papers), pp. 1701–1722, 2024, doi: 10.18653/v1/2024.eacl-long.102.

[4] A. Scirè, K. Ghonim, and R. Navigli, “FENICE: Factuality Evaluation of summarization based on Natural language Inference and Claim Extraction,” in Findings of the Association for Computational Linguistics: ACL 2024, pp. 14148–14161, 2024, doi: 10.18653/v1/2024.findings-acl.841.

[5] N. F. Liu et al., “Lost in the Middle: How Language Models Use Long Contexts,” Transactions of the Association for Computational Linguistics, vol. 12, pp. 157–173, 2024, doi: 10.1162/tacl_a_00638.

[6] Z. M. Mujahid, D. Wright, and I. Augenstein, “Stress Testing Factual Consistency Metrics for Long-Document Summarization,” in Proceedings of the 64th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pp. 31914–31933, 2026, doi: 10.18653/v1/2026.acl-long.1472.

[7] L. Tang, P. Laban, and G. Durrett, “MiniCheck: Efficient Fact-Checking of LLMs on Grounding Documents,” in Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing, pp. 8818–8847, 2024, doi: 10.18653/v1/2024.emnlp-main.499.

[8] Microsoft, “microsoft/deberta-v3-base,” Hugging Face, model card. Diakses 11 Oktober 2026. [Online]. Tersedia: https://huggingface.co/microsoft/deberta-v3-base

[9] ParticleMedia, “RAGTruth,” GitHub repository, commit c103204b9ce28d6bbad859304bf30de72b8ed8fe. Diakses 11 Oktober 2026. [Online]. Tersedia: https://github.com/ParticleMedia/RAGTruth

[10] Scikit-learn developers, “f1_score,” Scikit-learn documentation. Diakses 11 Oktober 2026. [Online]. Tersedia: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html

[11] Scikit-learn developers, “average_precision_score,” Scikit-learn documentation. Diakses 11 Oktober 2026. [Online]. Tersedia: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.average_precision_score.html
