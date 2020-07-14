
"""
    Modelos do app de Produtos
"""

from django.db import models
from django.db.models import Q, QuerySet


class ProductManager(models.Manager):
    def with_text(self, text: str) -> QuerySet:
        """
            Realiza a Pesquisa nos produtos cujo o nome contenha "text"
        """
        queryset = self.get_queryset().filter(name__contains=text)
        return queryset

    def expensive_products(self) -> QuerySet:
        """
         Realiza o filtro dos produtos cujo preço seja maior que 500 reais
        """
        return self.get_queryset().filter(price__gte=200)

    def cheap_toys(self) -> QuerySet:
        """
            Retorna a lista com os brinquedos mais baratos.
        """
        return self.get_queryset().filter(category__name="Categoria Exemplo", price__lte=200)

    # filtro para Categoria Exemplo OU itens caros
    def toys_or_expensive_items(self) -> QuerySet:
        """
            Retorna a lista com os brinquedos mais caros.
        """
        query_filter = Q(category__name="Categoria Exemplo") | Q(
            price__gte=500)
        queryset = self.get_queryset().filter(query_filter)
        print(queryset)
        return queryset

    def test_function(self):
        a = self.with_text("")
        b = self.expensive_products()
        c = self.cheap_toys()
        d = self.toys_or_expensive_items()


class Category(models.Model):
    name = models.CharField('Nome', max_length=50)
    description = models.TextField('Descrição')

    def __str__(self):
        return f'{self.name} - {self.products.count()}'

    class Meta:
        verbose_name_plural = 'Categories'


class Product(models.Model):
    """
        Model contendo todos os campos necessários para cadastrar produtos
        no ecomm.
    """
    objects = ProductManager()
    name = models.CharField('Nome', max_length=100)
    description = models.TextField('Descrição')
    price = models.DecimalField('Preço', max_digits=8, decimal_places=2)
    category = models.ForeignKey(
        Category,
        on_delete=models.deletion.DO_NOTHING,
        related_name='products'
    )

    def __str__(self):
        return self.name


class Order(models.Model):
    name = models.CharField('Nome do Cliente', max_length=100)
    payment = models.CharField('Meio de Pagamento', max_length=50)
    products = models.ManyToManyField(Product)

    @property
    def total_amount(self):
        return sum([product.price for product in self.products.all()])

    def __str__(self):
        return f'{self.name} - {self.total_amount}'
