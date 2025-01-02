import mysql.connector
from mysql.connector import errorcode
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import string
from gensim.models import KeyedVectors
import numpy as np

class DatabaseConnection:
    def __init__(self, user, database):
        self.config = {
            'user': user,
            'database': database,
        }
        try:
            self.db_connect = mysql.connector.connect(**self.config)
            self.cursor = self.db_connect.cursor()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

    def select(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def __del__(self):
        self.cursor.close()
        self.db_connect.close()

def preprocess(text):
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')

    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))

    text = text.lower()
    tokens = word_tokenize(text)
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words and word not in string.punctuation]
    return tokens

def main():
    db = DatabaseConnection('root', 'medicine')
    query = "SELECT Medicine_Name, Composition, Uses FROM medicine LIMIT 100"
    data = db.select(query)

    model_path = "model\GoogleNews-vectors-negative300-SLIM.bin.gz"  # Path to the pretrained model
    model = KeyedVectors.load_word2vec_format(model_path, binary=True)  # Load the model

    processed_data = [preprocess(' '.join(row)) for row in data]
    document_vectors = [np.mean([model[word] for word in doc if word in model], axis=0) for doc in processed_data]

    user_query = input("Enter your search query: ")
    query_vector = preprocess(user_query)
    query_vector = np.mean([model[word] for word in query_vector if word in model], axis=0)

    similarities = [np.dot(doc_vec, query_vector) / (np.linalg.norm(doc_vec) * np.linalg.norm(query_vector)) for doc_vec in document_vectors]
    top_indices = np.argsort(similarities)[::-1][:10]

    print("Top matching documents:")
    for index in top_indices:
        print(f"Document {index + 1}: ", ' '.join(data[index]))

if __name__ == "__main__":
    main()
