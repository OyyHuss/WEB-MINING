import json

# Fungsi untuk membaca dan menghapus data yang tidak diinginkan
def filter_data(data):
    # Hanya menyimpan data dengan description yang bukan "No description available"
    filtered_data = [item for item in data if item.get('description') != "No description available"]
    return filtered_data

# Membaca data dari file pertama (misalnya output.json)
with open('normalisasi_subkategori.json', 'r') as f:  # Ganti dengan nama file JSON pertama Anda
    data1 = json.load(f)

# Membaca data dari file kedua (misalnya file tambahan lain.json)
with open('kategori.json', 'r') as f:  # Ganti dengan nama file JSON kedua Anda
    data2 = json.load(f)

# Gabungkan kedua data
merged_data = data1 + data2

# Filter data yang memiliki 'description' = "No description available"
filtered_data = filter_data(merged_data)

# Menyimpan hasilnya ke file JSON baru
with open('all.json', 'w') as f:  # Ganti dengan nama file hasil yang Anda inginkan
    json.dump(filtered_data, f, ensure_ascii=False, indent=4)

print("Data berhasil digabungkan dan disaring, disimpan ke 'all.json'")
