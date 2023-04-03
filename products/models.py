from django.db import models
from mytools.randomslug import get_random
from django.utils.text import slugify


class ProductManager(models.Manager):
    def published(self):
        return self.filter(status='p')

    def discounters(self):
        return self.filter(discount_amount__gt=0)


class CategoryManager(models.Manager):
    pass


class Product(models.Model):
    STATUS_CHOICES = {
        ('d', 'draft'),
        ('p', 'published'),
    }

    name = models.CharField(max_length=60)
    description = models.TextField(max_length=1000, null=True, blank=True)
    image = models.ImageField(blank=True, null=True, upload_to='products/',
                              default='../static/images/default-product.png')
    slug = models.SlugField(unique=True, max_length=80, blank=True)
    price = models.BigIntegerField(default=0, null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='d')
    categories = models.ManyToManyField('Category', 'products', blank=True)
    discount_amount = models.IntegerField(default=0)


    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'
        ordering = ['price']

    def save(self, *args, **kwargs):
        if self.slug:

            super(Product, self).save(*args, **kwargs)

        else:
            self.slug = slugify(self.name) + '-' + get_random(5)
            super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def last_price(self):
        if self.discount_amount > 0:
            price = int(self.price - ((self.price) * ((self.discount_amount) / 100)))

        else:
            price = self.price

        return price

    def get_categories(self):

        categories = ' , '.join([cat.name for cat in self.categories.all()])
        return categories

    objects = ProductManager()


class Category(models.Model):
    name = models.CharField(max_length=60)
    slug = models.SlugField(unique=True, max_length=80, blank=True)
    image = models.ImageField(blank=True, null=True, upload_to='categories/',
                              default='../static/images/default-product.png')
    parent = models.ForeignKey('self', related_name='subcat', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = ['name']

    def save(self, *args, **kwargs):

        if self.slug:

            super(Category, self).save(*args, **kwargs)

        else:
            self.slug = slugify(self.name)
            super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    objects = CategoryManager()
