from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from decimal import Decimal

from .models import (
    ProductType, Product, Client, Employee, 
    Order, OrderItem, Cart, CartItem, PickupPoint
)


class ProductTypeModelTest(TestCase):
    def setUp(self):
        self.product_type = ProductType.objects.create(
            name='Торты',
            slug='torty'
        )
    
    def test_product_type_creation(self):
        self.assertEqual(self.product_type.name, 'Торты')
        self.assertEqual(str(self.product_type), 'Торты')
    
    def test_product_type_slug(self):
        self.assertEqual(self.product_type.slug, 'torty')


class ProductModelTest(TestCase):
    def setUp(self):
        self.product_type = ProductType.objects.create(name='Торты')
        self.product = Product.objects.create(
            name='Наполеон',
            product_type=self.product_type,
            price=Decimal('350.00'),
            description='Вкусный торт',
            unit='kg'
        )
    
    def test_product_creation(self):
        self.assertEqual(self.product.name, 'Наполеон')
        self.assertEqual(self.product.price, Decimal('350.00'))
        self.assertTrue(self.product.is_available)
    
    def test_product_str(self):
        self.assertIn('Наполеон', str(self.product))
        self.assertIn('350', str(self.product))
    
    def test_product_price_validation(self):
        product = Product(
            name='Тест',
            product_type=self.product_type,
            price=Decimal('-100'),
            description='Отрицательная цена'
        )
        with self.assertRaises(ValidationError):
            product.full_clean()


class ClientModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testclient',
            password='testpass123',
            first_name='Тест',
            last_name='Клиентов'
        )
        self.client_obj = Client.objects.create(
            user=self.user,
            phone='+375 (29) 123-45-67',
            birth_date=date(2000, 1, 15),
            address='г. Минск, ул. Тестовая, 1',
            loyalty_discount=10
        )
    
    def test_client_creation(self):
        self.assertEqual(self.client_obj.user.username, 'testclient')
        self.assertEqual(self.client_obj.phone, '+375 (29) 123-45-67')
        self.assertEqual(self.client_obj.loyalty_discount, 10)
    
    def test_client_age(self):
        age = self.client_obj.age()
        self.assertGreaterEqual(age, 18)
    
    def test_client_is_adult(self):
        self.assertTrue(self.client_obj.is_adult())


class EmployeeModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testemployee',
            password='testpass123',
            first_name='Сотрудник',
            last_name='Тестовый'
        )
        self.employee = Employee.objects.create(
            user=self.user,
            position='sales',
            phone='+375 (29) 111-22-33',
            birth_date=date(1990, 1, 1),
            show_on_contacts=True
        )
    
    def test_employee_creation(self):
        self.assertEqual(self.employee.position, 'sales')
        self.assertEqual(self.employee.get_position_display(), 'Продавец-консультант')
        self.assertTrue(self.employee.show_on_contacts)
    
    def test_employee_phone_property(self):
        # Если нет client, то возвращается 'не указан'
        self.assertEqual(self.employee.phone, 'не указан')


class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testclient')
        self.client_obj = Client.objects.create(user=self.user)
        self.product_type = ProductType.objects.create(name='Торты')
        self.product = Product.objects.create(
            name='Наполеон',
            product_type=self.product_type,
            price=Decimal('350.00'),
            description='Торт'
        )
        self.order = Order.objects.create(
            client=self.client_obj,
            delivery_date=date.today() + timedelta(days=3),
            status='new',
            total_amount=Decimal('700.00')
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            price_at_time=Decimal('350.00')
        )
    
    def test_order_creation(self):
        self.assertEqual(self.order.status, 'new')
        self.assertEqual(self.order.total_amount, Decimal('700.00'))
    
    def test_order_item_subtotal(self):
        self.assertEqual(self.order_item.subtotal(), Decimal('700.00'))
    
    def test_calculate_total(self):
        self.order.calculate_total()
        self.assertEqual(self.order.total_amount, Decimal('700.00'))


class CartModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testclient')
        self.client_obj = Client.objects.create(user=self.user)
        self.product_type = ProductType.objects.create(name='Торты')
        self.product = Product.objects.create(
            name='Наполеон',
            product_type=self.product_type,
            price=Decimal('350.00'),
            description='Торт'
        )
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item = CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=3
        )
    
    def test_cart_total(self):
        self.assertEqual(self.cart.total(), Decimal('1050.00'))
    
    def test_cart_total_quantity(self):
        self.assertEqual(self.cart.total_quantity(), 3)


class PickupPointModelTest(TestCase):
    def setUp(self):
        self.point = PickupPoint.objects.create(
            name='Центральный',
            address='ул. Ленина, 10',
            working_hours='10:00-20:00',
            phone='+375 (29) 111-22-33',
            is_active=True,
            order=1
        )
    
    def test_pickup_point_creation(self):
        self.assertEqual(self.point.name, 'Центральный')
        self.assertTrue(self.point.is_active)
        self.assertEqual(str(self.point), 'Центральный')


class ViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client_obj = Client.objects.create(user=self.user)
    
    def test_home_page_status(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_catalog_page_status(self):
        response = self.client.get('/catalog/')
        self.assertEqual(response.status_code, 200)
    
    def test_login_page(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
    
    def test_register_page(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)
    
    def test_statistics_redirect_for_anonymous(self):
        response = self.client.get('/statistics/')
        self.assertEqual(response.status_code, 302)
    
    def test_statistics_access_for_client(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/statistics/')
        # Клиент не имеет доступа к статистике (нужен is_employee_or_superuser)
        self.assertEqual(response.status_code, 302)

from .forms import RegistrationForm, ReviewForm, ProductForm

class RegistrationFormTest(TestCase):
    def test_valid_registration_form(self):
        form_data = {
            'username': 'newuser',
            'first_name': 'Новый',
            'last_name': 'Пользователь',
            'email': 'new@example.com',
            'phone': '+375 (29) 123-45-67',
            'birth_date': '2000-01-01',
            'address': 'г. Минск',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
        }
        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_invalid_birth_date_under_18(self):
        form_data = {
            'username': 'newuser',
            'first_name': 'Новый',
            'last_name': 'Пользователь',
            'email': 'new@example.com',
            'phone': '+375 (29) 123-45-67',
            'birth_date': '2010-01-01',  # меньше 18 лет
            'address': 'г. Минск',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('birth_date', form.errors)


class ReviewFormTest(TestCase):
    def test_valid_review_form(self):
        form_data = {
            'client_name': 'Иван',
            'rating': 5,
            'text': 'Отличный магазин!',
        }
        form = ReviewForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_invalid_rating(self):
        form_data = {
            'client_name': 'Иван',
            'rating': 10,  # недопустимое значение
            'text': 'Текст',
        }
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())

class ViewCoverageTest(TestCase):
    def setUp(self):
        # Создаём пользователей
        self.admin_user = User.objects.create_superuser(
            username='admin',
            password='adminpass123',
            email='admin@example.com'
        )
        self.employee_user = User.objects.create_user(
            username='employee',
            password='employeepass123'
        )
        self.employee = Employee.objects.create(
            user=self.employee_user,
            position='sales',
            phone='+375 (29) 111-22-33',
            birth_date=date(1990, 1, 1)
        )
        self.client_user = User.objects.create_user(
            username='client',
            password='clientpass123'
        )
        self.client = Client.objects.create(
            user=self.client_user,
            phone='+375 (29) 123-45-67',
            birth_date=date(2000, 1, 1),
            address='Test Address'
        )
        
        # Создаём товары
        self.product_type = ProductType.objects.create(name='Торты')
        self.product = Product.objects.create(
            name='Тестовый торт',
            product_type=self.product_type,
            price=Decimal('500.00'),
            description='Тестовое описание',
            is_available=True
        )
        
        # Создаём заказ
        self.order = Order.objects.create(
            client=self.client,
            employee=self.employee,
            delivery_date=date.today() + timedelta(days=3),
            status='new',
            total_amount=Decimal('1000.00')
        )
    
    def test_about_page(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)
    
    def test_news_list_page(self):
        response = self.client.get('/news/')
        self.assertEqual(response.status_code, 200)
    
    def test_glossary_page(self):
        response = self.client.get('/glossary/')
        self.assertEqual(response.status_code, 200)
    
    def test_contacts_page(self):
        response = self.client.get('/contacts/')
        self.assertEqual(response.status_code, 200)
    
    def test_privacy_page(self):
        response = self.client.get('/privacy/')
        self.assertEqual(response.status_code, 200)
    
    def test_vacancies_page(self):
        response = self.client.get('/vacancies/')
        self.assertEqual(response.status_code, 200)
    
    def test_reviews_page(self):
        response = self.client.get('/reviews/')
        self.assertEqual(response.status_code, 200)
    
    def test_promocodes_page(self):
        response = self.client.get('/promocodes/')
        self.assertEqual(response.status_code, 200)
    
    def test_catalog_page_with_filters(self):
        response = self.client.get('/catalog/?search=торт&sort=price_asc&type=1')
        self.assertEqual(response.status_code, 200)
    
    def test_year_archive_page(self):
        response = self.client.get('/year/2024/')
        self.assertEqual(response.status_code, 200)
    
    def test_statistics_access_for_employee(self):
        self.client.login(username='employee', password='employeepass123')
        response = self.client.get('/statistics/')
        self.assertEqual(response.status_code, 200)
    
    def test_employee_dashboard(self):
        self.client.login(username='employee', password='employeepass123')
        response = self.client.get('/employee/dashboard/')
        self.assertEqual(response.status_code, 200)
    
    def test_employee_orders_manage(self):
        self.client.login(username='employee', password='employeepass123')
        response = self.client.get('/employee/orders/manage/')
        self.assertEqual(response.status_code, 200)
    
    def test_admin_products_for_superuser(self):
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get('/admin-panel/products/')
        self.assertEqual(response.status_code, 200)
    
    def test_admin_orders_for_superuser(self):
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get('/admin-panel/orders/')
        self.assertEqual(response.status_code, 200)
    
    def test_admin_clients_for_superuser(self):
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get('/admin-panel/clients/')
        self.assertEqual(response.status_code, 200)
    
    def test_profile_for_client(self):
        self.client.login(username='client', password='clientpass123')
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)
    
    def test_cart_view(self):
        self.client.login(username='client', password='clientpass123')
        response = self.client.get('/cart/')
        self.assertEqual(response.status_code, 200)
    
    def test_cart_add(self):
        self.client.login(username='client', password='clientpass123')
        response = self.client.get(f'/cart/add/{self.product.id}/')
        self.assertIn(response.status_code, [302, 200])
    
    def test_checkout_view(self):
        self.client.login(username='client', password='clientpass123')
        # Сначала добавим товар в корзину
        self.client.get(f'/cart/add/{self.product.id}/')
        response = self.client.get('/checkout/')
        self.assertEqual(response.status_code, 200)
    
    def test_update_order_status_by_employee(self):
        self.client.login(username='employee', password='employeepass123')
        response = self.client.post(f'/order/{self.order.id}/status/', {'status': 'processing'})
        self.assertIn(response.status_code, [302, 200])
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'processing')
    
    def test_register_post(self):
        response = self.client.post('/register/', {
            'username': 'newuser123',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'new@example.com',
            'phone': '+375 (29) 111-22-33',
            'birth_date': '2000-01-01',
            'address': 'Test Address',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
        })
        self.assertIn(response.status_code, [200, 302])
        self.assertTrue(User.objects.filter(username='newuser123').exists())
    
    def test_login_post(self):
        response = self.client.post('/login/', {
            'username': 'client',
            'password': 'clientpass123'
        })
        self.assertIn(response.status_code, [200, 302])
    
    def test_logout(self):
        self.client.login(username='client', password='clientpass123')
        response = self.client.get('/logout/')
        self.assertIn(response.status_code, [200, 302])

class ApiServicesTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
    
    def test_weather_page_requires_login(self):
        response = self.client.get('/api/weather/')
        self.assertEqual(response.status_code, 302)  # редирект на login
    
    def test_weather_page_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get('/api/weather/')
        self.assertEqual(response.status_code, 200)
    
    def test_recipes_page_requires_login(self):
        response = self.client.get('/api/recipes/')
        self.assertEqual(response.status_code, 302)
    
    def test_recipes_page_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get('/api/recipes/')
        self.assertEqual(response.status_code, 200)

class AdminViewsTest(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username='admin',
            password='adminpass123',
            email='admin@example.com'
        )
        self.product_type = ProductType.objects.create(name='Торты')
        self.product = Product.objects.create(
            name='Тестовый торт',
            product_type=self.product_type,
            price=500,
            description='Описание'
        )
    
    def test_admin_products_access_for_superuser(self):
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get('/admin-panel/products/')
        self.assertEqual(response.status_code, 200)
    
    def test_admin_product_add_post(self):
        self.client.login(username='admin', password='adminpass123')
        response = self.client.post('/admin-panel/products/add/', {
            'name': 'Новый торт',
            'product_type': self.product_type.id,
            'price': 600,
            'description': 'Новое описание',
            'unit': 'kg',
            'is_available': True
        })
        self.assertIn(response.status_code, [200, 302])
    
    def test_admin_product_edit(self):
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(f'/admin-panel/products/{self.product.id}/edit/')
        self.assertEqual(response.status_code, 200)
    
    def test_admin_product_edit_post(self):
        self.client.login(username='admin', password='adminpass123')
        response = self.client.post(f'/admin-panel/products/{self.product.id}/edit/', {
            'name': 'Изменённый торт',
            'product_type': self.product_type.id,
            'price': 700,
            'description': 'Изменённое описание',
            'unit': 'kg',
            'is_available': False
        })
        self.assertIn(response.status_code, [200, 302])
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Изменённый торт')
    
    def test_admin_product_delete(self):
        self.client.login(username='admin', password='adminpass123')
        response = self.client.post(f'/admin-panel/products/{self.product.id}/delete/')
        self.assertIn(response.status_code, [200, 302])
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())
    
    def test_admin_orders(self):
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get('/admin-panel/orders/')
        self.assertEqual(response.status_code, 200)
    
    def test_admin_clients(self):
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get('/admin-panel/clients/')
        self.assertEqual(response.status_code, 200)


class CartAndCheckoutTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testclient', password='testpass')
        self.client_obj = Client.objects.create(user=self.user)
        self.product_type = ProductType.objects.create(name='Торты')
        self.product = Product.objects.create(
            name='Тестовый товар',
            product_type=self.product_type,
            price=100,
            description='Описание',
            is_available=True
        )
        self.pickup_point = PickupPoint.objects.create(
            name='Тестовая точка',
            address='Test Address',
            is_active=True
        )
    
    def test_add_to_cart(self):
        self.client.login(username='testclient', password='testpass')
        response = self.client.get(f'/cart/add/{self.product.id}/')
        self.assertEqual(response.status_code, 302)
        
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.items.count(), 1)
    
    def test_cart_view(self):
        self.client.login(username='testclient', password='testpass')
        self.client.get(f'/cart/add/{self.product.id}/')
        response = self.client.get('/cart/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Тестовый товар')
    
    def test_cart_update(self):
        self.client.login(username='testclient', password='testpass')
        self.client.get(f'/cart/add/{self.product.id}/')
        cart_item = CartItem.objects.get(cart__user=self.user)
        
        response = self.client.post(f'/cart/update/{cart_item.id}/', {'quantity': 5})
        self.assertEqual(response.status_code, 302)
        cart_item.refresh_from_db()
        self.assertEqual(cart_item.quantity, 5)
    
    def test_cart_remove(self):
        self.client.login(username='testclient', password='testpass')
        self.client.get(f'/cart/add/{self.product.id}/')
        cart_item = CartItem.objects.get(cart__user=self.user)
        
        response = self.client.get(f'/cart/remove/{cart_item.id}/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(CartItem.objects.filter(id=cart_item.id).count(), 0)
    
    def test_checkout_view_get(self):
        self.client.login(username='testclient', password='testpass')
        self.client.get(f'/cart/add/{self.product.id}/')
        response = self.client.get('/checkout/')
        self.assertEqual(response.status_code, 200)
    
    def test_checkout_view_post(self):
        self.client.login(username='testclient', password='testpass')
        self.client.get(f'/cart/add/{self.product.id}/')
        response = self.client.post('/checkout/', {
            'delivery_date': '2025-12-31',
            'pickup_point': self.pickup_point.id
        })
        self.assertIn(response.status_code, [200, 302])


class OrderStatusUpdateTest(TestCase):
    def setUp(self):
        self.employee_user = User.objects.create_user(username='employee', password='employeepass')
        self.employee = Employee.objects.create(
            user=self.employee_user,
            position='sales',
            phone='+375 (29) 111-22-33',
            birth_date=date(1990, 1, 1)
        )
        self.client_user = User.objects.create_user(username='client', password='clientpass')
        self.client = Client.objects.create(user=self.client_user)
        self.order = Order.objects.create(
            client=self.client,
            employee=self.employee,
            delivery_date=date.today() + timedelta(days=3),
            status='new',
            total_amount=1000
        )
    
    def test_update_order_status_by_employee(self):
        self.client.login(username='employee', password='employeepass')
        response = self.client.post(f'/order/{self.order.id}/status/', {'status': 'processing'})
        self.assertIn(response.status_code, [200, 302])
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'processing')
    
    def test_update_order_status_invalid_status(self):
        self.client.login(username='employee', password='employeepass')
        response = self.client.post(f'/order/{self.order.id}/status/', {'status': 'invalid'})
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'new')  # статус не изменился