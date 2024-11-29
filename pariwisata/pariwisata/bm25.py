import re
import sys
import json
import pickle
import math

if len(sys.argv) != 3:
    print("\nUse python \n\t bm25.py [data.json] [output]\n")
    sys.exit(1)

input_data = sys.argv[1]
output_data = sys.argv[2]

with open(input_data, 'r', encoding='utf-8') as f:
    try:
        content = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        sys.exit(1)

with open("stopword.txt", 'r', encoding='utf-8') as sw_file:
    sw = sw_file.read().splitlines()

df_data = {}
bm25_data = {}
document_lengths = []

k1 = 1.5
b = 0.75

def clean_str(text):
    text = (text.encode('ascii', 'ignore')).decode("utf-8")
    text = re.sub("&.*?;", "", text)
    text = re.sub(">", "", text)
    text = re.sub("[\]\|\[\@\,\$\%\*\&\\\(\)\":]", "", text)
    text = re.sub("-", " ", text)
    text = re.sub("\.+", "", text)
    text = re.sub("^\s+", "", text)
    text = text.lower()
    return text

def process_data(data, parent_title="Root Category"):
    """
    Memproses kategori utama dan sub-kategori secara rekursif.
    """
    clean_title = clean_str(data['title']) if data['title'] != "No title" else "no_title"
    list_word = clean_title.split(" ")
    list_word = [word for word in list_word if word.strip() != '' and word not in sw]

    document_lengths.append(len(list_word))

    tf = {}
    for word in list_word:
        if word in tf:
            tf[word] += 1
        else:
            tf[word] = 1

        if word in df_data:
            df_data[word] += 1
        else:
            df_data[word] = 1

    # Simpan data BM25 dengan informasi parent dan type
    bm25_data[data['url']] = {
        'tf': tf,
        'length': len(list_word),
        'title': data['title'],
        'parent_title': parent_title,
        'type': data.get('type', 'Tidak tersedia'),  # Menambahkan type
        'description': data.get('description', 'Deskripsi tidak tersedia'),
        'image_url': data.get('image_url', None)
    }

    # Proses sub-kategori jika ada
    sub_links = data.get('sub_links', [])
    for sub_data in sub_links:
        process_data(sub_data, parent_title=data['title'])  # Rekursif

# Proses semua data dari JSON input
for category in content:
    process_data(category)

# Hitung rata-rata panjang dokumen
avg_doc_length = sum(document_lengths) / len(document_lengths)

# Hitung IDF untuk setiap kata
idf_data = {}
for word in df_data:
    idf_data[word] = math.log10((len(bm25_data) - df_data[word] + 0.5) / (df_data[word] + 0.5) + 1)

# Hitung skor BM25
bm25_scores = {}
for word in df_data:
    list_doc = []
    for url, data in bm25_data.items():
        tf_value = data['tf'].get(word, 0)
        doc_length = data['length']

        numerator = tf_value * (k1 + 1)
        denominator = tf_value + k1 * (1 - b + b * (doc_length / avg_doc_length))
        score = idf_data[word] * (numerator / denominator)

        doc = {
            'url': url,
            'title': data['title'],
            'score': score,
            'type': data['type'],  # Sertakan type di sini
            'description': data['description'],
            'image_url': data.get('image_url', None)
        }

        if doc['score'] > 0:
            list_doc.append(doc)

    bm25_scores[word] = list_doc

# Simpan data ke file output
with open(output_data, 'wb') as file:
    pickle.dump(bm25_scores, file)

print(f"BM25 data telah disimpan di {output_data}")
