import mysql.connector # Meng import module mysql
import os # Opsional
os.system("cls") # Opsional

# Koneksi ke Database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="db_alpro" #Tergantung nama database yang di buat dalam PHPMYADMIN (MYSQL)
)

# Menu Registrasi
def registrasi(db):
    cursor = db.cursor()
    print("\n======== HALAMAN REGISTRASI ========")
    ussername = input("Masukkan Ussername Anda: ")
    password = input("Masukkan Password Anda: ")
    tgl_lahir = input("Masukkan Tanggal lahir Anda (DD): ")
    sql = "INSERT INTO login(username, password, tgl_lahir) VALUES (%s, %s, %s)"
    val = (ussername, password, tgl_lahir)
    cursor.execute(sql, val)
    db.commit()

    if cursor.rowcount == 1:
        print("\nBerhasil Registrasi ")
        print("")
    else: 
        print("")

# Menu Login
def login(db):
    cursor = db.cursor()
    print("\n========== HALAMAN LOGIN ==========")
    ussername = input("Masukkan Ussername Anda: ")
    password = input("Masukkan Password Anda: ")
    tgl_lahir = input("Masukkan Tanggal Lahir Anda (DD): ")
    sql = "SELECT * FROM login WHERE username=%s AND password=%s AND tgl_lahir=%s"
    val = (ussername, password, tgl_lahir)
    cursor.execute(sql, val)

    result = cursor.fetchall()

    if result:
        login == "berhasil"
        print("\nLogin berhasil")
        print("")
    else:
        print("\nLogin gagal")
        print("")
        
# Menu Utama
def main(db):
    while True:
        pilihan = input("Apakah anda sudah memiliki akun? (y/t/q): ").upper()
        if pilihan == "Y":
            login(db)
        elif pilihan == "T":
            registrasi(db)
        elif pilihan == "Q":
            break
        else:
            print("\nMohon Masukkan Inputan yang sesuai..!")
            print("")

main(db)
