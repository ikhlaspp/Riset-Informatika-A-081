# 5 Rencana Evaluation Metric

## 5.1 Kelas positif dan confusion matrix

Kelas positif adalah respons berlabel halusinasi. TP berarti respons positif terdeteksi positif; FN berarti respons positif lolos sebagai negatif. FP berarti respons negatif ditandai positif, sedangkan TN berarti respons negatif terdeteksi negatif. Seluruh perhitungan dilakukan per respons setelah agregasi jendela, bukan per token atau per jendela.

| Label sebenarnya | Prediksi halusinasi | Prediksi nonhalusinasi |
| --- | --- | --- |
| Halusinasi | TP | FN |
| Nonhalusinasi | FP | TN |

## 5.2 Metrik utama dan pendukung

| Metrik | Rumus atau cara ukur | Alasan penggunaan |
| --- | --- | --- |
| Macro-F1 utama | F1 positif = 2TP / (2TP + FP + FN). F1 negatif = 2TN / (2TN + FP + FN). Macro-F1 = (F1 positif + F1 negatif) / 2. | Memberi bobot yang sama pada kedua kelas, meskipun jumlahnya tidak seimbang [10]. |
| Precision positif | TP / (TP + FP) | Menilai ketepatan peringatan halusinasi. |
| Recall positif | TP / (TP + FN) | Mengukur proporsi halusinasi yang berhasil ditemukan. |
| Average precision atau AP | Jumlah kenaikan recall pada tiap ambang dikalikan precision pada ambang itu, memakai skor probabilitas. | Menilai pemeringkatan kelas positif tanpa bergantung pada satu ambang; bukan luas trapezoidal kurva PR [11]. |
| Latensi | Median dan P95 milidetik per respons, termasuk pemilihan konteks dan seluruh jendela. | Memperlihatkan biaya tambahan BM25 pada perangkat yang sama. |
| Audit konteks | Token sumber yang dipakai, jumlah jendela, serta proporsi sumber melebihi alokasi. | Memastikan selisih hasil tidak hanya muncul karena perbedaan panjang masukan. |

Accuracy dicatat sebagai pelengkap. Pada label utama data uji kandidat, prediksi selalu negatif sudah menghasilkan accuracy 165/216 atau 76,4%, tetapi recall positifnya nol. Nilai ini adalah baseline aritmetis dari distribusi label, bukan hasil pelatihan model. Macro-F1 baseline tersebut sekitar 0,433.

## 5.3 Pemilihan model dan ambang

Checkpoint tiap strategi dan seed dipilih menurut macro-F1 validasi pada ambang 0,5. Ambang kemudian dicari pada validasi dari 0,05 sampai 0,95 dengan langkah 0,01. Jika setara, pilih yang terdekat dengan 0,5, lalu yang lebih kecil. Bobot kelas positif pada loss dihitung dari data latihan. Parameter, checkpoint, dan ambang tidak dipilih berdasarkan data uji.

## 5.4 Pembandingan dan ketidakpastian

Hasil utama adalah selisih macro-F1 B2 dikurangi B1 pada respons uji yang sama. Kedua seed dilaporkan terpisah beserta reratanya. Interval kepercayaan 95% dihitung melalui 2.000 bootstrap berpasangan menurut sumber; semua respons dari sumber terpilih ikut bersama. Seed tidak dihitung sebagai tambahan sampel independen.

Jika interval mencakup nol, hasil dilaporkan belum memberikan bukti yang meyakinkan tentang arah perbedaan pada sampel ini. Analisis tambahan memisahkan sumber yang muat dan yang melampaui alokasi berdasarkan tokenizer, lalu melaporkan jumlah positif dan negatif setiap kelompok. Metrik yang tidak terdefinisi ditulis NA beserta alasannya; AP tidak ditafsirkan jika tidak ada kelas positif. Tidak ada kelompok yang dihapus hanya karena hasilnya buruk.

## 5.5 Analisis kesalahan dan waktu pemrosesan

Sebanyak 20 respons dari gabungan FP/FN kedua strategi akan dipilih secara acak untuk pemeriksaan kualitatif; jika kurang, seluruhnya diperiksa. Sumber lengkap dibaca untuk membedakan bukti yang tidak terpilih dari bukti yang tersedia tetapi salah dinilai. Kasus angka, tanggal, dan entitas diberi catatan deskriptif. Pemeriksaan satu peneliti ini bukan anotasi benchmark baru atau bukti sebab-akibat.

Latensi diukur tiga kali setelah warm-up dengan perangkat, batch, dan urutan respons yang sama. Median dan P95 disertai token aktual serta jumlah jendela. Waktu pelatihan dicatat terpisah. Commit data/model, hash split, konfigurasi, seed, ambang, log, dan prediksi disimpan. Tabel hasil menyertakan dukungan kelas.

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
