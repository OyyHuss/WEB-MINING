import scrapy
import json

class PariwisataSpider(scrapy.Spider):
    name = "pariwisata_crawl_subkategori"
    
    def start_requests(self):
        # Membaca file JSON yang berisi daftar subkategori
        with open('subkategori.json', 'r') as f:  # Ganti dengan lokasi file JSON Anda
            subcategories = json.load(f)

        # Mengambil URL dari setiap subkategori dan membuat permintaan (request)
        for subcategory in subcategories:
            url = subcategory['url']
            yield scrapy.Request(url=url, callback=self.parse, meta={'subcategory': subcategory})

    def parse(self, response):
        # Mengambil informasi dari halaman subkategori
        subcategory = response.meta['subcategory']
        title = subcategory['title']
        url = subcategory['url']

        # Mengambil halaman-halaman yang ada di dalam subkategori
        pages = response.css('div.mw-category a::attr(href)').getall()

        # Proses setiap halaman yang ditemukan dalam subkategori
        for page in pages:
            full_url = response.urljoin(page)
            page_title = page.split(":")[-1].replace('_', ' ')  # Memperbaiki format judul
            
            # Menyimpan hasil yang ditemukan untuk halaman-halaman dalam subkategori
            yield response.follow(full_url, callback=self.parse_page_details, meta={
                'subcategory': title,
                'page_title': page_title.strip(),
                'url': full_url
            })

        # Jika ada halaman berikutnya, ikuti dan ambil halaman-halaman lebih lanjut
        next_page = response.css('div#mw-pages a:contains("berikutnya")::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse, meta={'subcategory': subcategory})

    def parse_page_details(self, response):
        # Ambil data dari meta
        subcategory = response.meta['subcategory']
        page_title = response.meta['page_title']
        page_url = response.meta['url']
        
        # Mengambil deskripsi (biasanya ada di paragraf pertama)
        description = response.css('div.mw-parser-output p::text').get()
        
        # Mengambil gambar pertama jika ada
        image_url = response.css('table.infobox img::attr(src)').get()
        if image_url:
            image_url = response.urljoin(image_url)  # Mengubah relatif menjadi URL penuh

        # Menyimpan hasil yang ditemukan untuk halaman ini
        yield {
            'type': 'page',
            'subcategory': subcategory,
            'page_title': page_title,
            'url': page_url,
            'description': description.strip() if description else 'No description available',
            'image_url': image_url if image_url else 'No image available'
        }
