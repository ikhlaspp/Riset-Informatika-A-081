# 3 Research Gap

## 3.1 Posisi terhadap penelitian terdahulu

| Penelitian | Temuan atau pendekatan | Hubungan dengan riset kecil |
| --- | --- | --- |
| RAGTruth [1] | Korpus beranotasi untuk mempelajari halusinasi dalam pengaturan RAG. | Menyediakan objek dan label; jumlah generator saja tidak membuktikan uji generalisasi. |
| SummaC [2] | Segmentasi kalimat dan agregasi skor NLI untuk konsistensi ringkasan. | Menjadi dasar bahwa cara memasangkan sumber dan keluaran memengaruhi evaluasi. |
| InFusE dan FENICE [3], [4] | Premis berukuran variabel, penyederhanaan hipotesis, atau ekstraksi klaim dan alignment. | Pemilihan bukti serta pemeriksaan klaim sudah diteliti; keduanya bukan klaim kebaruan riset ini. |
| Lost in the Middle [5] | Posisi informasi memengaruhi kinerja pada tugas konteks panjang yang diuji. | Memotivasi pemeriksaan posisi bukti; bukan bukti langsung untuk DeBERTa pada subset ini. |
| Stress Testing [6] | Evaluasi metrik pada dokumen panjang, termasuk sensitivitas konteks retrieval. | Anggaran konteks sudah dibahas; riset kecil memusatkan pembandingan pada dua strategi sederhana. |
| MiniCheck [7] | Pemeriksaan dukungan dokumen terhadap klaim menggunakan model relatif kecil. | Pembanding literatur yang lebih kuat; perbandingan langsung ditunda ke perluasan. |

## 3.2 Gap operasional dan kontribusi

Pertanyaan yang belum terjawab untuk rancangan ini adalah apakah pemilihan konteks BM25 lebih berguna daripada pemotongan awal pada subset RAGTruth yang sama ketika anggaran token dan model dikendalikan. Riset ini akan menyediakan perbandingan lokal, catatan latensi, dan contoh kegagalan untuk menjawabnya. Kajian yang digunakan belum cukup untuk menyatakan bahwa kombinasi tersebut belum pernah diteliti oleh siapa pun.

Kontribusi tugas kuliah adalah replikasi terarah dan evaluasi empiris dengan data serta protokol yang dapat diperiksa. Klaim bahwa BM25 lebih baik hanya dibuat jika hasil mendukungnya. Pengaruh perubahan konteks dinilai dari perbandingan B1/B2; temuan tidak langsung digeneralisasi ke dataset atau keluarga model lain.

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
