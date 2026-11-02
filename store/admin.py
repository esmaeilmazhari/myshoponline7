from django.contrib import admin
from .models import Category, Product, Order, OrderItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'discount_price', 'stock', 'category']
    list_filter = ['category']

# 👇 این کلاس باعث می‌شود آیتم‌های سفارش داخل صفحه سفارش نمایش داده شوند
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price') # فقط خواندنی باشد تا ادمین اشتباهی تغییرش ندهد

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # 👇 در لیست سفارش‌ها، نام کاربر هم نمایش داده می‌شود
    list_display = ['id', 'full_name', 'user', 'phone', 'total_price', 'status_colored', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['full_name', 'phone', 'tracking_code']
    inlines = [OrderItemInline] # 👈 اتصال آیتم‌ها به صفحه سفارش