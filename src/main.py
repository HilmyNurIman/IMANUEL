# =====================================================
# UI dan Loop Utama Program IMANUEL
# =====================================================
from dotenv import load_dotenv
import os
from groq import Groq
from datetime import datetime
from time import sleep
from data_handler import baca_data_excel, tampilkan_tabel, update_status_kembali, tambah_data_excel
from ai_handler import handle_tanya_bebas
# Import hanya fungsi yang benar-benar dipakai
from data_handler import (
    baca_data_excel,
    hapus_semua_data_excel,
    update_status_kembali,
    tampilkan_tabel,
    tambah_data_excel          # baru ditambahkan di data_handler
)
from ai_handler import handle_tanya_bebas
# Load environment
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    print("❌ GROQ_API_KEY tidak ditemukan!")
    exit()
client = Groq(api_key=GROQ_API_KEY)
DATA_FILE = "peminjaman_laptop.xlsx"
# =====================================================
# UI SELAMAT DATANG
# =====================================================
print("\n" + "="*60)
sleep(0.2)
print(" IMANUEL - ASISTEN AI & SISTEM PEMINJAMAN LAPTOP")
sleep(0.2)
print("="*60)
sleep(0.2)
nama = input("Namamu siapa: ").strip() or "Teman"
print(f"\nHalo {nama}! 👋")
sleep(0.2)
print("Perintah yang tersedia:")
sleep(0.2)
print("- tambah data")
sleep(0.2)
print("- lihat data / tampilkan data / tabel")
sleep(0.2)
print("- evaluasi")
sleep(0.2)
print("- hapus semua data")
sleep(0.2)
print("- ubah status")
sleep(0.2)
print("- keluar\n")
# =====================================================
# LOOP UTAMA
# =====================================================
while True:
    perintah = input(f"{nama}: ").strip().lower()
    if perintah == "keluar":
        print("IMANUEL: Sampai jumpa! 👋")
        break
    elif perintah == "tambah data":
        nama_p = input("Nama peminjam: ").title()
        kelas = input("Kelas: ").upper()
        tgl_pinjam = datetime.now().strftime("%Y-%m-%d %H:%M")
        tgl_kembali = input("Tanggal kembali (kosong jika belum): ") or None
        ket = input("Keterangan: ")
        if tambah_data_excel(nama_p, kelas, tgl_pinjam, tgl_kembali, ket):
            print("✅ Data berhasil disimpan\n")
        else:
            print("❌ Gagal menyimpan data\n")
        continue
    elif perintah in ["lihat data", "tampilkan data", "tabel", "lihat tabel"]:
        data = baca_data_excel()
        tampilkan_tabel(data)
        continue
    elif perintah == "hapus semua data":
        konfirmasi = input("⚠️ Yakin hapus SEMUA data? (ya/tidak): ").lower()
        if konfirmasi == "ya":
            hapus_semua_data_excel()
            print("🧹 Semua data berhasil dihapus!\n")
        else:
            print("❌ Dibatalkan. Data aman.\n")
        continue
    elif perintah == "ubah status":
        nama_ubah = input("Masukkan nama peminjam: ").title()
        kelas_ubah = input("Masukkan kelas peminjam: ").upper()
        if update_status_kembali(nama_ubah, kelas_ubah):
            print("✅ Status kembali berhasil diperbarui.\n")
        else:
            print("❌ Peminjam tidak ditemukan atau dibatalkan.\n")
        continue
    elif perintah == "evaluasi":
        data = baca_data_excel()
        if not data:
            print("⚠️ Data masih kosong\n")
            continue
        ringkasan = "\n".join([
            f"{d['Nama']} | {d['Kelas']} | {d['Tanggal Pinjam']} | "
            f"{d['Tanggal Kembali'] or 'Belum'} | {d['Keterangan']}"
            for d in data
        ])
        prompt = f"""
Berikut data peminjaman laptop sekolah:
{ringkasan}
ATURAN WAJIB:
1. cek kembali berdasarkan data di atas
2. jangan asal bilang belum baca dengan teliti
3. cek kembali tanggal dan apakah sudah dikembalikan atau belum
Tugas:
1. Analisis masalah
2. Jumlah yang belum kembali
3. Saran perbaikan
Jawab singkat dan jelas.
"""
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Kamu evaluator sistem peminjaman sekolah."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6,
            max_tokens=500
        )
        print("\nIMANUEL 🤖:")
        print(completion.choices[0].message.content)
        print()
        continue
    else:
        # Semua perintah lain → ditangani oleh AI (bagian Ghozy)
        handle_tanya_bebas(perintah, client, DATA_FILE)