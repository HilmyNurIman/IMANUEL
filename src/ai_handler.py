import json
from data_handler import baca_data_excel
def handle_tanya_bebas(perintah, client, data_file):
    """Handle semua input yang bukan perintah tetap → kirim ke Groq"""
    data = baca_data_excel()
    konteks = "\n".join([
        f"{d['Nama']} ({d['Kelas']}): Pinjam {d['Tanggal Pinjam']}, "
        f"Kembali {d['Tanggal Kembali'] or 'Belum'}, Keterangan: {d['Keterangan']}"
        for d in data
    ]) if data else "Tidak ada data peminjaman saat ini."
    prompt = f"""
Kamu adalah IMANUEL, asisten pintar dan ramah untuk sistem peminjaman laptop sekolah.
DATA TERBARU SAAT INI (gunakan ini sebagai fakta UTAMA):
{konteks}
User bilang: "{perintah}"
Aturan WAJIB:
-jika user mengatakan hal yang mengarah kepada penambahan data maka katakan jika ingin menambahkan data silahkan ketik "tambah data"
-jika user mengatakan hal yang mengarah menghapus data, maka katakan jika ingin menghapus semua data ketik "hapus semua data"
- Kalau user tanya siapa yang belum kembali, cek Tanggal Kembali:
  - Ada tanggal → SUDAH KEMBALI
  - '-' atau kosong → BELUM KEMBALI
  - pastikan cek kembali data dengan teliti
- Kalau user ingin UPDATE status kembali atau mengatakan misal ("hanif sudah mengembalikan laptop")  
  balas: "ketik 'ubah status' untuk mengubah status peminjam"
- Jawab SINGKAT, jelas, ramah, pakai emoji.
"""
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Kamu IMANUEL, asisten yang selalu pakai data terkini dan jujur."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=200
        )
        respons = completion.choices[0].message.content.strip()
        # Coba parse jika LLM balas dalam format JSON (untuk action update)
        try:
            parsed = json.loads(respons)
            if parsed.get("action") == "update_kembali":
                nama_up = parsed.get("nama", "").strip()
                kelas_up = parsed.get("kelas", "").strip()
                from data_handler import update_status_kembali  # import di sini agar tidak circular
                success, msg = update_status_kembali(nama_up, kelas_up)
                if success:
                    print(f"\nIMANUEL 🤖: {parsed.get('pesan', '✅ Status berhasil diupdate!')}")
                else:
                    print(f"\nIMANUEL 🤖: {msg}")
                return
        except json.JSONDecodeError:
            pass  # bukan JSON → tampilkan biasa
        # Tampilkan respons normal
        print("\nIMANUEL 🤖:")
        print(respons)
        print()
    except Exception as e:
        print(f"\nIMANUEL 🤖: Maaf, ada masalah dengan AI: {str(e)}\n")