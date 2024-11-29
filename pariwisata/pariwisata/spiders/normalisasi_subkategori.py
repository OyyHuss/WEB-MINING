import json

# Membaca data JSON dari file
with open('sub_kategori.json', 'r') as f:  # Ganti 'output.json' dengan nama file JSON Anda
    data = json.load(f)

# Menormalisasi data:
# 1. Mengubah 'page_title' menjadi 'title' dan menghapus '/wiki'.
# 2. Mengganti 'type' menjadi 'subcategory' diikuti dengan nama subkategori.
# 3. Menghapus key selain 'type', 'title', 'url', 'description', dan 'image_url'.
for item in data:
    # Mengubah 'type' menjadi 'subcategory' dan menambahkan nama subkategori
    item['type'] = f"subcategory {item.get('subcategory', '')}"

    # Mengubah 'page_title' menjadi 'title' dan menghapus '/wiki' jika ada
    if item.get('page_title', '').startswith('/wiki'):
        item['title'] = item['page_title'][5:]  # Menghapus "/wiki" dari awal
    else:
        item['title'] = item.get('page_title', '')  # Jika tidak ada '/wiki', tetap menggunakan nilai 'page_title'
    
    # Menghapus key 'page_title' dan 'subcategory'
    del item['page_title']
    if 'subcategory' in item:
        del item['subcategory']
    
    # Menjaga key yang diperlukan: 'type', 'title', 'url', 'description', 'image_url'
    keys_to_keep = ['type', 'title', 'url', 'description', 'image_url']
    item = {key: item[key] for key in keys_to_keep if key in item}
    
    # Memperbarui item dalam data
    data[data.index(item)] = item

# Mengurutkan data berdasarkan 'type' secara abjad
data.sort(key=lambda x: x['type'].lower())

# Menyimpan hasilnya ke file JSON baru
with open('output_normalized.json', 'w') as f:  # Ganti dengan nama file yang Anda inginkan
    json.dump(data, f, ensure_ascii=False, indent=4)

print("Data berhasil dinormalisasi dan disimpan ke 'output_normalized.json'")
