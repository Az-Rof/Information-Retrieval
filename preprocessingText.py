import nltk  # Mengimpor pustaka NLTK untuk pemrosesan bahasa alami
from nltk.corpus import wordnet  # Mengimpor WordNet untuk sinonim
from nltk.tokenize import word_tokenize  # Mengimpor fungsi untuk tokenisasi
from nltk.stem import WordNetLemmatizer  # Mengimpor lemmatizer dari NLTK
from nltk.corpus import stopwords  # Mengimpor daftar kata berhenti
import string  # Mengimpor pustaka string untuk manipulasi string

# Pastikan data NLTK yang diperlukan sudah diunduh
nltk.download('punkt')  # Mengunduh data tokenisasi
nltk.download('wordnet')  # Mengunduh data WordNet
nltk.download('stopwords')  # Mengunduh daftar kata berhenti

class PreprocessingText:  # Mendefinisikan kelas untuk pemrosesan teks
    def __init__(self):  # Metode inisialisasi untuk kelas
        # Inisialisasi lemmatizer dan daftar kata berhenti
        self.lemmatizer = WordNetLemmatizer()  # Membuat objek lemmatizer
        self.stop_words = set(stopwords.words('english'))  # Mengambil kata berhenti dalam bahasa Inggris

    def preprocess(self, text):  # Metode untuk memproses teks
        """
        Memproses teks dengan tokenisasi, normalisasi, dan lemmatization.
        """
        text = text.lower()  # Mengubah teks menjadi huruf kecil
        tokens = word_tokenize(text)  # Tokenisasi teks menjadi kata-kata
        processed_tokens = [  # Membuat daftar token yang telah diproses
            self.lemmatizer.lemmatize(word) for word in tokens  # Melakukan lemmatization pada setiap token
            if word not in self.stop_words and word not in string.punctuation  # Mengabaikan kata berhenti dan tanda baca
        ]
        return processed_tokens  # Mengembalikan token yang telah diproses

    def expand_query(self, query_tokens):  # Metode untuk memperluas kueri
        """
        Memperluas kueri menggunakan WordNet untuk menyertakan sinonim.
        """
        expanded_query = set(query_tokens)  # Menggunakan set untuk menghindari duplikasi
        for word in query_tokens:  # Iterasi setiap token dalam kueri
            for syn in wordnet.synsets(word):  # Mendapatkan sinonim dari WordNet
                for lemma in syn.lemmas():  # Iterasi setiap lemma dari sinonim
                    expanded_query.add(lemma.name())  # Menambahkan sinonim ke kueri yang diperluas
        return list(expanded_query)  # Mengembalikan kueri yang diperluas sebagai daftar


