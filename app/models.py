from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=40, verbose_name='Раздел')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='sub_category')

    def __str__(self):
        return self.name
    
class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="Раздел")
    title = models.CharField(max_length=112, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Текст")
    price = models.IntegerField(verbose_name="Цена")
    contact = models.CharField(max_length=112, verbose_name="Контакт")
    image = models.ImageField(verbose_name="Фото", upload_to='images', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")

    def __str__(self):
        return f'{self.title} опубликовано {self.created_at} {self.author}'
