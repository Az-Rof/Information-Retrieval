import numpy as np  # Mengimpor pustaka NumPy untuk operasi numerik
from gensim.models import KeyedVectors  # Mengimpor KeyedVectors dari Gensim untuk memuat model word vectors
from preprocessingText import PreprocessingText  # Mengimpor kelas PreprocessingText untuk pemrosesan teks
from database import DatabaseConnection  # Mengimpor kelas DatabaseConnection untuk koneksi database


class Main:  # Mendefinisikan kelas utama
    def __init__(self):  # Metode inisialisasi untuk kelas
        self.db = DatabaseConnection('root', 'medicine')  # Membuat koneksi ke database
        self.preprocessing = PreprocessingText()  # Membuat objek untuk pemrosesan teks
        self.model = KeyedVectors.load_word2vec_format(  # Memuat model word vectors
            "model/GoogleNews-vectors-negative300-SLIM.bin.gz", binary=True
        )

    def run(self):  # Metode untuk menjalankan program
        query = "SELECT Medicine_Name, Uses, Composition, Side_Effects FROM medicine LIMIT 100"  # Kueri untuk mengambil data obat
        data = self.db.select(query)  # Menjalankan kueri dan mendapatkan data
        
        # Memproses data dengan menggabungkan nama dan penggunaan obat
        processed_data = [self.preprocessing.preprocess(' '.join(row[:2])) for row in data]
        document_vectors = [  # Menghitung vektor dokumen
            np.mean([self.model[word] for word in doc if word in self.model], axis=0) 
            for doc in processed_data
        ]

        user_query = input("Enter your search query: ")  # Meminta input kueri dari pengguna
        query_tokens = self.preprocessing.preprocess(user_query)  # Memproses kueri pengguna
        expanded_query_tokens = self.preprocessing.expand_query(query_tokens)  # Memperluas kueri dengan sinonim
        query_vector = np.mean(  # Menghitung vektor kueri
            [self.model[word] for word in expanded_query_tokens if word in self.model], 
            axis=0
        )

        # Menghitung kesamaan antara vektor dokumen dan vektor kueri
        similarities = [
            np.dot(doc_vec, query_vector) / (np.linalg.norm(doc_vec) * np.linalg.norm(query_vector)) 
            for doc_vec in document_vectors
        ]
        top_indices = np.argsort(similarities)[::-1][:10]  # Mengambil dokumen teratas berdasarkan kesamaan
        # Menampilkan dokumen yang cocok
        for index in top_indices:
            print("-----------------")
            print(f"Medicine Name : {data[index][0]}")
            print(f"Uses : {data[index][1]}")
            print(f"Composition : {data[index][2]}")
            print(f"Side Effects : {data[index][3]}")
            print(f"Similarity Score : {similarities[index]:.4f}")

if __name__ == "__main__":  # Memastikan bahwa skrip dijalankan sebagai program utama
    app = Main()  # Membuat objek dari kelas Main
    app.run()  # Menjalankan program

