from django.contrib import admin
from .models import Category, Product, News, Order, OrderItem

# Регистрация моделей в админке
admin.site.site_header = "Админка магазина сборок ПК"  # Название вверху админки
admin.site.site_title = "PC Shop Admin"
admin.site.index_title = "Управление сайтом"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Что показывать в списке
    search_fields = ('name',)  # Поиск по названию

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price')
    list_filter = ('category',)  # Фильтр справа
    search_fields = ('name', 'description')

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'date')
    list_filter = ('date',)
    search_fields = ('title', 'content')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'status', 'total_price')
    list_filter = ('status', 'created_at')
    readonly_fields = ('user', 'created_at', 'total_price')

# OrderItem показываем внутри заказа
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

# Добавляем OrderItem в админку заказа
OrderAdmin.inlines = [OrderItemInline]