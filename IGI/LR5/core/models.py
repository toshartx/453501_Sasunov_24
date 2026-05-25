from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from datetime import date

# Валидатор для телефона в формате +375 (29) XXX-XX-XX
phone_validator = RegexValidator(
    regex=r'^\+375 \(\d{2}\) \d{3}-\d{2}-\d{2}$',
    message='Телефон должен быть в формате: +375 (29) XXX-XX-XX'
)

class Employee(models.Model):
    """Сотрудник"""
    POSITION_CHOICES = [
        ('manager', 'Менеджер'),
        ('sales', 'Продавец-консультант'),
        ('courier', 'Курьер'),
        ('baker', 'Кондитер'),
        ('admin', 'Администратор'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    position = models.CharField(max_length=50, choices=POSITION_CHOICES, verbose_name='Должность')
    phone = models.CharField(max_length=20, validators=[phone_validator], verbose_name='Телефон')
    birth_date = models.DateField(verbose_name='Дата рождения')
    hire_date = models.DateField(auto_now_add=True, verbose_name='Дата приёма')
    photo = models.ImageField(upload_to='employees/', blank=True, null=True, verbose_name='Фото')
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_position_display()}"
    
    def age(self):
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
    
    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'


class ProductType(models.Model):
    """Вид изделия (категория)"""
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    slug = models.SlugField(unique=True, blank=True, verbose_name='URL-метка')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Вид изделия'
        verbose_name_plural = 'Виды изделий'


class Product(models.Model):
    """Изделие (товар)"""
    UNIT_CHOICES = [
        ('piece', 'штука'),
        ('kg', 'килограмм'),
        ('g', 'грамм'),
    ]
    
    name = models.CharField(max_length=200, verbose_name='Название')
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, related_name='products', verbose_name='Вид изделия')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name='Цена')
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default='piece', verbose_name='Единица измерения')
    is_available = models.BooleanField(default=True, verbose_name='В наличии')
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name='Изображение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    def __str__(self):
        return f"{self.name} - {self.price} руб. ({self.get_unit_display()})"
    
    class Meta:
        verbose_name = 'Изделие'
        verbose_name_plural = 'Изделия'


class Client(models.Model):
    """Клиент"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    phone = models.CharField(max_length=20, validators=[phone_validator], verbose_name='Телефон')
    birth_date = models.DateField(verbose_name='Дата рождения')
    address = models.TextField(verbose_name='Адрес доставки')
    loyalty_discount = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name='Скидка %')
    
    def __str__(self):
        return self.user.get_full_name()
    
    def age(self):
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
    
    def is_adult(self):
        return self.age() >= 18
    
    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Order(models.Model):
    """Заказ"""
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('processing', 'В обработке'),
        ('delivering', 'Доставляется'),
        ('completed', 'Выполнен'),
        ('cancelled', 'Отменён'),
    ]
    
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='orders', verbose_name='Клиент')
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders', verbose_name='Обработал сотрудник')
    products = models.ManyToManyField(Product, through='OrderItem', verbose_name='Товары')
    order_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')
    delivery_date = models.DateField(verbose_name='Дата доставки')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Статус')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Итоговая сумма')
    promo_code_applied = models.CharField(max_length=50, blank=True, null=True, verbose_name='Применённый промокод')
    
    def __str__(self):
        return f"Заказ #{self.id} от {self.order_date.strftime('%d.%m.%Y')} - {self.client}"
    
    def calculate_total(self):
        total = sum(item.subtotal() for item in self.items.all())
        self.total_amount = total
        self.save()
        return total
    
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-order_date']


class OrderItem(models.Model):
    """Товар в заказе (промежуточная модель для ManyToMany)"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items', verbose_name='Товар')
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)], verbose_name='Количество')
    price_at_time = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена на момент заказа')
    
    def subtotal(self):
        return self.quantity * self.price_at_time
    
    def __str__(self):
        return f"{self.product.name} x{self.quantity} в заказе #{self.order.id}"
    
    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказов'

class News(models.Model):
    """Новость"""
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    summary = models.CharField(max_length=300, verbose_name='Краткое содержание (одно предложение)')
    content = models.TextField(verbose_name='Полное содержание')
    image = models.ImageField(upload_to='news/', blank=True, null=True, verbose_name='Изображение')
    published_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-published_date']