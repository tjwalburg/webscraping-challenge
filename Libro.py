class Libro(object):

    def __init__(self):
        self.title = ''
        self.price = 0
        self.stock = 0
        self.category = ''
        self.cover = ''
        self.upc = ''
        self.product_type = ''
        self.price_excl_tax = 0
        self.price_incl_tax = 0
        self.tax = 0
        self.availability = ''
        self.number_of_reviews = 0
        self.urlDescription = ''

    def actualizarAtributoLibro(self, atributo, valor):
        self.__dict__[atributo] = valor
