from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.db.models import Sum, Avg, Count, Q
from statistics import median, mode
from .models import (
    News, CompanyHistory, CompanyRequisite, Glossary,
    Vacancy, Review, PromoCode, Client,
    Product, ProductType, Order, OrderItem, Employee, PickupPoint
)
from .forms import RegistrationForm, LoginForm, ReviewForm

import logging
logger = logging.getLogger('core')

# Функции для проверки прав доступа
def is_employee(user):
    return user.is_authenticated and hasattr(user, 'employee')

def is_client(user):
    return user.is_authenticated and hasattr(user, 'client')

def is_admin(user):
    return user.is_superuser

def is_employee_or_admin(user):
    return user.is_superuser or is_employee(user)

def is_client_or_admin(user):
    return user.is_superuser or is_client(user)

@login_required
def profile(request):
    """Личный кабинет пользователя"""
    user = request.user
    
    # Если пользователь — сотрудник
    if hasattr(user, 'employee'):
        employee = user.employee
        orders = Order.objects.filter(employee=employee)
        return render(request, 'core/profile.html', {
            'user_type': 'employee',
            'employee': employee,
            'orders': orders
        })
    
    # Если пользователь — клиент
    elif hasattr(user, 'client'):
        client = user.client
        orders = client.orders.all()
        return render(request, 'core/profile.html', {
            'user_type': 'client',
            'client': client,
            'orders': orders
        })
    
    # Обычный пользователь (только суперпользователь)
    else:
        return render(request, 'core/profile.html', {
            'user_type': 'regular',
            'user': user
        })

def home(request):
    """Главная страница с последней новостью"""
    logger.info(f"Home page visited by {request.user}")
    latest_news = News.objects.filter(is_published=True).first()
    return render(request, 'core/home.html', {'latest_news': latest_news})


def about(request):
    """Страница 'О компании'"""
    history = CompanyHistory.objects.all()
    requisites = CompanyRequisite.objects.all()
    return render(request, 'core/about.html', {
        'history': history,
        'requisites': requisites,
    })

def news_list(request):
    """Список всех новостей"""
    news_list = News.objects.filter(is_published=True)
    return render(request, 'core/news_list.html', {'news_list': news_list})

def news_detail(request, news_id):
    """Детальная страница новости"""
    news = get_object_or_404(News, id=news_id, is_published=True)
    return render(request, 'core/news_detail.html', {'news': news})

def glossary_list(request):
    """Словарь терминов"""
    terms = Glossary.objects.filter(is_published=True)
    return render(request, 'core/glossary_list.html', {'terms': terms})

def contacts(request):
    """Страница контактов - показываем только сотрудников с show_on_contacts=True"""
    employees = Employee.objects.filter(show_on_contacts=True)
    return render(request, 'core/contacts.html', {'employees': employees})

def privacy(request):
    """Страница политики конфиденциальности"""
    return render(request, 'core/privacy.html')

def vacancies(request):
    """Страница вакансий"""
    vacancies_list = Vacancy.objects.filter(is_active=True)
    return render(request, 'core/vacancies.html', {'vacancies': vacancies_list})

def reviews(request):
    """Страница отзывов с формой добавления"""
    reviews_list = Review.objects.filter(is_published=True)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:reviews')
    else:
        form = ReviewForm()
    
    return render(request, 'core/reviews.html', {
        'reviews': reviews_list,
        'form': form
    })

def promocodes(request):
    """Страница промокодов"""
    now = timezone.now()
    active_codes = PromoCode.objects.filter(is_active=True, valid_from__lte=now, valid_to__gte=now)
    archive_codes = PromoCode.objects.filter(is_active=False) | PromoCode.objects.filter(valid_to__lt=now)
    
    return render(request, 'core/promocodes.html', {
        'active_codes': active_codes,
        'archive_codes': archive_codes
    })


def register(request):
    """Регистрация пользователя"""
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Автоматически входим после регистрации
            login(request, user)
            return redirect('core:home')  # Перенаправляем на главную
    else:
        form = RegistrationForm()
    return render(request, 'core/register.html', {'form': form})


def user_login(request):
    """Вход пользователя"""
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('core:home')
    else:
        form = LoginForm()
    return render(request, 'core/login.html', {'form': form})


def user_logout(request):
    """Выход пользователя"""
    logout(request)
    return redirect('core:home')


@login_required
def profile(request):
    """Личный кабинет пользователя"""
    # Получаем или создаём клиента для пользователя
    client, created = Client.objects.get_or_create(user=request.user)
    orders = client.orders.all()
    
    return render(request, 'core/profile.html', {
        'client': client,
        'orders': orders
    })

def year_archive(request, year):
    """Пример использования регулярного выражения в URL"""
    return render(request, 'core/year_archive.html', {'year': year})

def is_employee(user):
    """Проверка, является ли пользователь сотрудником"""
    return user.is_authenticated and hasattr(user, 'employee')

@user_passes_test(is_employee)
def employee_dashboard(request):
    """Панель сотрудника: заказы и клиенты, с которыми работает"""
    employee = request.user.employee
    
    # Заказы, где сотрудник указан
    my_orders = Order.objects.filter(employee=employee).order_by('-order_date')
    
    # Клиенты, которые делали заказы у этого сотрудника
    my_clients = Client.objects.filter(orders__employee=employee).distinct()
    
    # Статистика для сотрудника
    total_orders = my_orders.count()
    total_revenue = my_orders.aggregate(total=Sum('total_amount'))['total'] or 0
    completed_orders = my_orders.filter(status='completed').count()
    
    return render(request, 'core/employee_dashboard.html', {
        'employee': employee,
        'orders': my_orders,
        'clients': my_clients,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'completed_orders': completed_orders,
    })

@user_passes_test(is_admin)
def admin_only_view(request):
    # только для админа
    pass

def catalog(request):
    """Каталог товаров с поиском и сортировкой"""
    logger.info(f"Catalog viewed. Search: {request.GET.get('search', '')}")
    products = Product.objects.filter(is_available=True)
    
    # Поиск по названию
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(name__icontains=search_query)
    
    # Сортировка
    sort_by = request.GET.get('sort', 'name')
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'name':
        products = products.order_by('name')
    elif sort_by == 'type':
        products = products.order_by('product_type__name')
    
    # Фильтр по виду изделия
    type_filter = request.GET.get('type', '')
    if type_filter:
        products = products.filter(product_type_id=type_filter)
    
    product_types = ProductType.objects.all()
    
    return render(request, 'core/catalog.html', {
        'products': products,
        'product_types': product_types,
        'search_query': search_query,
        'sort_by': sort_by,
        'type_filter': type_filter,
    })

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect
from .forms import ProductForm

@staff_member_required
def admin_clients(request):
    """Список всех клиентов для администрирования"""
    clients = Client.objects.all().order_by('user__last_name', 'user__first_name')
    return render(request, 'core/admin_clients.html', {'clients': clients})

@staff_member_required
def admin_orders(request):
    """Список всех заказов для администрирования"""
    orders = Order.objects.all().order_by('-order_date')
    return render(request, 'core/admin_orders.html', {'orders': orders})

@staff_member_required
def admin_products(request):
    """Список товаров для администрирования"""
    products = Product.objects.all()
    return render(request, 'core/admin_products.html', {'products': products})

@staff_member_required
def admin_product_add(request):
    """Добавление товара"""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('core:admin_products')
    else:
        form = ProductForm()
    return render(request, 'core/admin_product_form.html', {'form': form, 'title': 'Добавить товар'})

@staff_member_required
def admin_product_edit(request, product_id):
    """Редактирование товара"""
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('core:admin_products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'core/admin_product_form.html', {'form': form, 'title': 'Редактировать товар'})

@staff_member_required
def admin_product_delete(request, product_id):
    """Удаление товара"""
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('core:admin_products')
    return render(request, 'core/admin_product_confirm_delete.html', {'product': product})

@staff_member_required
def admin_orders(request):
    """Список всех заказов для администрирования"""
    orders = Order.objects.all().order_by('-order_date')
    return render(request, 'core/admin_orders.html', {'orders': orders})

from .models import Cart, CartItem

@login_required
def cart_view(request):
    """Просмотр корзины"""
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return render(request, 'core/cart.html', {'cart': cart})

@login_required
def cart_add(request, product_id):
    """Добавление товара в корзину"""
    product = get_object_or_404(Product, id=product_id, is_available=True)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('core:cart_view')

@login_required
def cart_remove(request, item_id):
    """Удаление товара из корзины"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('core:cart_view')

@login_required
def cart_update(request, item_id):
    """Обновление количества товара"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
    return redirect('core:cart_view')

@login_required
def checkout(request):
    """Оформление заказа"""
    cart, _ = Cart.objects.get_or_create(user=request.user)
    
    if cart.items.count() == 0:
        return redirect('core:cart_view')
    
    if request.method == 'POST':
        # Создаём заказ
        client = request.user.client
        delivery_date = request.POST.get('delivery_date')
        pickup_point_id = request.POST.get('pickup_point')
        
        order = Order.objects.create(
            client=client,
            delivery_date=delivery_date,
            status='new',
            total_amount=cart.total()
        )
        
        # Переносим товары из корзины в заказ
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price_at_time=cart_item.product.price
            )
        
        # Очищаем корзину
        cart.items.all().delete()
        logger.info(f"Order #{order.id} created by {request.user} for {order.total_amount} руб.")
        
        return redirect('core:profile')
    
    # Точки самовывоза
    pickup_points = PickupPoint.objects.filter(is_active=True)
    
    return render(request, 'core/checkout.html', {
        'cart': cart,
        'pickup_points': pickup_points
    })

import matplotlib
matplotlib.use('Agg')  # Важно для сервера без GUI
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.db.models import Sum, Count, Avg, F, ExpressionWrapper, DecimalField
from statistics import median, mode
from datetime import date, timedelta
from django.utils import timezone
from django.db.models.functions import TruncMonth

@user_passes_test(is_employee_or_admin)
def statistics(request):
    """Полные статистические показатели"""
    
    # ===== 1. Товары в алфавитном порядке =====
    products_alpha = Product.objects.filter(is_available=True).order_by('name')
    
    # ===== 2. Клиенты в алфавитном порядке =====
    clients_alpha = Client.objects.all().order_by('user__last_name', 'user__first_name')
    clients_with_data = []
    for client in clients_alpha:
        orders_sum = client.orders.aggregate(total=Sum('total_amount'))['total'] or 0
        clients_with_data.append({
            'client': client,
            'orders_count': client.orders.count(),
            'orders_sum': orders_sum
        })
    
    # ===== 3. Общая сумма продаж =====
    total_sales = Order.objects.aggregate(total=Sum('total_amount'))['total'] or 0
    
    # ===== 4. Статистика по сумме продаж (среднее, мода, медиана) =====
    order_amounts = list(Order.objects.filter(total_amount__gt=0).values_list('total_amount', flat=True))
    if order_amounts:
        amounts_float = [float(amt) for amt in order_amounts]
        avg_sale = sum(amounts_float) / len(amounts_float)
        median_sale = median(amounts_float)
        try:
            mode_sale = mode(amounts_float)
        except:
            mode_sale = "Нет уникальной моды"
    else:
        avg_sale = median_sale = mode_sale = 0
    
    # ===== 5. Статистика по возрасту клиентов (среднее, медиана) =====
    ages = []
    for client in Client.objects.all():
        if client.birth_date:
            age = date.today().year - client.birth_date.year - ((date.today().month, date.today().day) < (client.birth_date.month, client.birth_date.day))
            if age > 0:
                ages.append(age)
    
    if ages:
        avg_age = sum(ages) / len(ages)
        median_age = median(ages)
    else:
        avg_age = median_age = 0
    
    # ===== 6. Какой тип товаров наиболее популярен (по количеству продаж) =====
    popular_types = ProductType.objects.annotate(
        total_sold=Sum('products__order_items__quantity')
    ).order_by('-total_sold')
    
    most_popular_type = popular_types.first()
    
    # ===== 7. Какой тип товаров приносит наибольшую прибыль =====
    profitable_types = ProductType.objects.annotate(
        total_revenue=Sum(F('products__order_items__quantity') * F('products__order_items__price_at_time'))
    ).order_by('-total_revenue')
    
    most_profitable_type = profitable_types.first()
    
    # ===== 8. Топ-5 товаров по прибыли =====
    top_products = Product.objects.annotate(
        total_sold=Sum('order_items__quantity'),
        total_revenue=Sum(F('order_items__quantity') * F('order_items__price_at_time'))
    ).filter(total_sold__gt=0).order_by('-total_revenue')[:5]
    
    # ===== 9. Статусы заказов =====
    status_stats = {
        'new': Order.objects.filter(status='new').count(),
        'processing': Order.objects.filter(status='processing').count(),
        'delivering': Order.objects.filter(status='delivering').count(),
        'completed': Order.objects.filter(status='completed').count(),
        'cancelled': Order.objects.filter(status='cancelled').count(),
    }
    
    # ===== 10. Основные метрики =====
    total_orders = Order.objects.count()
    total_customers = Client.objects.count()
    avg_check = total_sales / total_orders if total_orders > 0 else 0
    
    # ===== КРУГОВАЯ ДИАГРАММА ПО КАТЕГОРИЯМ =====
    category_revenue = ProductType.objects.annotate(
        total_revenue=Sum(
            ExpressionWrapper(
                F('products__order_items__quantity') * F('products__order_items__price_at_time'),
                output_field=DecimalField(max_digits=15, decimal_places=2)
            )
        )
    ).filter(total_revenue__gt=0).order_by('-total_revenue')

    category_names = [cat.name for cat in category_revenue if cat.total_revenue]
    category_revenues = [float(cat.total_revenue) for cat in category_revenue if cat.total_revenue]

    if category_revenues:
        plt.figure(figsize=(10, 8))
        colors = ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40', '#66CC66', '#FF6666']
        
        wedges, texts, autotexts = plt.pie(
            category_revenues,
            labels=category_names,
            autopct=lambda pct: f'{pct:.1f}%\n({int(pct * sum(category_revenues) / 100):,} ₽)',
            colors=colors[:len(category_names)],
            startangle=90,
            textprops={'fontsize': 11}
        )
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(10)
        
        plt.title('Выручка по категориям товаров', fontsize=16, fontweight='bold', pad=20)
        plt.axis('equal')
        
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        buffer.close()
        plt.close()
        
        revenue_by_category_chart = f'data:image/png;base64,{image_base64}'
    else:
        revenue_by_category_chart = None
    context = {
        # Товары и клиенты
        'products_alpha': products_alpha,
        'clients_alpha': clients_alpha,
        'total_sales': round(total_sales, 2),
        
        # Статистика по суммам продаж
        'avg_sale': round(avg_sale, 2),
        'median_sale': round(median_sale, 2),
        'mode_sale': mode_sale,
        
        # Статистика по возрасту
        'avg_age': round(avg_age, 1),
        'median_age': round(median_age, 1),
        
        # Типы товаров
        'most_popular_type': most_popular_type,
        'most_popular_type_sold': popular_types.first().total_sold if popular_types.first() and popular_types.first().total_sold else 0,
        'most_profitable_type': most_profitable_type,
        'most_profitable_type_revenue': round(profitable_types.first().total_revenue, 2) if profitable_types.first() and profitable_types.first().total_revenue else 0,
        
        # Топ товаров
        'top_products': top_products,
        
        # Статусы
        'status_stats': status_stats,
        
        # Основные метрики
        'total_orders': total_orders,
        'total_customers': total_customers,
        'avg_check': round(avg_check, 2),

        'clients_with_data': clients_with_data,
        'revenue_by_category_chart': revenue_by_category_chart,
    }
    
    return render(request, 'core/statistics.html', context)

from django.contrib import messages

def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if not request.user.is_superuser and (not hasattr(request.user, 'employee') or order.employee != request.user.employee):
        messages.error(request, 'У вас нет прав для изменения этого заказа')
    elif request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            messages.success(request, f'Статус заказа #{order.id} изменён на "{order.get_status_display()}"')
            logger.info(f"Order #{order.id} status changed to {order.status} by {request.user}")
    
    if hasattr(request.user, 'employee'):
        return redirect('core:employee_orders_manage')
    return redirect('core:admin_orders')

@user_passes_test(is_employee_or_admin)
def employee_orders_manage(request):
    """Управление заказами для сотрудника (только свои заказы)"""
    if hasattr(request.user, 'employee'):
        employee = request.user.employee
        orders = Order.objects.filter(employee=employee).order_by('-order_date')
    else:
        orders = Order.objects.all().order_by('-order_date')
    
    return render(request, 'core/employee_orders_manage.html', {'orders': orders})