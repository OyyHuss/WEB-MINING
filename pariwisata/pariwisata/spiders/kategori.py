import scrapy

class PariwisataSpider(scrapy.Spider):
    name = "pariwisata_kategori"
    start_urls = ['https://id.wikipedia.org/wiki/Kategori:Pariwisata']

    def parse(self, response):
        # Ambil kategori utama (halaman dalam kategori)
        pages = response.css('div#mw-pages div.mw-category-group a')
        for page in pages:
            title = page.css('::text').get()
            relative_link = page.css('::attr(href)').get()
            full_link = response.urljoin(relative_link)

            # Navigasi ke halaman kategori individual
            yield response.follow(full_link, callback=self.parse_category_page, meta={'title': title.strip()})

        # Navigasi ke halaman berikutnya untuk kategori utama
        next_page = response.css('div#mw-pages a:contains("berikutnya")::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_category_page(self, response):
        # Ambil title dari meta data yang kita kirimkan
        category_title = response.meta['title']
        
        # Ambil deskripsi kategori (biasanya ada di paragraf pertama setelah judul)
        description = response.css('div.mw-parser-output p::text').get()
        
        # Ambil gambar pertama jika ada
        image_url = response.css('table.infobox img::attr(src)').get()
        if image_url:
            image_url = response.urljoin(image_url)  # Mengubah relatif menjadi URL penuh

        # Menghasilkan data kategori beserta informasi tambahan
        yield {
            'type': 'kategori',
            'title': category_title,
            'url': response.url,
            'description': description.strip() if description else 'No description available',
            'image_url': image_url if image_url else 'No image available'
        }
