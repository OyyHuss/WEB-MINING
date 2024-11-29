from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

# Fungsi untuk memuat JSON dari file
def load_json(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading {file_name}: {e}")
        return {}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data-preprocessing")
def data_preprocessing():
    kategori = load_json("pariwisata/pariwisata/spiders/kategori.json")
    crawl_subkategori = load_json("pariwisata/pariwisata/spiders/crawl_subkategori.json")
    sub_kategori = load_json("pariwisata/pariwisata/spiders/sub_kategori.json")
    return render_template(
        "data_preprocessing.html",
        kategori=kategori,
        crawl_subkategori=crawl_subkategori,
        sub_kategori=sub_kategori
    )

@app.route("/normalized-data")
def normalized_data():
    normalized = load_json("pariwisata/pariwisata/spiders/normalisasi_subkategori.json")
    return render_template("normalized_data.html", normalized=normalized)

@app.route("/all-data")
def all_data():
    all_data = load_json("pariwisata/pariwisata/spiders/all.json")
    return render_template("all_data.html", all_data=all_data)

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get('query')  # Mengambil query dari parameter GET
    n = int(request.args.get('n', 5))  # Menentukan jumlah hasil yang ingin ditampilkan (default 5)

    # Load data
    all_data = load_json("pariwisata/pariwisata/spiders/all.json")

    # Mencari hasil yang sesuai dengan query
    search_results = []
    if query:
        for item in all_data:
            if query.lower() in item['title'].lower():  # Cek apakah query ada dalam 'title'
                search_results.append(item)

    # Batasi jumlah hasil sesuai dengan 'n'
    search_results = search_results[:n]

    # Render hasil pencarian
    return render_template("results.html", query=query, results=search_results)

if __name__ == "__main__":
    app.run(debug=True)
