from gensim.models import KeyedVectors
import numpy as np
import preprocessingText as pt
from tabulate import tabulate
import database
from sklearn.metrics import precision_score, recall_score

def main():
    # Koneksi database
    db = database.DatabaseConnection('root', 'medicine')
    query = "SELECT Medicine_Name, Uses FROM medicine LIMIT 100"
    data = db.select(query)
    
    # Memuat model word2vec yang telah dilatih
    model_path = "model/GoogleNews-vectors-negative300-SLIM.bin.gz"
    model = KeyedVectors.load_word2vec_format(model_path, binary=True)

    # Pra-pemrosesan data
    processed_data = [pt.preprocess(' '.join(row)) for row in data]
    document_vectors = [np.mean([model[word] for word in doc if word in model], axis=0) for doc in processed_data]

    # Masukan pengguna untuk kueri dan komputasi vektor yang sesuai
    user_query = input("Enter your search query: ")
    query_vector = pt.preprocess(user_query)
    query_vector = np.mean([model[word] for word in query_vector if word in model], axis=0)

    # Menghitung kesamaan dan mengambil dokumen teratas
    similarities = [np.dot(doc_vec, query_vector) / (np.linalg.norm(doc_vec) * np.linalg.norm(query_vector)) for doc_vec in document_vectors]
    top_indices = np.argsort(similarities)[::-1][:10]

    # Menampilkan dokumen yang paling cocok beserta skornya
    print("\nTop matching documents:")
    headers = ["Medicine Name", "Composition", "Uses", "Side Effects", "Similarity Score"]
    table_data = []
    
    predicted_labels = []  # Menyimpan prediksi (1 untuk relevan, 0 untuk tidak relevan)
    ground_truth_labels = []  # Menyimpan label ground truth
    
    # Iterasi hasil prediksi dan simpan ke tabel relevance_labels
    for index in top_indices:
        full_details_query = "SELECT Medicine_Name, Composition, Uses, Side_effects FROM medicine WHERE Medicine_Name = %s"
        full_details_data = db.select(full_details_query, (data[index][0],))
        if full_details_data:
            # Menambahkan skor kesamaan ke data tabel
            row = list(full_details_data[0])  # Ubah tuple menjadi list untuk memodifikasi
            row.append(f"{similarities[index]:.4f}")  # Format skor kesamaan dengan 4 angka desimal
            table_data.append(row)
            
            # Evaluasi relevansi berdasarkan threshold
            is_relevant = 1 if similarities[index] > 0.7 else 0  # Threshold relevansi
            predicted_labels.append(is_relevant)  # Simpan prediksi relevansi
            
            # Asumsi ground truth dari threshold sementara
            # Jika Anda memiliki tabel relevance_labels, ambil dari sana
            ground_truth_labels.append(1 if similarities[index] > 0.5 else 0)  # Sesuaikan threshold
            
            # Simpan relevansi ke tabel relevance_labels
            insert_query = """
            INSERT INTO relevance_labels (Medicine_Name, Relevance)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE Relevance = VALUES(Relevance)
            """
            db.execute(insert_query, (data[index][0], is_relevant))

    # Tampilkan tabel dengan tabulate
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    
    # Evaluasi model dengan precision dan recall
    if predicted_labels and ground_truth_labels:
        precision = precision_score(ground_truth_labels, predicted_labels)
        recall = recall_score(ground_truth_labels, predicted_labels)
        print("\nEvaluation Metrics:")
        print(f"Precision: {precision:.4f}")
        print(f"Recall: {recall:.4f}")
    else:
        print("\nEvaluation Metrics:")
        print("Insufficient data for precision and recall calculation.")

if __name__ == "__main__":
    main()