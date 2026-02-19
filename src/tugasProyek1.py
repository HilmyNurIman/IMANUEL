# Sistem Peminjaman Laptop Sederhana

data_peminjaman = []

def tambah_peminjaman():
    print("\n=== Input Data Peminjaman Laptop ===")
    nama = input("Nama Siswa            : ")
    kelas = input("Kelas                 : ")
    tanggal_pinjam = input("Tanggal Pinjam        : ")
    tanggal_kembali = input("Tanggal Kembali       : ")
    keperluan = input("Keperluan             : ")
    penanggung_jawab = input("Penanggung Jawab/Guru : ")

    data = {
        "Nama": nama,
        "Kelas": kelas,
        "Tanggal Pinjam": tanggal_pinjam,
        "Tanggal Kembali": tanggal_kembali,
        "Keperluan": keperluan,
        "Penanggung Jawab": penanggung_jawab
    }

    data_peminjaman.append(data)
    print("\n✅ Data berhasil ditambahkan!\n")

def tampilkan_data():
    print("\n=== Daftar Peminjaman Laptop ===")
    if len(data_peminjaman) == 0:
        print("Belum ada data peminjaman.")
    else:
        for i, data in enumerate(data_peminjaman, start=1):
            print(f"\nData ke-{i}")
            for key, value in data.items():
                print(f"{key} : {value}")

def menu():
    while True:
        print("\n===== SISTEM PEMINJAMAN LAPTOP =====")
        print("1. Tambah Data Peminjaman")
        print("2. Tampilkan Data Peminjaman")
        print("3. Keluar")

        pilihan = input("Pilih menu (1/2/3): ")

        if pilihan == "1":
            tambah_peminjaman()
        elif pilihan == "2":
            tampilkan_data()
        elif pilihan == "3":
            print("Terima kasih telah menggunakan sistem.")
            break
        else:
            print("Pilihan tidak valid, coba lagi!")

menu()
