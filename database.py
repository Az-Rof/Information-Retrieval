import mysql.connector  # Mengimpor pustaka mysql.connector untuk koneksi ke database MySQL
from mysql.connector import errorcode  # Mengimpor errorcode untuk menangani kesalahan koneksi

class DatabaseConnection:  # Mendefinisikan kelas untuk koneksi database
    def __init__(self, user, database):  # Metode inisialisasi untuk kelas
        config = {  # Konfigurasi untuk koneksi database
            'user': user,  # Nama pengguna untuk koneksi
            'database': database  # Nama database yang akan dihubungkan
        }
        try:
            self.db_connect = mysql.connector.connect(**config)  # Mencoba untuk menghubungkan ke database
            self.cursor = self.db_connect.cursor()  # Membuat objek cursor untuk eksekusi kueri
        except mysql.connector.Error as err:  # Menangani kesalahan koneksi
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")  # Kesalahan akses
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")  # Kesalahan database tidak ada
            else:
                print(err)  # Menampilkan kesalahan lainnya

    def select(self, query, params=None):  # Metode untuk menjalankan kueri SELECT
        self.cursor.execute(query, params)  # Menjalankan kueri
        return self.cursor.fetchall()  # Mengembalikan semua hasil kueri

    def execute(self, query, params=None):  # Metode untuk menjalankan kueri lainnya
        self.cursor.execute(query, params)  # Menjalankan kueri
        self.db_connect.commit()  # Menyimpan perubahan ke database

    def __del__(self):  # Metode destructor untuk membersihkan sumber daya
        self.cursor.close()  # Menutup cursor
        self.db_connect.close()  # Menutup koneksi database
