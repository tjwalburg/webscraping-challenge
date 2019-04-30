from bs4 import BeautifulSoup
from Libro import Libro
import requests
import csv

class Scraping(object):

    urlBase = 'http://books.toscrape.com/catalogue/'
    url = 'page-@.html'
    maxPage = 51

    def __init__(self):
        self.libros = []
        print('Se obtienen datos del sitio')
        self.obtenerDatos()
        print('Captura de datos finalizado. Se comienza a obtener informacion de detalles de cada libro')
        self.actualizarDetallesLibro()
        print('Actualizacion finalizada. Se comienza a crear el archivo a exportar.')
        self.exportarCsv()
        print('Proceso finalizado')

    def obtenerHtml(self, url):
        datos = requests.get(url)
        return BeautifulSoup(datos.content, 'html.parser')

    def obtenerInformacionPorSelector(self, selector, html, atributo = None):
        if( atributo is None ):
            return html.select_one(selector).text.strip().encode('utf-8')
        else:
            return html.select_one(selector)[atributo]

    def obtenerDatos(self):
        for nPagina in range(1, self.maxPage):
            rows = self.obtenerHtml(self.obtenerUrlPagina(nPagina)).select('ol.row li')
            for row in rows:
                libro = Libro()
                libro.actualizarAtributoLibro('title', self.obtenerInformacionPorSelector('article.product_pod h3', row))
                libro.actualizarAtributoLibro('price', self.obtenerInformacionPorSelector('article.product_pod p.price_color', row))
                libro.actualizarAtributoLibro('cover', self.obtenerInformacionPorSelector('article.product_pod div.image_container img', row, 'src'))
                libro.actualizarAtributoLibro('urlDescription', self.urlBase + self.obtenerInformacionPorSelector('article.product_pod div.image_container a', row, 'href'))
                self.libros.append(libro)

    def obtenerUrlPagina(self, nPagina):
        urlPagina = self.url.replace('@', str(nPagina))
        return self.urlBase + urlPagina

    def actualizarDetallesLibro(self):
        for libro in self.libros:
            soup = self.obtenerHtml(libro.urlDescription)
            libro.actualizarAtributoLibro('availability', self.obtenerInformacionPorSelector('div.product_main p.instock', soup))
            libro.actualizarAtributoLibro('stock', self.obtenerInformacionPorSelector('div.product_main p.instock', soup))

            categoria = soup.select('ul.breadcrumb li')[2].text.strip().encode('utf-8')
            libro.actualizarAtributoLibro('category', categoria)

            descripciones = soup.select('article table tr')
            for descripcion in descripciones:
                columna = self.obtenerNombreColumnaDescripcion(self.obtenerInformacionPorSelector('th', descripcion))
                libro.actualizarAtributoLibro(columna, self.obtenerInformacionPorSelector('td', descripcion))

    def obtenerNombreColumnaDescripcion(self, texto):
        return texto.replace('(', '').replace(')', '').replace('.', '').replace(' ', '_').lower()

    def exportarCsv(self):

        with open('libros.csv', mode='w') as libros_file:
            cabeceras = ['Title', 'Price', 'Stock', 'Category', 'Cover', 'UPC', 'Product type', 'Price (excl. tax)', 'Price (incl. tax)', 'Tax', 'Availability', 'Number of reviews']
            libros_writer = csv.DictWriter(libros_file, fieldnames = cabeceras)
            libros_writer.writeheader()
            for libro in self.libros:
                libros_writer.writerow({'Title': libro.title, 'Price': libro.price, 'Stock': libro.stock, 'Category': libro.category, 'Cover': libro.cover, 'UPC': libro.upc, 'Product type': libro.product_type, 'Price (excl. tax)' : libro.price_excl_tax, 'Price (incl. tax)': libro.price_incl_tax, 'Tax': libro.tax, 'Availability': libro.availability, 'Number of reviews': libro.number_of_reviews})

        libros_file.close()
