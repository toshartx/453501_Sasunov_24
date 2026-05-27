from django.urls import path, re_path
from . import views
from django.urls import include

app_name = 'core'

urlpatterns = [
    re_path(r'^archive/(?P<year>[0-9]{4})/$', views.year_archive, name='year_archive'),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('news/', views.news_list, name='news_list'),
    path('news/<int:news_id>/', views.news_detail, name='news_detail'),
    path('glossary/', views.glossary_list, name='glossary_list'),
    path('contacts/', views.contacts, name='contacts'),
    path('privacy/', views.privacy, name='privacy'),
    path('vacancies/', views.vacancies, name='vacancies'),
    path('reviews/', views.reviews, name='reviews'),
    path('promocodes/', views.promocodes, name='promocodes'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('api/', include('api_services.urls')),
    path('employee/dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('catalog/', views.catalog, name='catalog'),
    # Управление для суперпользователя
    # Управление для суперпользователя
    path('admin-panel/products/', views.admin_products, name='admin_products'),
    path('admin-panel/products/add/', views.admin_product_add, name='admin_product_add'),
    path('admin-panel/products/<int:product_id>/edit/', views.admin_product_edit, name='admin_product_edit'),
    path('admin-panel/products/<int:product_id>/delete/', views.admin_product_delete, name='admin_product_delete'),
    path('admin-panel/orders/', views.admin_orders, name='admin_orders'),
    path('admin-panel/clients/', views.admin_clients, name='admin_clients'),
    # Управление заказами и клиентами
    path('admin-panel/orders/', views.admin_orders, name='admin_orders'),
    # Единый маршрут для изменения статуса заказа
    path('employee/orders/manage/', views.employee_orders_manage, name='employee_orders_manage'),
    path('order/<int:order_id>/status/', views.update_order_status, name='update_order_status'),
    # Корзина
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:item_id>/', views.cart_remove, name='cart_remove'),
    path('cart/update/<int:item_id>/', views.cart_update, name='cart_update'),
    path('checkout/', views.checkout, name='checkout'),
    path('statistics/', views.statistics, name='statistics'),
    path('set-timezone/', views.set_timezone, name='set_timezone'),
]