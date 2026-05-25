from django.contrib import admin
from .models import Employee, ProductType, Product, Client, Order, OrderItem, News

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'position', 'phone', 'hire_date')
    list_filter = ('position', 'hire_date')
    search_fields = ('user__first_name', 'user__last_name', 'phone')
    readonly_fields = ('hire_date',)

@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'product_type', 'price', 'unit', 'is_available')
    list_filter = ('product_type', 'is_available', 'unit')
    search_fields = ('name', 'description')
    list_editable = ('price', 'is_available')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone', 'birth_date', 'loyalty_discount')
    search_fields = ('user__first_name', 'user__last_name', 'phone')
    list_editable = ('loyalty_discount',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'employee', 'order_date', 'delivery_date', 'status', 'total_amount')
    list_filter = ('status', 'order_date', 'delivery_date')
    search_fields = ('client__user__first_name', 'client__user__last_name')
    readonly_fields = ('order_date', 'total_amount')
    list_editable = ('status',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'price_at_time', 'subtotal')
    list_filter = ('order__status', 'product__product_type')
    search_fields = ('order__id', 'product__name')
    readonly_fields = ('price_at_time',)

    def subtotal(self, obj):
        return obj.subtotal()
    subtotal.short_description = 'Сумма'

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date', 'is_published')
    list_filter = ('is_published', 'published_date')
    search_fields = ('title', 'summary')
    list_editable = ('is_published',)
    readonly_fields = ('published_date',)

from .models import CompanyHistory, CompanyRequisite

@admin.register(CompanyHistory)
class CompanyHistoryAdmin(admin.ModelAdmin):
    list_display = ('year', 'event', 'order')
    list_editable = ('order',)
    search_fields = ('year', 'event')

@admin.register(CompanyRequisite)
class CompanyRequisiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'order')
    list_editable = ('order',)
    search_fields = ('name',)

from .models import Glossary

@admin.register(Glossary)
class GlossaryAdmin(admin.ModelAdmin):
    list_display = ('question', 'added_date', 'is_published')
    list_filter = ('is_published', 'added_date')
    search_fields = ('question', 'answer')
    list_editable = ('is_published',)
    readonly_fields = ('added_date',)

from .models import Contact, Vacancy, Review, PromoCode

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'phone', 'email', 'order')
    list_editable = ('order',)

@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('title', 'salary', 'published_date', 'is_active')
    list_editable = ('is_active',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'rating', 'created_date', 'is_published')
    list_editable = ('is_published',)

@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percent', 'valid_from', 'valid_to', 'is_active')
    list_editable = ('is_active',)