# store/models.py
from django.db import models

class Product(models.Model):
    title = models.CharField(max_length=200, verbose_name="نام محصول")
    description = models.TextField(verbose_name="توضیحات")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="قیمت (تومان)")
    stock = models.IntegerField(default=0, verbose_name="موجودی انبار")
    image_url = models.CharField(max_length=500, blank=True, null=True, verbose_name="لینک تصویر")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    def __str__(self):
        return self.title

class Order(models.Model):
    full_name = models.CharField(max_length=100, verbose_name="نام مشتری")
    address = models.TextField(verbose_name="آدرس پستی")
    phone = models.CharField(max_length=15, verbose_name="شماره تماس")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="مجموع مبلغ")
    is_paid = models.BooleanField(default=False, verbose_name="وضعیت پرداخت")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت سفارش")

    def __str__(self):
        return f"سفارش شماره {self.id} - {self.full_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name="سفارش")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="محصول")
    quantity = models.PositiveIntegerField(default=1, verbose_name="تعداد")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="قیمت در زمان خرید")

    def __str__(self):
        return f"{self.quantity} عدد از {self.product.title}"
