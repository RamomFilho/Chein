from io import BytesIO
from PIL import Image

from django.core.files import File
from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=255)
    slug = models.SlugField()

    class Meta:
        ordering = ('nome',)
    
    def __str__(self):
        return self.nome
    
    def get_absolute_url(self):
        return f'/{self.slug}/'

class Produto(models.Model):
    categoria = models.ForeignKey(Categoria, related_name='produtos', on_delete=models.CASCADE)
    nome = models.CharField(max_length=255)
    slug = models.SlugField()
    descricao = models.TextField(blank=True, null=True)
    preco = models.DecimalField(max_digits=6, decimal_places=2)
    imagem = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)
    data_adicao = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-data_adicao',)
    
    def __str__(self):
        return self.nome
    
    def get_absolute_url(self):
        return f'/{self.categoria.slug}/{self.slug}/'
    
    def get_image(self):
        if self.imagem:
            return self.imagem.url
        return ''
    
    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return self.thumbnail.url
            else:
                return ''

    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail