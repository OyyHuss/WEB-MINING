import scrapy

class PariwisataSpider(scrapy.Spider):
    name = "pariwisata_subkategori"
    start_urls = ['https://id.wikipedia.org/wiki/Kategori:Pariwisata']

    def parse(self, response):
        # Ambil subkategori dari halaman kategori
        subcategories = response.css('div.mw-category a')
        for subcategory in subcategories:
            title = subcategory.css('::text').get()
            relative_link = subcategory.css('::attr(href)').get()
            full_link = response.urljoin(relative_link)

            # Filter hanya subkategori (bukan kategori utama)
            yield {
                'type': 'subkategori',
                'title': title.strip() if title else "No title",
                'url': full_link
            }

        # Navigasi ke halaman berikutnya jika ada
        next_page = response.css('div#mw-pages a:contains("berikutnya")::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
