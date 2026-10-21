# 2 Dataset Rencana Riset Kecil

Status berkas pendukung: angka bagian ini disalin dari draft. Berkas train.jsonl, validation.jsonl, test.jsonl, dan contoh_6_respons.jsonl yang disebut dalam draft tidak tersedia pada bahan yang diterima. Hitungan belum diaudit ulang terhadap data mentah. CSV agregat tersedia; CSV metadata per respons hanya berisi header sampai data asli tersedia.

## 2.1 Sumber dan unit data

Dataset berasal dari repositori resmi RAGTruth [9], diunduh pada 11 Oktober 2026 dengan commit c103204b9ce28d6bbad859304bf30de72b8ed8fe. Satu unit analisis adalah pasangan dokumen sumber dan respons. Berkas source_info.jsonl digabungkan dengan response.jsonl melalui source_id. Angka pada tabel berikut berasal dari pembacaan berkas, bukan perkiraan atau hasil model.

| Tahap audit | Jumlah aktual |
| --- | --- |
| Seluruh sumber Summary | 943 sumber |
| Seluruh respons Summary | 5.658 respons |
| Respons quality selain good | 3 respons dikeluarkan |
| Grup teks sumber duplikat persis setelah normalisasi | 1 grup berisi 2 source_id; 12 respons dikeluarkan |
| Subset kandidat terpilih | 240 sumber dan 1.440 respons |
| Kelas positif / negatif | 408 / 1.032 respons |
| Positif hanya karena implicit_true | 23 respons; disimpan untuk analisis sensitivitas |

## 2.2 Pembagian dataset kandidat

| Bagian | Sumber | Respons | Positif | Negatif |
| --- | --- | --- | --- | --- |
| Latihan | 168 | 1008 | 291 | 717 |
| Validasi | 36 | 216 | 66 | 150 |
| Uji | 36 | 216 | 51 | 165 |

Pemilihan dilakukan secara acak menurut sumber dengan seed 42, tanpa menyeimbangkan kelas. Latihan dan validasi diambil dari split train resmi; uji diambil dari split test resmi. Tidak ada source_id atau hash teks sumber yang beririsan antarbagiannya. Kemiripan sumber yang tidak identik masih perlu diperiksa sebelum split dibekukan. Jika ditemukan, sumber terkait dikelompokkan kembali dan semua hitungan diperbarui.

Berkas kandidat terlampir sebagai train.jsonl, validation.jsonl, dan test.jsonl. File contoh_6_respons.jsonl mengulang enam baris latihan untuk memperlihatkan strukturnya; file tersebut bukan data tambahan.

## 2.3 Skema data yang digunakan

| Atribut | Kegunaan |
| --- | --- |
| response_id; source_id; source_hash | Identitas respons, pengelompokan sumber, dan pemeriksaan duplikasi. |
| source_text; response_text | Teks asli yang menjadi masukan detektor. Tidak dinormalisasi ulang agar offset label tetap berlaku. |
| generator; source_origin | Identitas generator dan asal sumber untuk analisis deskriptif. |
| split; official_split | Bagian kandidat riset kecil dan asal pembagian resmi. |
| label; label_excluding_implicit_true | Label utama dan label alternatif untuk analisis sensitivitas. |
| original_labels; quality | Anotasi span asli beserta status kualitas yang dipertahankan. |

Label utama bernilai 1 jika daftar anotasi halusinasi tidak kosong, termasuk implicit_true, sesuai fokus ketat pada dukungan sumber. Nilai 0 berarti tidak ada span beranotasi halusinasi. Label alternatif bernilai 1 hanya jika sedikitnya satu anotasi tidak bertanda implicit_true. Kedua kebijakan tidak dicampur: analisis sensitivitas memakai prediksi utama yang sama, lalu menilai perubahan skor saat definisi label diubah.

## 2.4 Sebaran kelas menurut generator

| Generator | Positif total | Negatif total | Uji positif / negatif |
| --- | --- | --- | --- |
| gpt-3.5-turbo-0613 | 11 | 229 | 1 / 35 |
| gpt-4-0613 | 22 | 218 | 4 / 32 |
| llama-2-13b-chat | 76 | 164 | 7 / 29 |
| llama-2-70b-chat | 46 | 194 | 5 / 31 |
| llama-2-7b-chat | 112 | 128 | 13 / 23 |
| mistral-7B-instruct | 141 | 99 | 21 / 15 |

Setiap generator menyumbang 240 respons. Namun, data uji GPT-3.5 hanya memiliki satu contoh positif. Karena itu, perbandingan per generator bersifat deskriptif dan tidak digunakan untuk menyatakan bahwa suatu generator paling mudah dideteksi. Panjang token dan proporsi sumber yang terpotong belum diukur; istilah dokumen panjang belum dijadikan karakteristik seluruh subset.

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
