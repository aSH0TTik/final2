from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):
    name = models.CharField('Название категории', max_length=100)
    description = models.TextField('Описание', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Product(models.Model):
    name = models.CharField('Название сборки', max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    description = models.TextField('Описание')
    image = models.ImageField('Фото', upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Сборка ПК'
        verbose_name_plural = 'Сборки ПК'

class News(models.Model):
    title = models.CharField('Заголовок', max_length=200)
    content = models.TextField('Текст новости')
    date = models.DateTimeField('Дата', auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('processing', 'В обработке'),
        ('completed', 'Выполнен'),
        ('cancelled', 'Отменён'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Клиент')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='new')
    total_price = models.DecimalField('Общая сумма', max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Заказ №{self.id} от {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField('Количество', default=1)
    price = models.DecimalField('Цена на момент заказа', max_digits=10, decimal_places=2)

    
class Feedback(models.Model):
        name = models.CharField(max_length=100, verbose_name='Имя')
        email = models.EmailField(verbose_name='Email')
        phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
        subject = models.CharField(max_length=200, verbose_name='Тема')
        message = models.TextField(verbose_name='Сообщение')
        created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
        is_processed = models.BooleanField(default=False, verbose_name='Обработано')
    
        class Meta:
            verbose_name = 'Обратная связь'
            verbose_name_plural = 'Обратная связь'
            ordering = ['-created_at']
    
        def __str__(self):
            return f'{self.name} - {self.subject}'