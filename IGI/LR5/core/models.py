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
    hire_date = models.DateField(auto_now_add=True, verbose_name='Дата приёма')
    photo = models.ImageField(upload_to='employees/', blank=True, null=True, verbose_name='Фото')
    show_on_contacts = models.BooleanField(default=True, verbose_name='Показывать на странице контактов')
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_position_display()}"
    
    @property
    def phone(self):
        """Получить телефон из связанного клиента"""
        if hasattr(self.user, 'client') and self.user.client.phone:
            return self.user.client.phone
        return 'не указан'
    
    @property
    def birth_date(self):
        """Получить дату рождения из связанного клиента"""
        if hasattr(self.user, 'client') and self.user.client.birth_date:
            return self.user.client.birth_date
        return None
    
    @property
    def age(self):
        """Вычислить возраст"""
        if self.birth_date:
            today = date.today()
            return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        return None
    
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
    phone = models.CharField(max_length=20, validators=[phone_validator], blank=True, null=True, verbose_name='Телефон')
    birth_date = models.DateField(blank=True, null=True, verbose_name='Дата рождения')
    address = models.TextField(blank=True, null=True, verbose_name='Адрес доставки')
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

from django.db.models.signals import post_save
from django.dispatch import receiver

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

class CompanyHistory(models.Model):
    """История компании по годам"""
    year = models.PositiveIntegerField(verbose_name='Год')
    event = models.TextField(verbose_name='Событие')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        ordering = ['order', 'year']
        verbose_name = 'История компании'
        verbose_name_plural = 'История компании'

    def __str__(self):
        return f"{self.year} - {self.event[:50]}"


class CompanyRequisite(models.Model):
    """Реквизиты компании"""
    name = models.CharField(max_length=200, verbose_name='Название реквизита')
    value = models.TextField(verbose_name='Значение')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        ordering = ['order']
        verbose_name = 'Реквизит'
        verbose_name_plural = 'Реквизиты'

    def __str__(self):
        return self.name

class Glossary(models.Model):
    """Словарь терминов (вопрос-ответ)"""
    question = models.CharField(max_length=255, verbose_name='Вопрос')
    answer = models.TextField(verbose_name='Ответ')
    added_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')

    class Meta:
        verbose_name = 'Термин'
        verbose_name_plural = 'Словарь терминов'
        ordering = ['-added_date']

    def __str__(self):
        return self.question

class Contact(models.Model):
    """Контакты - сотрудники"""
    name = models.CharField(max_length=150, verbose_name='ФИО')
    position = models.CharField(max_length=100, verbose_name='Должность')
    phone = models.CharField(max_length=20, validators=[phone_validator], verbose_name='Телефон')
    email = models.EmailField(verbose_name='Email')
    description = models.TextField(blank=True, verbose_name='Описание работ')
    photo = models.ImageField(upload_to='contacts/', blank=True, null=True, verbose_name='Фото')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'

    def __str__(self):
        return f"{self.name} - {self.position}"

class Vacancy(models.Model):
    """Вакансии"""
    title = models.CharField(max_length=150, verbose_name='Название вакансии')
    description = models.TextField(verbose_name='Описание')
    salary = models.CharField(max_length=100, blank=True, verbose_name='Зарплата')
    published_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    is_active = models.BooleanField(default=True, verbose_name='Актуально')

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        ordering = ['-published_date']

    def __str__(self):
        return self.title

class Review(models.Model):
    """Отзывы"""
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    
    client_name = models.CharField(max_length=100, verbose_name='Имя')
    rating = models.IntegerField(choices=RATING_CHOICES, verbose_name='Оценка')
    text = models.TextField(verbose_name='Текст отзыва')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_date']

    def __str__(self):
        return f"{self.client_name} - {self.rating}★"

class PromoCode(models.Model):
    """Промокоды и купоны"""
    code = models.CharField(max_length=50, unique=True, verbose_name='Код')
    discount_percent = models.PositiveIntegerField(verbose_name='Скидка %')
    valid_from = models.DateTimeField(verbose_name='Действует с')
    valid_to = models.DateTimeField(verbose_name='Действует до')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    description = models.CharField(max_length=200, blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'
        ordering = ['-valid_to']

    def __str__(self):
        return f"{self.code} - {self.discount_percent}%"

class Cart(models.Model):
    """Корзина покупок"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart', verbose_name='Пользователь')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Корзина {self.user.username}"

    def total(self):
        return sum(item.total() for item in self.items.all())

    def total_quantity(self):
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    """Товар в корзине"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name='Корзина')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)], verbose_name='Количество')

    def __str__(self):
        return f"{self.product.name} x{self.quantity}"

    def total(self):
        return self.quantity * self.product.price

class PickupPoint(models.Model):
    """Точка самовывоза"""
    name = models.CharField(max_length=100, verbose_name='Название')
    address = models.TextField(verbose_name='Адрес')
    working_hours = models.CharField(max_length=100, verbose_name='Часы работы', blank=True)
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    is_active = models.BooleanField(default=True, verbose_name='Активна')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Точка самовывоза'
        verbose_name_plural = 'Точки самовывоза'

    def __str__(self):
        return self.name
