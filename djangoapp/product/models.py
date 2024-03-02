from django.db import models
from utils.word_random import slugify_new
from utils.images import resize_image

# Create your models here.

"""        Produto:
            nome - Char
            descricao_curta - Text
            descricao_longa - Text
            imagem - Image
            slug - Slug
            preco_marketing - Float
            preco_marketing_promocional - Float
            tipo - Choices
                ('V', 'Variável'),
                ('S', 'Simples'),
"""


class Product(models.Model):
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    name = models.CharField(max_length=255)
    description_short = models.TextField(max_length=255)
    description_long = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='product_images/%Y/%m/')
    slug = models.SlugField(
        unique=True, default=None,
        null=True, blank=True, max_length=255
    )
    price_marketing = models.FloatField()
    price_marketing_promotional = models.FloatField(default=0)
    type = models.CharField(
        default='V', max_length=1,
        choices=(
            ('V', 'Variation'),
            ('S', 'Simple'),
        )
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.name)

        current_image_name = str(self.image.name)

        super_save = super().save(*args, **kwargs)
        image_changed = False

        if self.image:
            image_changed = current_image_name != self.image.name

        if image_changed:
            resize_image(self.image, 900, quality=80)

        return super_save

    def __str__(self) -> str:
        return self.name


"""       Variacao:
            nome - char
            produto - FK Produto
            preco - Float
            preco_promocional - Float
            estoque - Int
"""


class Variation(models.Model):
    class Meta:
        verbose_name = 'Variation'
        verbose_name_plural = 'Variations'

    name = models.CharField(max_length=50)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name='variation'
    )
    price = models.FloatField()
    price_promotional = models.FloatField(default=0)
    stock = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        return self.name
