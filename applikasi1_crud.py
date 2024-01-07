import mysql.connector # Meng import module mysql
import os # Opsional
import time # Opsional
os.system("cls") # Opsional

# Koneksi ke Database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="db_alpro" # Tergantung nama database yang di buat dalam PHPMYADMIN (MYSQL)
)

# Membuat data (Create Data)
def create_data(db):
    cursor = db.cursor()
    nim = int(input("\n>>> Masukkan NIM: "))
    nama = input(">>> Masukkan Nama Mahasiswa: ")
    prodi = input(">>> Masukkan Prodi Mahasiswa: ")
    mk = input(">>> Masukkan Mata Kuliah: ")
    nilai_uh1 = int(input("\n>>> Masukkan Nilai Ulangan Harian Pertama: "))
    nilai_uh2 = int(input(">>> Masukkan Nilai Ulangan Harian Kedua: "))
    nilai_uts = int(input(">>> Masukkan Nilai Ulangan Tengah Semester: "))
    nilai_uas = int(input(">>> Masukkan Nilai Ulangan Akhir Semester: "))

    total_uh = (nilai_uh1 + nilai_uh2) / 2
    total_nilai = 0.3 * total_uh + nilai_uts * 0.3 + nilai_uas * 0.4

    if total_nilai > 80:
        nilai_huruf = "A"
    elif total_nilai > 60:
        nilai_huruf = "B"
    elif total_nilai > 40:
        nilai_huruf = "C"
    elif total_nilai > 20:
        nilai_huruf = "D"
    else:
        nilai_huruf = "E"

    sql = "INSERT INTO crud(nim_mahasiswa, nama_mahasiswa, prodi_mahasiswa, mk_mahasiswa, nilai_uh1, nilai_uh2, nilai_uts, nilai_uas, total_nilai, nilai_huruf) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (nim, nama, prodi, mk, nilai_uh1, nilai_uh2, nilai_uts, nilai_uas, total_nilai, nilai_huruf)
    cursor.execute(sql, val)
    db.commit()

    if cursor.rowcount == 0:
        print("\nTidak ada data yang diubah")
        print("")
    else: 
        print("\n{} data berhasil ditambahkan ".format(cursor.rowcount))
        print("")

# Melihatkan data (Read Data)
def read_data(db):
    cursor = db.cursor()
    print("\n=== MENU TAMPIL DATA ===")
    cari_nim = input(">>> Masukkan NIM yang ingin dicari: ")
    sql = "SELECT * FROM crud WHERE nim_mahasiswa=%s"
    val = (cari_nim,)
    cursor.execute(sql, val)
    fetch = cursor.fetchall()
    
    for data in fetch:
        if data[0] == cari_nim:
            print("\n>>> DATA MAHASISWA <<<")
            print("==============================================")
            print("NIM                  : ", data[0])
            print("Nama Mahasiswa       : ", data[1])
            print("Prgram Studi         : ", data[2])
            print("Mata Kuliah          : ", data[3])
            print("Total Nilai          : ", data[8])
            print("Nilai Huruf          : ", data[9])
            print("==============================================")
    
    if cursor.rowcount == 0:
        print("\nTidak ada data yang diubah")
        print("")
    else: 
        print("\n{} data berhasil diperlihatkan ".format(cursor.rowcount))
        print("")

# Mengubah Data (Update Data)
def update_data(db):
    cursor = db.cursor()
    nim_lama = input("\n>>> Masukkan NIM yang ingin diubah: ")
    sql = "SELECT * FROM crud WHERE nim_mahasiswa=%s"
    val = (nim_lama,)
    cursor.execute(sql, val)
    fetch = cursor.fetchall()

    for data in fetch:
        if data[0] == nim_lama:
            print("\n>>> DATA MAHASISWA <<<")
            print("==============================================")
            print("NIM                  : ", data[0])
            print("Nama Mahasiswa       : ", data[1])
            print("Prgram Studi         : ", data[2])
            print("Mata Kuliah          : ", data[3])
            print("Total Nilai          : ", data[8])
            print("Nilai Huruf          : ", data[9])
            print("==============================================")

    while True:
        print("\n=== OPSI PERUBAHAN ===")
        print("[1] Ubah NIM")
        print("[2] Ubah Nama")
        print("[3] Ubah Prodi")
        print("[4] Ubah Mata Kuliah")
        print("[5] Kembali")
        print("===========================")
        pilihan_ubah = int(input(">>> Data apa yang ingin diubah? [1/2/3/4]: "))
        
        if pilihan_ubah == 1:
            nim_baru = input(">>> Masukkan NIM baru: ")
            sql2 = "UPDATE crud SET nim_mahasiswa=%s WHERE nim_mahasiswa=%s"
            val2 = (nim_baru, nim_lama)
            cursor.execute(sql2, val2)
            break

        elif pilihan_ubah == 2:
            nama_baru = input(">>> Masukkan Nama baru: ")
            sql2 = "UPDATE crud SET nama_mahasiswa=%s WHERE nim_mahasiswa=%s"
            val2 = (nama_baru, nim_lama)
            cursor.execute(sql2, val2)
            break

        elif pilihan_ubah == 3:
            prodi_baru = input(">>> Masukkan Prodi Baru: ")
            sql2 = "UPDATE crud SET prodi_mahasiswa=%s WHERE nim_mahasiswa=%s"
            val2 = (prodi_baru, nim_lama)
            cursor.execute(sql2, val2)
            break

        elif pilihan_ubah == 4:
            mk_baru = input(">>> Masukkan Mata Kuliah Baru: ")
            sql2 = "UPDATE crud SET mk_mahasiswa=%s WHERE nim_mahasiswa=%s"
            val2 = (mk_baru, nim_lama)
            cursor.execute(sql2, val2)
            break

        elif pilihan_ubah == 5:
            break
        else:
            print("Pilihan tidak valid!")
            continue
    
    db.commit()
    
    if cursor.rowcount == 0:
        print("\nTidak ada data yang diubah")
        print("")
    else: 
        print("\n{} data berhasil diubah ".format(cursor.rowcount))
        print("")
    

# Menghapus Data (Delete Data)
def delete_data(db):
    cursor = db.cursor()
    nim_dicari = input("\n>>> Masukkan NIM data yang ingin dihapus: ")

    sql = "DELETE FROM crud WHERE nim_mahasiswa=%s"
    val = (nim_dicari,)
    cursor.execute(sql, val)
    db.commit()

    if cursor.rowcount == 0:
        print("\nTidak ada data yang diubah")
        print("")
    else: 
        print("\n{} data berhasil dihapus ".format(cursor.rowcount))
        print("")

# Hanya Administrator
def admin_only(db):
    cursor = db.cursor()
    sql = "SELECT * FROM crud"
    cursor.execute(sql)
    fetch = cursor.fetchall()
    
    print("\nMenampilkan Seluruh Data yang ada di Database...")
    time.sleep(3)
    print("\n==================================================")
    
    for i in fetch:
        print("NIM: ", i[0])
        print("Nama Mahasiswa: ", i[1])
        print("Prodi Mahasiswa: ", i[2])
        print("Mata Kuliah Mahasiswa: ", i[3])
        print("Nilai Ulangan Harian Pertama: ", i[4])
        print("Nilai Ulangan Harian: ", i[5])
        print("Nilai Ujian Tengah Semester: ", i[6])
        print("Nilai Ujian Akhir Semester: ", i[7])
        print("Total Nilai Mahasiswa: ", i[8])
        print("Nilai Huruf: ", i[9])
        print("==================================================")
    print("")

    nim_lama = input("\n>>> Masukkan NIM yang ingin diubah: ")
    sql = "SELECT * FROM crud WHERE nim_mahasiswa=%s"
    val = (nim_lama,)
    cursor.execute(sql, val)
    fetch = cursor.fetchall()
    
    for data in fetch:
        if data[0] == nim_lama:
            print("\n>>> DATA MAHASISWA <<<")
            print("==============================================")
            print("NIM: ", data[0])
            print("Nama Mahasiswa: ", data[1])
            print("Prodi Mahasiswa: ", data[2])
            print("Mata Kuliah Mahasiswa: ", data[3])
            print("Nilai Ulangan Harian Pertama: ", data[4])
            print("Nilai Ulangan Harian: ", data[5])
            print("Nilai Ujian Tengah Semester: ", data[6])
            print("Nilai Ujian Akhir Semester: ", data[7])
            print("Total Nilai Mahasiswa: ", data[8])
            print("Nilai Huruf: ", data[9])
            print("==============================================")



    while True:
        print("\n============== OPSI PERUBAHAN ==============")
        print("[1] Ubah NIM")
        print("[2] Ubah Nama")
        print("[3] Ubah Prodi")
        print("[4] Ubah Mata Kuliah")
        print("[5] Ubah Nilai Ulangan Harian Pertama")
        print("[6] Ubah Nilai Ulangan Harian Kedua")
        print("[7] Ubah Nilai Ujian Tengah Semester")
        print("[8] Ubah Nilai Ujian Akhir Semester")
        print("[9] Kembali")
        print("===============================================")
        pilihan_ubah = int(input(">>> Data apa yang ingin diubah? [1/2/3/4/5/6/7/8/9]: "))
        
        if pilihan_ubah == 1:
            nim_baru = input(">>> Masukkan NIM baru: ")
            sql2 = "UPDATE crud SET nim_mahasiswa=%s WHERE nim_mahasiswa=%s"
            val2 = (nim_baru, nim_lama)
            cursor.execute(sql2, val2)
            print("\n{} data berhasil diubah ".format(cursor.rowcount))
            print("")
            break

        elif pilihan_ubah == 2:
            nama_baru = input(">>> Masukkan Nama baru: ")
            sql2 = "UPDATE crud SET nama_mahasiswa=%s WHERE nim_mahasiswa=%s"
            val2 = (nama_baru, nim_lama)
            cursor.execute(sql2, val2)
            print("\n{} data berhasil diubah ".format(cursor.rowcount))
            print("")
            break

        elif pilihan_ubah == 3:
            prodi_baru = input(">>> Masukkan Prodi Baru: ")
            sql2 = "UPDATE crud SET prodi_mahasiswa=%s WHERE nim_mahasiswa=%s"
            val2 = (prodi_baru, nim_lama)
            cursor.execute(sql2, val2)
            print("\n{} data berhasil diubah ".format(cursor.rowcount))
            print("")
            break

        elif pilihan_ubah == 4:
            mk_baru = input(">>> Masukkan Mata Kuliah Baru: ")
            sql2 = "UPDATE crud SET mk_mahasiswa=%s WHERE nim_mahasiswa=%s"
            val2 = (mk_baru, nim_lama)
            cursor.execute(sql2, val2)
            print("\n{} data berhasil diubah ".format(cursor.rowcount))
            print("")
            break

        elif pilihan_ubah == 5:
            uh1_baru = input(">>> Masukkan Nilai Ulangan Harian Pertama Terbaru: ")
            sql2 = "UPDATE crud SET nilai_uh1=%s WHERE nim_mahasiswa=%s"
            val2 = (uh1_baru, nim_lama)
            cursor.execute(sql2, val2)
            print("\n{} data berhasil diubah ".format(cursor.rowcount))
            print("")
            break

        elif pilihan_ubah == 6:
            uh2_baru = input(">>> Masukkan Nilai Ulangan Kedua Terbaru: ")
            sql2 = "UPDATE crud SET nilai_uh2=%s WHERE nim_mahasiswa=%s"
            val2 = (uh2_baru, nim_lama)
            cursor.execute(sql2, val2)
            print("\n{} data berhasil diubah ".format(cursor.rowcount))
            print("")
            break

        elif pilihan_ubah == 7:
            uts_baru = input(">>> Masukkan Nilai Ujian Tengah Terbaru: ")
            sql2 = "UPDATE crud SET nilai_uts=%s WHERE nim_mahasiswa=%s"
            val2 = (uts_baru, nim_lama)
            cursor.execute(sql2, val2)
            print("\n{} data berhasil diubah ".format(cursor.rowcount))
            print("")
            break

        elif pilihan_ubah == 8:
            uas_baru = input(">>> Masukkan Ujian Akhir Semester Terbaru: ")
            sql2 = "UPDATE crud SET nilai_uas=%s WHERE nim_mahasiswa=%s"
            val2 = (uas_baru, nim_lama)
            cursor.execute(sql2, val2)
            print("\n{} data berhasil diubah ".format(cursor.rowcount))
            print("")
            break

        elif pilihan_ubah == 9:
            break
        else:
            print("Pilihan tidak valid!")
            continue
    
    db.commit()

def main():
    print(">>> Selamat Datang di Database Nilai Mahasiswa UTY <<<")
    while True:
        print("=== PILIHAN MENU ===")
        print("(1) Tambah Data")
        print("(2) Tampilkan Data")
        print("(3) Ubah Data")
        print("(4) Delete Data")
        print("(5) Keluar Aplikasi")

        pilihan = int(input(">>> Masukkan menu pilihan [1/2/3/4/5]: "))

        if pilihan == 1:
            create_data(db)
        elif pilihan == 2:
            read_data(db)
        elif pilihan == 3:
            update_data(db)
        elif pilihan == 4:
            delete_data(db)
        elif pilihan == 5:
            print("\nTerimakasih! <3")
            break
        elif pilihan == 10:
            admin_only(db)
        else:
            print("\nInputan tidak valid")
            print("")
            continue
main()
