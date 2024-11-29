import re
import sys
import json
import pickle

if len(sys.argv) != 4:
    print("\n\nPenggunaan\n\tquery.py [bm25_index] [n] [query]..\n")
    sys.exit(1)

query = sys.argv[3].lower().split(" ")
n = int(sys.argv[2])

# Membaca file indeks BM25
with open(sys.argv[1], 'rb') as indexdb:
    indexFile = pickle.load(indexdb)

print(f"Index file BM25 dimuat dengan {len(indexFile)} kata kunci.")

list_doc = {}

# Langkah 1: Proses setiap kata dalam query
for q in query:
    print(f"Mencari kata kunci: {q}")
    if q not in indexFile:
        print(f"Kata '{q}' tidak ada dalam index.")
        continue
    try:
        for doc in indexFile[q]:
            if doc['url'] in list_doc:
                list_doc[doc['url']]['score'] += doc['score']
            else:
                list_doc[doc['url']] = doc
    except KeyError:
        continue

# Langkah 2: Sortir dokumen berdasarkan skor
list_data = sorted(list_doc.values(), key=lambda k: k['score'], reverse=True)

# Langkah 3: Menampilkan hasil pencarian
if list_data:
    print(f"\nHasil pencarian untuk query: \"{' '.join(query)}\":\n")
    output_list = []
    for data in list_data[:n]:
        # Output untuk kategori utama dan sub-kategori
        main_output = {
            "title": data['title'],
            "url": data['url'],
            "type": data.get('type', 'Tidak tersedia'),  # Menambahkan type di sini
            "description": data.get('description', "Deskripsi tidak tersedia"),
            "image_url": data.get('image_url', "Gambar tidak tersedia")
        }
        output_list.append(main_output)

    # Cetak hasil sebagai JSON
    print(json.dumps(output_list, ensure_ascii=False, indent=4))
else:
    print(f"Tidak ada hasil yang ditemukan untuk query \"{' '.join(query)}\".")
